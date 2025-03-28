import streamlit as st
import PyPDF2
import pandas as pd
import zipfile
import os
import shutil

# Streamlit app title
st.title("PDF Splitter and Renamer")

# Upload PDF file
pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

# Upload Excel file
excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if pdf_file and excel_file:
    # Read the Excel file
    names_df = pd.read_excel(excel_file)
    names_list = names_df.iloc[:, 0].tolist()  # Assuming names are in the first column

    # Read the PDF file using PdfReader (instead of PdfFileReader)
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Check if the number of pages matches the number of names
    if len(pdf_reader.pages) != len(names_list):
        st.error("The number of pages in the PDF does not match the number of names in the Excel file.")
    else:
        # Create a directory to save the split PDF files
        output_dir = "split_pdfs"
        
        # Clear the output directory if it already exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)  # Remove the old directory and its contents

        os.makedirs(output_dir, exist_ok=True)

        # Split and save each page with the respective name
        for i in range(len(pdf_reader.pages)):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[i])

            output_filename = f"{names_list[i]}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

        # Create a ZIP file containing all the split PDFs
        zip_filename = "split_pdfs.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in os.listdir(output_dir):
                zipf.write(os.path.join(output_dir, file), file)

        # Provide a link to download the ZIP file
        with open(zip_filename, "rb") as f:
            st.download_button(
                label="Download ZIP",
                data=f,
                file_name=zip_filename,
                mime="application/zip"
            )

        st.success("PDF has been split and renamed successfully. Click the button above to download the files.")

        # Remove the temporary files and directory after the ZIP is created
        shutil.rmtree(output_dir)  # Delete the output directory
        os.remove(zip_filename)  # Delete the ZIP file after download link is provided
