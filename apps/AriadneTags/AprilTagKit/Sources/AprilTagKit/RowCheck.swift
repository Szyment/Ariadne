import Foundation

/// Field layout: `rows` rows across the track, `perRow` tags in a row, ID = perRow × row + position.
/// Position 0 is on the left looking from A to B; every tag lies with its top edge (the "ID nn" label) towards B.
public struct FieldPlan: Sendable {
    public var rows = 5
    public var perRow = 5
    public var spacing = 0.75          // centre to centre within a row [m]
    public var tagSize = 0.22          // black square [m]
    public var rowDistance = 5.0       // between rows along the track [m]
    public init() {}

    public func row(of id: Int) -> Int? { (id >= 0 && id < rows * perRow) ? id / perRow : nil }
    public func position(of id: Int) -> Int { id % perRow }
    public func ids(inRow r: Int) -> [Int] { (0..<perRow).map { r * perRow + $0 } }
    /// Distance between two tag centres in metres. Each tag's edges give a local image-to-ground mapping
    /// (one tag side along each edge), so camera tilt and tag rotation do not bias the result.
    /// The two estimates, one per tag, are averaged.
    public func distance(_ a: TagDetection, _ b: TagDetection) -> Double {
        let v = b.center - a.center
        return (a.tagUnits(v) + b.tagUnits(v)) / 2 * tagSize
    }
    public func rowLabel(_ r: Int) -> String { r == 0 ? "A" : (r == rows - 1 ? "B" : "\(Int(Double(r) * rowDistance)) m") }
}

public enum SlotState: Equatable, Sendable { case unseen, ok, problem }

public struct Slot: Equatable, Sendable {
    public let id: Int
    public let state: SlotState
    public let note: String?
}

public struct Spacing: Equatable, Sendable {
    public let a: Int, b: Int
    public let measured: Double?   // median [m]
    public let expected: Double
    public let ok: Bool?
}

/// Accumulates detections while walking along one row and checks IDs, order, spacing and orientation against the plan.
/// Every check uses only the last `window` frames, so a correction in the field shows up within a second.
public final class RowCheck {
    public private(set) var plan: FieldPlan
    public private(set) var row: Int?
    public var autoRow: Bool
    public private(set) var seenOrder: [Int] = []
    public private(set) var foreign: [Int] = []
    public private(set) var frames = 0
    /// Row IDs in the order they lie along the row, from the latest frame with at least three of them.
    public private(set) var observedOrder: [Int] = []

    public static let window = 20
    public static let spacingTolerance = 0.15   // relative

    private var spacingSamples: [Int: [Double]] = [:]   // neighbour pair keyed by lower ID [m]
    private var pairOK: [String: [Bool]] = [:]          // spacing of any pair within tolerance
    private var rotHist: [Int: [Int]] = [:]             // rotation needed per frame: 0, 90, -90, 180 [deg, clockwise positive]
    private var orderHist: [Bool] = []                  // frames with ≥ 3 tags: monotonic along the row
    private var flipHist: [Bool] = []                   // frames with ≥ 2 tags: all of them need 180°

    public init(plan: FieldPlan = FieldPlan(), row: Int? = nil) {
        self.plan = plan; self.row = row; self.autoRow = (row == nil)
    }

    public func setPlan(_ p: FieldPlan) {
        plan = p
        reset(row: autoRow ? nil : row)
    }

    public func reset(row newRow: Int?) {
        row = newRow; autoRow = (newRow == nil)
        seenOrder = []; foreign = []; frames = 0; observedOrder = []
        spacingSamples = [:]; pairOK = [:]; rotHist = [:]; orderHist = []; flipHist = []
    }

    private static func push<T>(_ a: inout [T], _ v: T, max n: Int = RowCheck.window) {
        a.append(v); if a.count > n { a.removeFirst(a.count - n) }
    }

    /// Feeds one frame. Returns IDs of this row seen for the first time.
    @discardableResult
    public func ingest(_ detections: [TagDetection]) -> [Int] {
        let inPlan = detections.filter { plan.row(of: $0.id) != nil }
        if row == nil, autoRow, let first = inPlan.first { row = plan.row(of: first.id) }
        guard let r = row else { return [] }
        frames += 1
        var newIDs: [Int] = []
        for d in detections {
            if plan.row(of: d.id) == r {
                if !seenOrder.contains(d.id) { seenOrder.append(d.id); newIDs.append(d.id) }
            } else if !foreign.contains(d.id) {
                foreign.append(d.id)
            }
        }
        let mine = detections.filter { plan.row(of: $0.id) == r }.sorted { $0.id < $1.id }
        guard mine.count >= 2 else { return newIDs }

        // Row axis from the tag centres, pointing towards growing position (left to right looking towards B).
        let n = Double(mine.count)
        let mc = mine.map(\.center).reduce(SIMD2<Double>(0, 0), +) / n
        var sxx = 0.0, syy = 0.0, sxy = 0.0
        for d in mine { let q = d.center - mc; sxx += q.x * q.x; syy += q.y * q.y; sxy += q.x * q.y }
        let th = 0.5 * atan2(2 * sxy, sxx - syy)
        var axis = SIMD2(cos(th), sin(th))
        let mp = mine.map { Double(plan.position(of: $0.id)) }.reduce(0, +) / n
        let corr = mine.map { (Double(plan.position(of: $0.id)) - mp) * (($0.center - mc) * axis).sum() }.reduce(0, +)
        if corr < 0 { axis = -axis }

        // Expected top direction: the label side faces B, i.e. 90° anticlockwise from the axis (image y points down).
        let expectedUp = SIMD2(axis.y, -axis.x)
        let expAngle = atan2(expectedUp.y, expectedUp.x)
        var needs: [Int] = []
        for d in mine {
            var delta = (expAngle - atan2(d.up.y, d.up.x)) * 180 / .pi
            while delta > 180 { delta -= 360 }
            while delta <= -180 { delta += 360 }
            var q = Int((delta / 90).rounded()) * 90
            if q == -180 { q = 180 }
            var h = rotHist[d.id] ?? []
            Self.push(&h, q)
            rotHist[d.id] = h
            needs.append(q)
        }
        Self.push(&flipHist, needs.allSatisfy { $0 == 180 })

        if mine.count >= 3 {
            let along = mine.sorted { (($0.center - mc) * axis).sum() < (($1.center - mc) * axis).sum() }.map(\.id)
            Self.push(&orderHist, along == along.sorted())
            observedOrder = along
        }

        for i in 0..<mine.count {
            for j in (i + 1)..<mine.count {
                let a = mine[i], b = mine[j]
                let dp = plan.position(of: b.id) - plan.position(of: a.id)
                let dist = plan.distance(a, b)
                let expected = Double(dp) * plan.spacing
                let key = "\(a.id)-\(b.id)"
                var h = pairOK[key] ?? []
                Self.push(&h, abs(dist - expected) <= Self.spacingTolerance * expected)
                pairOK[key] = h
                if dp == 1 {
                    var s = spacingSamples[a.id] ?? []
                    Self.push(&s, dist)
                    spacingSamples[a.id] = s
                }
            }
        }
        return newIDs
    }

    private static func mostlyTrue(_ h: [Bool]) -> Bool { h.count >= 3 && Double(h.filter { $0 }.count) / Double(h.count) > 0.5 }

    /// Whole row flipped: in most recent frames every visible tag needs 180°.
    public var reversed: Bool { Self.mostlyTrue(flipHist) }

    /// Rotation the tag needs in degrees (90 clockwise, -90 anticlockwise, 180), or nil when it lies right.
    public func rotationNeeded(_ id: Int) -> Int? {
        guard let h = rotHist[id], h.count >= 3, !reversed else { return nil }
        var counts: [Int: Int] = [:]
        for v in h { counts[v, default: 0] += 1 }
        guard let (q, c) = counts.max(by: { $0.value < $1.value }), q != 0, Double(c) / Double(h.count) > 0.5 else { return nil }
        return q
    }

    public static func rotationText(_ q: Int) -> String {
        switch q {
        case 90: return "rotate 90° clockwise"
        case -90: return "rotate 90° anticlockwise"
        default: return "rotate 180°"
        }
    }

    public static func rotationSymbol(_ q: Int) -> String {
        switch q { case 90: return "↻ 90°"; case -90: return "↺ 90°"; default: return "180°" }
    }

    public var orderWrong: Bool {
        orderHist.count >= 3 && Double(orderHist.filter { !$0 }.count) / Double(orderHist.count) > 0.5
    }

    private func spacingBad(_ id: Int) -> Bool {
        pairOK.contains { key, h in
            key.split(separator: "-").compactMap { Int($0) }.contains(id) && Self.mostlyTrue(h.map { !$0 })
        }
    }

    public var slots: [Slot] {
        guard let r = row else { return [] }
        return plan.ids(inRow: r).map { id in
            guard seenOrder.contains(id) else { return Slot(id: id, state: .unseen, note: nil) }
            var notes: [String] = []
            if let q = rotationNeeded(id) { notes.append(Self.rotationSymbol(q)) }
            if reversed { notes.append("180°") }
            if orderWrong && observedOrder.contains(id) { notes.append("order") }
            else if spacingBad(id) { notes.append("spacing") }
            return Slot(id: id, state: notes.isEmpty ? .ok : .problem, note: notes.isEmpty ? nil : notes.joined(separator: ", "))
        }
    }

    public var spacings: [Spacing] {
        guard let r = row else { return [] }
        return plan.ids(inRow: r).dropLast().map { a in
            let s = spacingSamples[a] ?? []
            let med: Double? = s.isEmpty ? nil : s.sorted()[s.count / 2]
            let ok = med.map { abs($0 - plan.spacing) <= Self.spacingTolerance * plan.spacing }
            return Spacing(a: a, b: a + 1, measured: med, expected: plan.spacing, ok: s.count >= 3 ? ok : nil)
        }
    }

    public var complete: Bool { slots.count == plan.perRow && slots.allSatisfy { $0.state == .ok } && foreign.isEmpty }

    public static func fmt(_ x: Double) -> String { String(format: "%.2f", x) }

    /// Messages in Polish, one per problem.
    public var messages: [String] {
        guard let r = row else { return ["Point the camera at a row of tags."] }
        var m: [String] = []
        if reversed {
            m.append("All visible tags are rotated 180° relative to the ID order. Rotate each by 180° or lay the row in reverse order: IDs increase from left to right looking from A to B, label towards B.")
        }
        if orderWrong {
            m.append("Order along the row: \(observedOrder.map(String.init).joined(separator: " ")), planned \(observedOrder.sorted().map(String.init).joined(separator: " ")).")
        }
        for id in plan.ids(inRow: r) {
            if let q = rotationNeeded(id) { m.append("ID \(id): \(Self.rotationText(q)).") }
        }
        if !orderWrong {
            for s in spacings where s.ok == false {
                m.append("Spacing \(s.a) to \(s.b): \(Self.fmt(s.measured ?? 0)) m instead of \(Self.fmt(s.expected)) m.")
            }
        }
        for f in foreign {
            if let fr = plan.row(of: f) {
                m.append("ID \(f) belongs to row \(plan.rowLabel(fr)), not \(plan.rowLabel(r)).")
            } else {
                m.append("ID \(f) is not in the plan.")
            }
        }
        let missing = slots.filter { $0.state == .unseen }.map { String($0.id) }
        if !missing.isEmpty { m.append("Not seen yet: \(missing.joined(separator: ", ")).") }
        if m.isEmpty && complete { m.append("Row \(plan.rowLabel(r)) matches the plan.") }
        return m
    }
}
