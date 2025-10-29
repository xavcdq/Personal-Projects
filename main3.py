import streamlit as st
from tika import parser

# Add a file uploader to the app


def extraction():
    uploaded_file = st.file_uploader("Select a file", type=["pdf", "docx", "txt"], key="for_ext")
    # Add a button to extract content
    if st.button("Extract Content", key = "extract_button"):
        if uploaded_file is not None:
            # Parse the uploaded file using Tika
            parsed_data = parser.from_file(uploaded_file)
            
            # Extract the content from the parsed data
            content = parsed_data["content"].strip()
            
            # Create a text box to display the extracted content
            st.text_area("Extracted Content:", value=content, height=500)
        else:
            st.write("Please select a file to extract content from.")



import fitz  # PyMuPDF
from PIL import Image
import io
import numpy as np

def extract_images_from_pdf(file):
    images = []
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        for img in image_list:
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # Image file extension

            # Convert the extracted image bytes to a PIL Image
            try:
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)
            except Exception as e:
                st.write(f"Error processing image on page {page_number + 1}: {e}")
                continue

    return images

def main():
    uploaded_file = st.file_uploader("Select a file", type=["pdf", "docx", "txt"], key = "for_ext")
    if uploaded_file is not None:
        if st.button('Extract Images', key = "images_button"):
            # Extract images from the uploaded PDF file
            images = extract_images_from_pdf(uploaded_file)

            if images:
                st.write(f"Extracted {len(images)} images:")
                for i, img in enumerate(images):
                    st.image(img, caption=f"Image {i+1}")
            else:
                st.write("No images found in the file.")


from transformers import BartTokenizer, BartForConditionalGeneration

# Load the tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

# Function to summarize text using BART
def summarize_text(max_length=150):
    uploaded_file = st.file_uploader("Select a file", type=["pdf", "docx", "txt"], key = "for_ext")
    if uploaded_file is not None:
        raw = parser.from_file(uploaded_file)
        text = raw['content'].strip()
        if st.button('Summarize', key = "summ_button"):
            inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model.generate(inputs, max_length=max_length, min_length=50, length_penalty=1.5, num_beams=6, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            st.text_area("Summary:", summary, height=200)

import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')


# Function to extract entities using spaCy
def extract_entities():
    uploaded_file = st.file_uploader("Select a file", type=["pdf", "docx", "txt"], key = "for_ext")
    if uploaded_file is not None:
        if st.button("Extract Entities", key = "ent_button"):
            raw = parser.from_file(uploaded_file)
            text = raw['content'].strip()
            doc = nlp(text)
            
            # Use dictionaries to handle case-insensitive uniqueness
            entities = {
                'Characters': {},
                'Places': {},
                'Organizations': {}
            }
            
            # Extract entities from the text
            for ent in doc.ents:
                # Normalize entity text to lowercase for case-insensitive comparison
                entity_text = ent.text.strip().lower()
                
                if ent.label_ == 'PERSON':
                    entities['Characters'][entity_text] = ent.text
                elif ent.label_ == 'GPE' or ent.label_ == 'LOC':
                    entities['Places'][entity_text] = ent.text
                elif ent.label_ == 'ORG':
                    entities['Organizations'][entity_text] = ent.text
            
            # Convert to sorted lists with capitalized text
            entities['Characters'] = sorted(set([v.capitalize() for v in entities['Characters'].values()]))
            entities['Places'] = sorted(set([v.capitalize() for v in entities['Places'].values()]))
            entities['Organizations'] = sorted(set([v.capitalize() for v in entities['Organizations'].values()]))
            
            st.write("### Extracted Entities")
            for entity_type, entity_list in entities.items():
                if entity_list:  # Only display if there are entities in the category
                    st.write(f"**{entity_type}:**")
                    st.write(entity_list)  # Display as a list
