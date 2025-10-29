import streamlit as st
import PyPDF2

def read_pdf(file, password=None):
    pdf_reader = PyPDF2.PdfReader(file)
    
    if pdf_reader.is_encrypted:
        if password:
            try:
                pdf_reader.decrypt(password)
            except PyPDF2.errors.WrongPasswordError:
                return "The password you entered is incorrect. Please check and try again."
            except PyPDF2.errors.DecryptionError:
                return "Failed to decrypt the PDF. It might be encrypted with an unsupported method."
            except Exception as e:
                return f"Error decrypting PDF: {str(e)}"
        else:
            return "PDF is encrypted. Please provide a password."
    
    # Extract text from the PDF
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

st.title("Password-Protected PDF Reader")

# File uploader for the PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        
        if pdf_reader.is_encrypted:
            password = st.text_input("Enter the password for the PDF", type="password")
            if password:
                pdf_text = read_pdf(uploaded_file, password)
                st.text_area("PDF Content", pdf_text, height=400)
            else:
                st.warning("Please enter the password to read the PDF.")
        else:
            pdf_text = read_pdf(uploaded_file)
            st.text_area("PDF Content", pdf_text, height=400)
    
    except PyPDF2.errors.FileNotDecryptedError:
        st.error("The file could not be decrypted. Please check if the password is correct or if the PDF is encrypted with an unsupported method.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
