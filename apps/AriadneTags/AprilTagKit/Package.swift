// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "AprilTagKit",
    platforms: [.iOS(.v17), .macOS(.v13)],
    products: [
        .library(name: "AprilTagKit", targets: ["AprilTagKit"])
    ],
    targets: [
        // AprilTag 3 C library (AprilRobotics/apriltag, BSD 2-Clause), tag36h11 family only.
        .target(
            name: "CAprilTag",
            path: "Sources/CAprilTag",
            cSettings: [
                .headerSearchPath("headers"),
                .headerSearchPath("headers/common"),
                .define("NDEBUG")
            ],
            linkerSettings: [
                .linkedLibrary("m", .when(platforms: [.linux])),
                .linkedLibrary("pthread", .when(platforms: [.linux]))
            ]
        ),
        .target(name: "AprilTagKit", dependencies: ["CAprilTag"], path: "Sources/AprilTagKit")
    ]
)
