import streamlit as st
import PyPDF2
import re

# Streamlit app title
st.title("Interactive PDF Text Extraction & Flexible Quotation Calculation")

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Add an option to select specific pages to extract text from
st.sidebar.header("Extraction Options")
all_pages = st.sidebar.checkbox("Extract text from all pages", value=True)
page_range = None

if not all_pages:
    start_page = st.sidebar.number_input("Start Page", min_value=1, step=1, value=1)
    end_page = st.sidebar.number_input("End Page", min_value=1, step=1, value=1)
    page_range = (start_page, end_page)

if uploaded_file is not None:
    try:
        # Attempt to read the uploaded PDF file
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        # Determine which pages to extract
        if all_pages:
            page_range = (1, len(reader.pages))

        # Adjust page numbers for zero-indexed list
        start_page, end_page = page_range[0] - 1, page_range[1]

        # Extract text from selected pages
        for page_num in range(start_page, end_page):
            page = reader.pages[page_num]
            text += page.extract_text()

        # Display the extracted text
        st.subheader("Extracted Text")
        st.text_area("Text", text, height=300)

        # Option to download the extracted text
        st.download_button("Download Text", text, file_name="extracted_text.txt")

        # Regular expressions to extract items, quantities, and prices
        quantities = re.findall(r"(\w+)\s*=\s*(\d+)", text)
        prices = re.findall(r"price\s*=\s*Rs\s*(\d+)", text)

        # Ensure the number of quantities matches the number of prices
        if len(quantities) != len(prices):
            st.error("Mismatch between the number of items/quantities and prices.")
        else:
            total_quotation = 0
            individual_calculations = []

            for (item, quantity), price in zip(quantities, prices):
                item_total = int(quantity) * int(price)
                total_quotation += item_total
                individual_calculations.append((item, quantity, price, item_total))

            # Display the total quotation
            st.subheader("Quotation Calculation")
            st.write(f"Total Quotation: Rs {total_quotation:.2f}")

            # Option to display individual item calculations
            if st.checkbox("Show individual item calculations"):
                for item, quantity, price, item_total in individual_calculations:
                    st.write(f"{item.capitalize()}: {quantity} units at Rs {price} each, Total: Rs {item_total}")

        # Additional option to display the number of words in the extracted text
        if st.checkbox("Show word count"):
            word_count = len(text.split())
            st.write(f"Word Count: {word_count}")

    except PyPDF2.errors.PdfReadError:
        st.error("Error reading the PDF file. It might be corrupted or improperly formatted.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

else:
    st.info("Please upload a PDF file to extract text.")
