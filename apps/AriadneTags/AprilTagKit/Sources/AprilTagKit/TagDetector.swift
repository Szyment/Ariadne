import CAprilTag

/// One tag36h11 detection in image pixel coordinates (x right, y down).
public struct TagDetection: Equatable, Sendable {
    public let id: Int
    public let hamming: Int
    public let margin: Float
    public let center: SIMD2<Double>
    /// Corners in tag order: bottom-left, bottom-right, top-right, top-left of the printed tag.
    public let corners: [SIMD2<Double>]

    public init(id: Int, hamming: Int = 0, margin: Float = 100, center: SIMD2<Double>, corners: [SIMD2<Double>]) {
        self.id = id; self.hamming = hamming; self.margin = margin; self.center = center; self.corners = corners
    }

    /// Mean side length of the black square in pixels.
    public var sidePx: Double {
        (0..<4).map { length(corners[$0], corners[($0 + 1) % 4]) }.reduce(0, +) / 4
    }

    /// Image vector `v` expressed in tag sides, using this tag's edges as a local affine frame.
    public func tagUnits(_ v: SIMD2<Double>) -> Double {
        let e1 = ((corners[1] - corners[0]) + (corners[2] - corners[3])) / 2
        let e2 = ((corners[3] - corners[0]) + (corners[2] - corners[1])) / 2
        let det = e1.x * e2.y - e1.y * e2.x
        guard abs(det) > 1e-9 else { return 0 }
        let x = (v.x * e2.y - v.y * e2.x) / det
        let y = (e1.x * v.y - e1.y * v.x) / det
        return (x * x + y * y).squareRoot()
    }

    /// Unit vector from the bottom edge to the top edge of the printed tag (the side with the "ID nn" label).
    public var up: SIMD2<Double> {
        let v = (corners[2] + corners[3]) / 2 - (corners[0] + corners[1]) / 2
        return v / max(1e-9, (v * v).sum().squareRoot())
    }
}

@inline(__always) func length(_ a: SIMD2<Double>, _ b: SIMD2<Double>) -> Double {
    let d = a - b
    return (d * d).sum().squareRoot()
}

/// Thin wrapper over the AprilTag C detector. Not thread-safe: call `detect` from one queue.
public final class TagDetector {
    private let td: UnsafeMutablePointer<apriltag_detector_t>
    private let tf: UnsafeMutablePointer<apriltag_family_t>

    public init(decimate: Float = 2, threads: Int = 4) {
        td = apriltag_detector_create()
        tf = tag36h11_create()
        apriltag_detector_add_family_bits(td, tf, 2)
        td.pointee.quad_decimate = decimate
        td.pointee.quad_sigma = 0
        td.pointee.nthreads = Int32(threads)
        td.pointee.refine_edges = true
        td.pointee.decode_sharpening = 0.25
    }

    deinit {
        apriltag_detector_destroy(td)
        tag36h11_destroy(tf)
    }

    public var decimate: Float {
        get { td.pointee.quad_decimate }
        set { td.pointee.quad_decimate = newValue }
    }

    /// Detects tags in an 8-bit grayscale image (for camera frames: the Y plane of a 420f buffer).
    public func detect(gray: UnsafeMutablePointer<UInt8>, width: Int, height: Int, stride: Int,
                       minMargin: Float = 20) -> [TagDetection] {
        var im = image_u8_t(width: Int32(width), height: Int32(height), stride: Int32(stride), buf: gray)
        guard let dets = apriltag_detector_detect(td, &im) else { return [] }
        defer { apriltag_detections_destroy(dets) }
        var out: [TagDetection] = []
        let n = Int(zarray_size(dets))
        out.reserveCapacity(n)
        for i in 0..<n {
            var ptr: UnsafeMutablePointer<apriltag_detection_t>? = nil
            zarray_get(dets, Int32(i), &ptr)
            guard let d = ptr?.pointee, d.decision_margin >= minMargin else { continue }
            let p = d.p
            let corners = [SIMD2(p.0.0, p.0.1), SIMD2(p.1.0, p.1.1), SIMD2(p.2.0, p.2.1), SIMD2(p.3.0, p.3.1)]
            out.append(TagDetection(id: Int(d.id), hamming: Int(d.hamming), margin: d.decision_margin,
                                    center: SIMD2(d.c.0, d.c.1), corners: corners))
        }
        return out
    }
}
