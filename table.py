import streamlit as st
import pandas as pd
import tabula.io as tabula_io
import io


def table():
    # Create a file uploader
    uploaded_file = st.file_uploader("Select a PDF file:", type=["pdf"])

    # Create a button to trigger the conversion
    if st.button("Convert to CSV"):
        if uploaded_file is not None:
            # Read the PDF into a list of DataFrames
            dfs = tabula_io.read_pdf(uploaded_file, pages='all')

            # Preview the content
            for i, df in enumerate(dfs):
                st.write(f"Table {i+1}:")
                st.dataframe(df)  # or st.table(df) for a static table

                # Create a download button for each table
                buffer = io.StringIO()
                df.to_csv(buffer, index=False)
                buffer.seek(0)
                st.download_button(
                    label=f"Download Table {i+1}",
                    data=buffer.getvalue(),
                    file_name=f"table_{i+1}.csv",
                    mime="text/csv"
                )
        else:
            st.write("Please select a PDF file to convert.")