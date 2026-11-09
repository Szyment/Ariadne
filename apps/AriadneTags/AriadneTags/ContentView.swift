import AprilTagKit
import SwiftUI

struct ContentView: View {
    @StateObject private var cam = CameraModel()
    @State private var rowChoice = -1          // -1: row picked from the first tag seen
    @State private var showPlan = false
    @AppStorage("tagSizeCm") private var tagSizeCm = 22
    @AppStorage("spacingCm") private var spacingCm = 75

    var body: some View {
        VStack(spacing: 0) {
            ZStack(alignment: .topLeading) {
                CameraPreview(model: cam)
                    .ignoresSafeArea(edges: .top)
                if cam.authorized == false {
                    Text("No camera access. Turn it on in Settings › Ariadne Tags.")
                        .padding()
                        .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 8))
                        .padding()
                }
                Text("\(Int(cam.fps.rounded())) fps · detection \(Int(cam.detectMs.rounded())) ms · tags \(cam.detections.count)")
                    .font(.caption.monospacedDigit())
                    .padding(.horizontal, 8).padding(.vertical, 4)
                    .background(.black.opacity(0.55), in: Capsule())
                    .foregroundStyle(.white)
                    .padding(10)
            }
            panel
        }
        .onAppear {
            UIApplication.shared.isIdleTimerDisabled = true
            cam.setPlan(tagSizeCm: tagSizeCm, spacingCm: spacingCm)
            cam.start()
        }
        .onChange(of: tagSizeCm) { _, _ in cam.setPlan(tagSizeCm: tagSizeCm, spacingCm: spacingCm) }
        .onChange(of: spacingCm) { _, _ in cam.setPlan(tagSizeCm: tagSizeCm, spacingCm: spacingCm) }
        .sheet(isPresented: $showPlan) {
            PlanSheet(tagSizeCm: $tagSizeCm, spacingCm: $spacingCm)
        }
        .onDisappear {
            UIApplication.shared.isIdleTimerDisabled = false
            cam.stop()
        }
    }

    private var panel: some View {
        let check = cam.check
        let plan = check.plan
        _ = cam.checkVersion
        return VStack(alignment: .leading, spacing: 12) {
            Picker("Row", selection: $rowChoice) {
                Text("auto").tag(-1)
                ForEach(0..<plan.rows, id: \.self) { r in Text(plan.rowLabel(r)).tag(r) }
            }
            .pickerStyle(.segmented)
            .onChange(of: rowChoice) { _, v in cam.resetRow(v < 0 ? nil : v) }

            if let r = check.row {
                Text("Row \(plan.rowLabel(r)): ID \(r * plan.perRow) to \(r * plan.perRow + plan.perRow - 1) · tag \(tagSizeCm) cm · spacing \(RowCheck.fmt(plan.spacing)) m")
                    .font(.subheadline).foregroundStyle(.secondary)
                HStack(spacing: 8) {
                    ForEach(check.slots, id: \.id) { s in SlotView(slot: s) }
                }
                HStack(spacing: 6) {
                    ForEach(check.spacings, id: \.a) { s in
                        Text(s.measured.map { "\(RowCheck.fmt($0))" } ?? "·")
                            .font(.caption.monospacedDigit())
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 4)
                            .background(spacingColor(s).opacity(0.18), in: RoundedRectangle(cornerRadius: 6))
                    }
                }
                .padding(.horizontal, 28)
            } else {
                Text("Point the camera at a row of tags. The row is picked from the first tag seen.")
                    .font(.subheadline).foregroundStyle(.secondary)
            }

            ScrollView {
                VStack(alignment: .leading, spacing: 4) {
                    ForEach(check.messages, id: \.self) { m in
                        Text(m).font(.callout).frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
            }
            .frame(maxHeight: 110)

            HStack {
                if cam.hasUltraWide {
                    Picker("Lens", selection: $cam.lens) {
                        ForEach(Lens.allCases) { Text($0.rawValue).tag($0) }
                    }
                    .pickerStyle(.segmented)
                    .frame(width: 140)
                }
                Spacer()
                Button { showPlan = true } label: { Image(systemName: "slider.horizontal.3") }
                    .buttonStyle(.bordered)
                Button("Reset") { cam.resetRow(rowChoice < 0 ? nil : rowChoice) }
                    .buttonStyle(.borderedProminent)
            }
        }
        .padding()
        .background(Color(.systemBackground))
    }

    private func spacingColor(_ s: Spacing) -> Color {
        switch s.ok {
        case .some(true): return .green
        case .some(false): return .red
        case .none: return .gray
        }
    }
}

struct SlotView: View {
    let slot: Slot

    var body: some View {
        VStack(spacing: 2) {
            Text("\(slot.id)")
                .font(.title2.weight(.semibold).monospacedDigit())
            Text(slot.note ?? (slot.state == .ok ? "OK" : " "))
                .font(.caption2)
                .lineLimit(1)
                .minimumScaleFactor(0.6)
        }
        .frame(maxWidth: .infinity, minHeight: 56)
        .background(color.opacity(slot.state == .unseen ? 0.12 : 0.25), in: RoundedRectangle(cornerRadius: 8))
        .overlay(RoundedRectangle(cornerRadius: 8).stroke(color, lineWidth: slot.state == .unseen ? 0 : 2))
    }

    private var color: Color {
        switch slot.state {
        case .unseen: return .gray
        case .ok: return .green
        case .problem: return .orange
        }
    }
}

struct PlanSheet: View {
    @Binding var tagSizeCm: Int
    @Binding var spacingCm: Int
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section("Black square side") {
                    Picker("Tag", selection: $tagSizeCm) {
                        Text("16 cm, A4 sheets").tag(16)
                        Text("22 cm, boards").tag(22)
                    }
                    .pickerStyle(.inline)
                    .labelsHidden()
                }
                Section("Centre spacing within a row") {
                    Stepper("\(RowCheck.fmt(Double(spacingCm) / 100)) m", value: $spacingCm, in: 20...150, step: 5)
                }
                Section {
                    Text("Field plan: 22 cm tags, 0.75 m spacing. Distances are measured using the tag size as scale, so the size must match the print.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Plan")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) { Button("Done") { dismiss() } }
            }
        }
    }
}
