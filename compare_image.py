import imageio.v2 as imageio
import dssim

def image_similarity(image_path1, image_path2, threshold=0.95):
    # Load images
    image1 = imageio.imread(image_path1)
    image2 = imageio.imread(image_path2)

    # Calculate Structural Similarity Index
    ssim_index = dssim.calculate_ssim(image1, image2)

    # Display result
    if ssim_index >= threshold:
        print("Images are similar. SSIM Index:", ssim_index)
        # Optionally, you can display the images here.
    else:
        print("Images are not similar. SSIM Index:", ssim_index)

# Example usage
reference_image_path = "android.png"
test_image_path = "android1.png"

image_similarity(reference_image_path, test_image_path)

