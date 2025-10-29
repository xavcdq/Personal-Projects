# Personal Projects

## 1. Airbnb Availability & Revenue Optimisation - Power BI Project
This project explores the Airbnb listings dataset in New York with the goal of reducing availability to indirectly increase host revenue in under-performing districts. Using Power BI, I analysed availability patterns and built a scenario-based What-If analysis to simulate changes in price and review quality. 
The objective is to identify strategies to reduce excess listing availability - particularly in the two districts with the highest number of available units (Staten Island and Bronx) - by adjusting controllable levers such as price and 5-star review count.

## 2. Spotify & YouTube Music Analytics - Streamlit Web App (app.py)
This project uses a combined Spotify and YouTube dataset to build an interactive Streamlit application that enables users to explore songs, artists, and albums through multiple analytical views. The app funcions as a self-service analytics tool for music data, enabling users to gain insights, compare musical engagement across platforms, and explore track-level details through a clean interactive interface.

## 3. Document & Media Intelligence Platform - Streamlit + Tika App (user.py)
This project is a multi-feature Streamlit application with secure login that integrates Apache Tika, computer vision, NLP, and media recognition tools to perform various file and data extraction tasks in a singale interface. The purpose of this application is to consolidate multiple document processing and recognition tasks into one secure web interface, enabling users to extract information from files, perform analytics, and run recognition models without writing code. 

### Authentication Layer
- Login page (user + password)
- User Registration page
- Forgot password page with password reset flow
- Role-based access (Moderator vs User)

### Application Modules
- File Extraction: Extract full text, embedded images, summarise documents, and extract name entities from uploaded files (main3.py)
- Image Recognition: Predict the object/animal present in an uploaded image (classi.py)
- Table Converter: Detect tables in PDFs and export them to editable Excel files (table.py)
- Car Plate Recognition: Identify license plate numbers from uploaded images (carplate.py)
- Regex Generator: DIsplay predefined regular expression samples with descriptions (reg.py)
- Song Recognition: Identify songs from uploaded audio files (audio.py)
- User Database (Moderator-only): View all registered users and export database to Excel

