---
name: swift-vision-specialist
description: Use when implementing Vision Hub AI scanning, product recognition, barcode detection, or real-time camera analysis for FlipScale reseller features
---

# Swift Vision Specialist

Implements Vision framework and CoreML for FlipScale's AI features: product recognition via photos, barcode/QR scanning, label reading, price comparison via image analysis.

## Core Vision Tasks for FlipScale

### 1. Product Recognition (Main Feature)

**Goal:** User snaps photo → app identifies item type → suggests category

```swift
import Vision

class ProductRecognizer {
    let model = try? VNCoreMLModel(for: FlipScaleProductClassifier().model)

    func identifyProduct(from image: UIImage) async -> ProductGuess? {
        guard let cgImage = image.cgImage else { return nil }

        let request = VNCoreMLRequest(model: model) { request, error in
            // Results in request.results
        }

        let handler = VNImageRequestHandler(cgImage: cgImage)
        try? handler.perform([request])

        return parseResults(request.results)
    }

    func parseResults(_ results: [Any]?) -> ProductGuess? {
        guard let classificationResults = results as? [VNClassificationObservation] else {
            return nil
        }

        let topResult = classificationResults.max { $0.confidence < $1.confidence }
        return ProductGuess(
            category: topResult?.identifier ?? "Unknown",
            confidence: topResult?.confidence ?? 0
        )
    }
}
```

### 2. Barcode/QR Reading

```swift
func detectBarcode(from image: UIImage) async -> String? {
    guard let cgImage = image.cgImage else { return nil }

    let barcodeRequest = VNDetectBarcodesRequest()
    let handler = VNImageRequestHandler(cgImage: cgImage)

    try? handler.perform([barcodeRequest])

    return barcodeRequest.results
        .compactMap { $0 as? VNBarcodeObservation }
        .compactMap { $0.payloadStringValue }
        .first
}
```

### 3. Text Recognition (OCR for Price Tags)

```swift
func extractText(from image: UIImage) async -> [String] {
    guard let cgImage = image.cgImage else { return [] }

    let textRequest = VNRecognizeTextRequest()
    textRequest.recognitionLanguages = ["en-US"]

    let handler = VNImageRequestHandler(cgImage: cgImage)
    try? handler.perform([textRequest])

    return textRequest.results
        .compactMap { $0 as? VNRecognizedTextObservation }
        .compactMap { $0.topCandidates(1).first?.string }
}
```

## CoreML Model Integration

### Custom Model for Reseller Items

Train a CoreML model on reseller items (thrift finds, vintage, collectibles):

```swift
// Use Create ML (Mac app) or Create ML Tools (Swift)
// Training data: photos of common reseller items

let modelConfig = MLModelConfiguration()
modelConfig.computeUnits = .all

let imageClassifier = try? FlipScaleProductClassifier(configuration: modelConfig)
```

### Model Performance Metrics

Target for 2026:
- **Accuracy:** 85%+ on common categories
- **Speed:** <200ms per image
- **Memory:** <50MB model size
- **Battery:** <5% drain per 100 photos

## Camera Integration (SwiftUI)

```swift
struct CameraView: View {
    @State var capturedImage: UIImage?
    @State var productGuess: ProductGuess?

    var body: some View {
        ZStack {
            CameraPreview()

            VStack {
                if let guess = productGuess {
                    VStack {
                        Text(guess.category)
                            .font(.title)
                        Text("Confidence: \(Int(guess.confidence * 100))%")
                            .font(.caption)
                    }
                    .padding()
                    .background(Color.black.opacity(0.7))
                    .foregroundColor(.white)
                    .cornerRadius(12)
                    .padding()
                }

                Spacer()

                Button("Take Photo") {
                    CameraManager.shared.capturePhoto { image in
                        Task {
                            let recognizer = ProductRecognizer()
                            productGuess = await recognizer.identifyProduct(from: image)
                        }
                    }
                }
                .padding()
            }
        }
    }
}
```

## Real-Time Scanning (Video)

For continuous scanning while browsing thrift store:

```swift
class RealTimeScannerViewController: UIViewController, AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(
        _ output: AVCaptureOutput,
        didOutput sampleBuffer: CMSampleBuffer,
        from connection: AVCaptureConnection
    ) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }

        let request = VNCoreMLRequest(model: model) { request, error in
            DispatchQueue.main.async {
                self.updateUI(with: request.results)
            }
        }

        let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, orientation: .right)
        try? handler.perform([request])
    }
}
```

## Privacy & Performance Considerations

### On-Device Processing
- ✅ All vision processing happens on device
- ✅ No images sent to server
- ✅ Zero network latency
- ❌ Don't send images to Vision API

### Battery Optimization
- Use lower resolution for previews (480p)
- Full resolution only for final capture
- Disable ML while app backgrounded
- Cache model in memory

### Permission Handling

```swift
func requestCameraPermission() async -> Bool {
    let status = AVCaptureDevice.authorizationStatus(for: .video)

    switch status {
    case .authorized:
        return true
    case .notDetermined:
        return await AVCaptureDevice.requestAccess(for: .video)
    case .denied, .restricted:
        // Show settings link
        return false
    @unknown default:
        return false
    }
}
```

## Vision Hub Server Integration (Future)

When Vision Hub backend is ready:

```swift
// Local processing first, send results + image hash to server
let localResult = await recognizer.identifyProduct(from: image)
let imageHash = image.sha256()

// Server can:
// - Track trending items
// - Improve pricing estimates
// - Detect fraud (suspicious patterns)
// - Never stores raw images
```

## Testing Vision Features

```swift
func testProductRecognition_KnownItems() {
    let testImages = [
        ("vintage_watch.jpg", "Watches"),
        ("designer_jeans.jpg", "Clothing"),
        ("collectible_sneakers.jpg", "Footwear")
    ]

    for (imageName, expectedCategory) in testImages {
        let image = UIImage(named: imageName)!
        let recognizer = ProductRecognizer()

        let result = recognizer.identifyProduct(from: image)
        XCTAssertEqual(result.category, expectedCategory)
        XCTAssertGreaterThan(result.confidence, 0.75)
    }
}
```

## Performance Benchmarks

Target metrics for shipping:
- Photo → Recognition: <250ms
- Real-time scanning: 8+ FPS
- Memory footprint: <100MB
- Battery drain: <2% per 50 photos

## References

- [Vision Framework Docs](https://developer.apple.com/documentation/vision)
- [CoreML Model Creation](https://developer.apple.com/machine-learning/create-ml/)
- [Create ML Tools](https://github.com/apple/coremltools)
- Docs/Product/Features/VISION_HUB.md - Feature spec

