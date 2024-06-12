import streamlit as st
from skimage.metrics import structural_similarity 
from PIL import Image
import numpy as np

try:
    import cv2
except ImportError:
    import cv2_headless as cv2

def main():
    st.title("Pan Card Originality Checker")

    # Check if an image has already been uploaded
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None

    # Upload an image if none has been uploaded yet
    if st.session_state.uploaded_image is None:
        st.write("Upload your Pan Card image:")
        uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            st.session_state.uploaded_image = uploaded_image

    # If an image has been uploaded, compare it with the original Pan Card
    if st.session_state.uploaded_image:
        uploaded_img = Image.open(st.session_state.uploaded_image)

        st.write("Uploaded Pan Card:")
        st.image(uploaded_img, caption='Uploaded Pan Card', use_column_width=True)

        # Resize uploaded image to match dimensions of the original Pan Card
        uploaded_img = uploaded_img.resize((250, 160))

        # Convert images to grayscale
        uploaded_gray = cv2.cvtColor(np.array(uploaded_img), cv2.COLOR_RGB2GRAY)

        # Load and resize original Pan Card image
        original_img = Image.open("original_pan_card.png").resize((250, 160))
        original_gray = cv2.cvtColor(np.array(original_img), cv2.COLOR_RGB2GRAY)

        # Compute Structural Similarity Index (SSIM)
        (score, _) = structural_similarity(original_gray, uploaded_gray, full=True)

        st.write("SSIM Score:", score)

        # Conclusion based on SSIM score
        if score >= 0.9:
            st.write("Conclusion: The uploaded Pan Card image closely matches the original one. It appears to be genuine.")
        else:
            st.write("Conclusion: The uploaded Pan Card image differs significantly from the original one. It may be tampered or fake.")

    # Button to clear uploaded image
    if st.button("Clear Uploaded Image"):
        st.session_state.uploaded_image = None

if __name__ == "__main__":
    main()
