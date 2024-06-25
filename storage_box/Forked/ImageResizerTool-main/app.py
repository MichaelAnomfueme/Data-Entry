import streamlit as st
from PIL import Image, ImageFilter
import os
import glob
from tqdm import tqdm
import tempfile
from zipfile import ZipFile
import base64


def convert_to_instagram_aspect_ratio(image_path):
    # Open the image
    image = Image.open(image_path)

    # Calculate the new size for the square image
    width, height = image.size
    new_size = max(width, height)

    # Create a new blank image with an alpha channel
    new_image = Image.new("RGBA", (new_size, new_size), (0, 0, 0, 0))

    # Calculate the offsets to center the original image
    x_offset = (new_size - width) // 2
    y_offset = (new_size - height) // 2

    # Paste the original image onto the new image as the background
    new_image.paste(image, (x_offset, y_offset))

    # Create a blurred copy of the original image
    blurred_image = image.copy()
    blurred_image = blurred_image.filter(ImageFilter.GaussianBlur(radius=30))

    # Resize the blurred image to fit the square image
    blurred_image = blurred_image.resize((new_size, new_size))

    # Create a new image with alpha channel
    new_image_with_alpha = Image.new("RGBA", (new_size, new_size), (0, 0, 0, 0))

    # Paste the blurred image onto the new image as the foreground
    new_image_with_alpha.paste(blurred_image, (0, 0))

    # Merge the new image with alpha channel and the original image
    final_image = Image.alpha_composite(new_image_with_alpha.convert("RGBA"), new_image.convert("RGBA"))

    # Close the images
    image.close()
    blurred_image.close()
    new_image_with_alpha.close()
    new_image.close()

    return final_image


def main():
    st.title("Instagram Aspect Ratio Converter")

    # Folder selection section
    st.header("Select Folder")

    # Upload ZIP file
    uploaded_file = st.file_uploader("Upload a ZIP file containing images", type="zip")

    if uploaded_file is not None:
        # Extract the uploaded ZIP file to a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "upload.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.read())

            # Extract the contents of the ZIP file
            with ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # Get all image files in the extracted directory
            image_files = glob.glob(os.path.join(temp_dir, "*.jpg")) + glob.glob(
                os.path.join(temp_dir, "*.jpeg")) + glob.glob(os.path.join(temp_dir, "*.png"))

            if len(image_files) > 0:
                # Convert images with progress bar
                progress_bar = st.progress(0)

                for i, image_file in enumerate(tqdm(image_files, desc="Converting images", unit="image")):
                    # Convert image to Instagram aspect ratio
                    converted_image = convert_to_instagram_aspect_ratio(image_file)

                    # Save the converted image in the same folder as the uploaded ZIP file
                    output_folder = os.path.dirname(os.path.abspath(uploaded_file.name))
                    output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_file))[0] + ".png")
                    converted_image.save(output_path)

                    # Update progress bar
                    progress_bar.progress((i + 1) / len(image_files))

                st.success("Image conversion complete!")
                st.warning("Converted images saved in the same folder as the uploaded ZIP file.")
            else:
                st.warning("No image files found in the uploaded folder.")
    else:
        st.info("Upload a ZIP file containing images.")


if __name__ == "__main__":
    main()
