import AVFoundation
import AprilTagKit
import SwiftUI
import UIKit

enum Lens: String, CaseIterable, Identifiable, Sendable {
    case wide = "1×", ultraWide = "0.5×"
    var id: String { rawValue }
    var deviceType: AVCaptureDevice.DeviceType { self == .wide ? .builtInWideAngleCamera : .builtInUltraWideCamera }
}

struct FrameResult: Sendable {
    let detections: [TagDetection]
    let width: Int
    let height: Int
    let detectMs: Double
    let frameInterval: Double
}

/// Owns the capture session and the detector. Everything here runs on its private serial queue.
final class CaptureController: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate, @unchecked Sendable {
    let session = AVCaptureSession()
    var onFrame: (@Sendable (FrameResult) -> Void)?
    var onUltraWide: (@Sendable (Bool) -> Void)?

    private let queue = DispatchQueue(label: "ariadne.camera", qos: .userInitiated)
    private let output = AVCaptureVideoDataOutput()
    private let detector = TagDetector(decimate: 2, threads: 4)
    private var input: AVCaptureDeviceInput?
    private var configured = false
    private var lastFrame: CFTimeInterval = 0

    func start() { queue.async { self.configureAndRun() } }
    func stop() { queue.async { if self.session.isRunning { self.session.stopRunning() } } }
    func setLens(_ lens: Lens) { queue.async { self.configureInput(lens) } }

    private func configureAndRun() {
        if !configured {
            configured = true
            session.beginConfiguration()
            if session.canSetSessionPreset(.hd1920x1080) { session.sessionPreset = .hd1920x1080 }
            output.videoSettings = [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarFullRange]
            output.alwaysDiscardsLateVideoFrames = true
            output.setSampleBufferDelegate(self, queue: queue)
            if session.canAddOutput(output) { session.addOutput(output) }
            session.commitConfiguration()
            configureInput(.wide)
            onUltraWide?(AVCaptureDevice.default(.builtInUltraWideCamera, for: .video, position: .back) != nil)
        }
        if !session.isRunning { session.startRunning() }
    }

    private func configureInput(_ lens: Lens) {
        guard let device = AVCaptureDevice.default(lens.deviceType, for: .video, position: .back)
                ?? AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back),
              let newInput = try? AVCaptureDeviceInput(device: device) else { return }
        session.beginConfiguration()
        if let old = input { session.removeInput(old) }
        if session.canAddInput(newInput) {
            session.addInput(newInput)
            input = newInput
        } else if let old = input, session.canAddInput(old) {
            session.addInput(old)
        }
        if session.canSetSessionPreset(.hd1920x1080) { session.sessionPreset = .hd1920x1080 }
        session.commitConfiguration()
        do {
            try device.lockForConfiguration()
            if device.isFocusModeSupported(.continuousAutoFocus) { device.focusMode = .continuousAutoFocus }
            if device.isGeometricDistortionCorrectionSupported { device.isGeometricDistortionCorrectionEnabled = true }
            device.unlockForConfiguration()
        } catch {}
    }

    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        guard let pb = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        CVPixelBufferLockBaseAddress(pb, .readOnly)
        defer { CVPixelBufferUnlockBaseAddress(pb, .readOnly) }
        guard let base = CVPixelBufferGetBaseAddressOfPlane(pb, 0) else { return }
        let w = CVPixelBufferGetWidthOfPlane(pb, 0)
        let h = CVPixelBufferGetHeightOfPlane(pb, 0)
        let stride = CVPixelBufferGetBytesPerRowOfPlane(pb, 0)

        let t0 = CACurrentMediaTime()
        let dets = detector.detect(gray: base.assumingMemoryBound(to: UInt8.self), width: w, height: h, stride: stride)
        let t1 = CACurrentMediaTime()
        let interval = lastFrame > 0 ? t1 - lastFrame : 0
        lastFrame = t1
        onFrame?(FrameResult(detections: dets, width: w, height: h, detectMs: (t1 - t0) * 1000, frameInterval: interval))
    }
}

/// UI state for the camera screen.
@MainActor
final class CameraModel: ObservableObject {
    let controller = CaptureController()
    let check = RowCheck()
    var session: AVCaptureSession { controller.session }

    @Published private(set) var detections: [TagDetection] = []
    @Published private(set) var bufferSize = CGSize(width: 1920, height: 1080)
    @Published private(set) var fps: Double = 0
    @Published private(set) var detectMs: Double = 0
    @Published private(set) var authorized: Bool?
    @Published private(set) var hasUltraWide = false
    @Published private(set) var checkVersion = 0
    @Published var lens: Lens = .wide {
        didSet { if lens != oldValue { controller.setLens(lens) } }
    }

    private let haptic = UIImpactFeedbackGenerator(style: .medium)

    init() {
        controller.onFrame = { [weak self] r in
            Task { @MainActor in self?.handle(r) }
        }
        controller.onUltraWide = { [weak self] has in
            Task { @MainActor in self?.hasUltraWide = has }
        }
    }

    func start() {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            authorized = true
            controller.start()
        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .video) { [weak self] ok in
                Task { @MainActor in
                    self?.authorized = ok
                    if ok { self?.controller.start() }
                }
            }
        default:
            authorized = false
        }
    }

    func stop() { controller.stop() }

    func setPlan(tagSizeCm: Int, spacingCm: Int) {
        var p = check.plan
        p.tagSize = Double(tagSizeCm) / 100
        p.spacing = Double(spacingCm) / 100
        check.setPlan(p)
        checkVersion &+= 1
    }

    func resetRow(_ row: Int?) {
        check.reset(row: row)
        checkVersion &+= 1
    }

    private func handle(_ r: FrameResult) {
        detections = r.detections
        bufferSize = CGSize(width: r.width, height: r.height)
        detectMs = r.detectMs
        if r.frameInterval > 0 { fps = fps == 0 ? 1 / r.frameInterval : 0.9 * fps + 0.1 / r.frameInterval }
        let newIDs = check.ingest(r.detections)
        if !newIDs.isEmpty { haptic.impactOccurred() }
        checkVersion &+= 1
    }
}
