import os
import streamlit as st
from pypdf import PdfReader, PdfWriter


def compress_pdf(input_path, output_path):
    """
    Compresses a PDF file by optimizing content streams.
    """
    # Check if the input file exists
    if not os.path.exists(input_path):
        st.error(f"Error: The file '{input_path}' does not exist.")
        return False

    # Read the original PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Copy pages and apply lossless compression to each page's stream
    for page in reader.pages:
        page.compress_content_streams()  # Reduces text and vector graphic overhead
        writer.add_page(page)

    # Save the newly optimized PDF
    with open(output_path, "wb") as f:
        writer.write(f)

    # Calculate and display the space saved
    initial_size = os.path.getsize(input_path)
    final_size = os.path.getsize(output_path)
    saved_bytes = initial_size - final_size

    # Fixed: Correctly multiplied by 100 for the percentage calculation
    savings_percentage = (saved_bytes / initial_size) * 100 if initial_size > 0 else 0

    st.success("Success! Compressed PDF processing complete.")
    st.write(f"**Original Size:** {initial_size / 1024:.2f} KB")
    st.write(f"**Compressed Size:** {final_size / 1024:.2f} KB")
    st.write(f"**Space Saved:** {saved_bytes / 1024:.2f} KB ({savings_percentage:.1f}%)")
    return True


# --- Streamlit Web Interface Layout ---
st.set_page_config(page_title="Enterprise PDF Compressor", page_icon="📄", layout="centered")

st.title("📄 Enterprise PDF Compressor")
st.write("Upload a PDF file below to optimize and compress its content streams natively in your browser.")

# Interactive File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Set temporary processing paths on the server
    temp_input = "temp_input.pdf"
    temp_output = "compressed_output.pdf"

    # Write the uploaded browser file data to the temp disk location
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Trigger button to run calculation process
    if st.button("Compress PDF Now", type="primary"):
        with st.spinner("Processing optimization algorithms..."):
            success = compress_pdf(temp_input, temp_output)

        if success and os.path.exists(temp_output):
            # Create download package mapping back to client machine
            with open(temp_output, "rb") as file_bytes:
                st.download_button(
                    label="📥 Download Compressed PDF",
                    data=file_bytes,
                    file_name=f"compressed_{uploaded_file.name}",
                    mime="application/pdf"
                )