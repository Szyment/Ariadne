import AVFoundation
import AprilTagKit
import SwiftUI
import UIKit

/// Live camera preview with tag outlines, IDs and neighbour spacing drawn on top.
struct CameraPreview: UIViewRepresentable {
    @ObservedObject var model: CameraModel

    func makeUIView(context: Context) -> PreviewUIView {
        let v = PreviewUIView()
        v.previewLayer.session = model.session
        v.previewLayer.videoGravity = .resizeAspectFill
        return v
    }

    func updateUIView(_ v: PreviewUIView, context: Context) {
        v.update(detections: model.detections, bufferSize: model.bufferSize, check: model.check)
    }
}

final class PreviewUIView: UIView {
    override class var layerClass: AnyClass { AVCaptureVideoPreviewLayer.self }
    var previewLayer: AVCaptureVideoPreviewLayer { layer as! AVCaptureVideoPreviewLayer }
    private let overlay = OverlayView()

    override init(frame: CGRect) {
        super.init(frame: frame)
        overlay.isOpaque = false
        overlay.backgroundColor = .clear
        overlay.isUserInteractionEnabled = false
        addSubview(overlay)
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) is not used") }

    override func layoutSubviews() {
        super.layoutSubviews()
        overlay.frame = bounds
        setPortrait()
    }

    private func setPortrait() {
        guard let c = previewLayer.connection else { return }
        if c.isVideoRotationAngleSupported(90), c.videoRotationAngle != 90 { c.videoRotationAngle = 90 }
    }

    func update(detections: [TagDetection], bufferSize: CGSize, check: RowCheck) {
        setPortrait()
        let pl = previewLayer
        // Detections are in sensor pixels; capture-device coordinates are the same frame normalised to 0...1.
        func conv(_ p: SIMD2<Double>) -> CGPoint {
            pl.layerPointConverted(fromCaptureDevicePoint: CGPoint(x: p.x / bufferSize.width, y: p.y / bufferSize.height))
        }
        let plan = check.plan
        let slots = check.slots
        var items: [OverlayView.Item] = []
        for d in detections {
            let inRow = check.row != nil && plan.row(of: d.id) == check.row
            let problem = slots.first(where: { $0.id == d.id })?.state == .problem
            let color: UIColor = !inRow ? .systemRed : (problem ? .systemOrange : .systemGreen)
            let rot = inRow ? check.rotationNeeded(d.id).map { "  " + RowCheck.rotationSymbol($0) } ?? "" : ""
            items.append(.init(corners: d.corners.map(conv), center: conv(d.center), label: "ID \(d.id)\(rot)", color: color))
        }
        var lines: [OverlayView.Line] = []
        if let r = check.row {
            let mine = detections.filter { plan.row(of: $0.id) == r }
            for a in mine {
                guard let b = mine.first(where: { $0.id == a.id + 1 }) else { continue }
                let dist = plan.distance(a, b)
                let ok = abs(dist - plan.spacing) <= RowCheck.spacingTolerance * plan.spacing
                lines.append(.init(from: conv(a.center), to: conv(b.center), label: "\(RowCheck.fmt(dist)) m", ok: ok))
            }
        }
        overlay.items = items
        overlay.lines = lines
        overlay.setNeedsDisplay()
    }
}

final class OverlayView: UIView {
    struct Item { var corners: [CGPoint]; var center: CGPoint; var label: String; var color: UIColor }
    struct Line { var from: CGPoint; var to: CGPoint; var label: String; var ok: Bool }

    var items: [Item] = []
    var lines: [Line] = []

    private let font = UIFont.monospacedDigitSystemFont(ofSize: 17, weight: .semibold)

    override func draw(_ rect: CGRect) {
        for l in lines {
            let p = UIBezierPath()
            p.move(to: l.from); p.addLine(to: l.to)
            p.lineWidth = 2
            (l.ok ? UIColor.systemYellow : UIColor.systemRed).setStroke()
            p.stroke()
            badge(l.label, at: CGPoint(x: (l.from.x + l.to.x) / 2, y: (l.from.y + l.to.y) / 2 - 22),
                  fg: .black, bg: l.ok ? .systemYellow : .systemRed)
        }
        for it in items {
            guard let first = it.corners.first else { continue }
            let p = UIBezierPath()
            p.move(to: first)
            it.corners.dropFirst().forEach { p.addLine(to: $0) }
            p.close()
            p.lineWidth = 3
            it.color.setStroke()
            p.stroke()
            badge(it.label, at: it.center, fg: .white, bg: it.color)
        }
    }

    private func badge(_ text: String, at c: CGPoint, fg: UIColor, bg: UIColor) {
        let s = NSAttributedString(string: text, attributes: [.font: font, .foregroundColor: fg])
        let size = s.size()
        let r = CGRect(x: c.x - size.width / 2 - 6, y: c.y - size.height / 2 - 3, width: size.width + 12, height: size.height + 6)
        bg.withAlphaComponent(0.9).setFill()
        UIBezierPath(roundedRect: r, cornerRadius: 6).fill()
        s.draw(at: CGPoint(x: r.minX + 6, y: r.minY + 3))
    }
}
