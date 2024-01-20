#include <opencv2/opencv.hpp>

int main() {
    // Load images
    cv::Mat referenceImage = cv::imread("android.png");
    cv::Mat testImage = cv::imread("android1.png");

    // Check if the images are loaded successfully
    if (referenceImage.empty() || testImage.empty()) {
        std::cerr << "Error loading images." << std::endl;
        return -1;
    }

    // Resize images to a common size
    cv::resize(referenceImage, referenceImage, testImage.size());

    // Convert images to grayscale
    cv::Mat referenceGray, testGray;
    cv::cvtColor(referenceImage, referenceGray, cv::COLOR_BGR2GRAY);
    cv::cvtColor(testImage, testGray, cv::COLOR_BGR2GRAY);

    // Calculate Structural Similarity Index
    cv::Scalar mssim = cv::quality::QualityBRISQUE::compute(referenceGray, testGray);

    // Display result
    double ssimIndex = (mssim[0] + mssim[1] + mssim[2]) / 3.0;

    if (ssimIndex >= 0.95) {
        std::cout << "Images are similar. SSIM Index: " << ssimIndex << std::endl;
        // Optionally, you can display the images here.
    } else {
        std::cout << "Images are not similar. SSIM Index: " << ssimIndex << std::endl;
    }

    return 0;
}

