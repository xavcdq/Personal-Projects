import streamlit as st

def regex():
    # Dictionary of regex samples
    regex_samples = {
        "Email": r"(?:[a-zA-Z0-9._%+-]+)@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}",
        "NRIC": r"(?i)(S|T|F|G)\d{7}[A-Z]",  # Added NRIC regex sample
        "Websites": r"^(https?|ftp):\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/[a-zA-Z0-9#?=&.-]*)?$",  # Added Website regex sample
        "Phone Number": r"^\+65\d{8}$",
    }

    # Dropdown to select a regex sample
    selected_sample = st.selectbox("Select a RegEx sample", list(regex_samples.keys()))

    # Display the selected regex
    st.write("Generated Regular Expression:")
    st.code(regex_samples[selected_sample], language="regex")

    st.write("Explanation:")
    # Display explanations for the selected regex
    if selected_sample == "Email":
        st.write("""
        - **^**: Asserts the start of a line.
        - **(?i)**: Enables case-insensitive matching.
        - **[a-z0-9._%+-]+**: Matches one or more occurrences of lowercase letters, digits, and special characters like period (.), underscore (_), percent (%), plus (+), and hyphen (-) before the '@' symbol.
        - **@**: Matches the '@' symbol literally.
        - **[a-z0-9.-]+**: Matches one or more occurrences of lowercase letters, digits, period (.), and hyphen (-) after the '@' symbol.
        - **\\.**: Matches a period (.) literally.
        - **[a-z]{2,}**: Matches two or more lowercase letters after the period, ensuring a valid top-level domain (TLD).
        - **$**: Asserts the end of a line.
                
        This regular expression pattern is designed to validate email addresses by checking for a specific pattern commonly found in email addresses.
        """)
    elif selected_sample == "NRIC":
        st.write("""
        - **(?i)**: Enables case-insensitive matching.
        - **(S|T|F|G)**: Matches the first letter of the NRIC, which can be 'S', 'T', 'F', or 'G'.
        - **\\d{7}**: Matches exactly seven digits.
        - **[A-Z]**: Matches a single uppercase letter, which is the checksum letter at the end of the NRIC.
        
        Therefore, this regular expression will match strings that start with either 'S', 'T', 'F', or 'G', followed by 7 digits, and ending with an uppercase letter.
        """)
    elif selected_sample == "Websites":
        st.write("""
        - **^**: Asserts the start of a line.
        - **(https?|ftp)**: Matches either "http", "https", or "ftp". "http" is followed by an optional "s", making it "http" or "https".
        - **:\\/\\/**: Matches "://" literally.
        - **[a-zA-Z0-9.-]+**: Matches one or more occurrences of alphabets, digits, dots, or hyphens.
        - **\\.**: Matches a dot.
        - **[a-zA-Z]{2,}**: Matches two or more occurrences of alphabets.
        - **(\\/[^ ]*)?$**: Optionally matches a forward slash (\/) followed by any combination of alphabets, digits, #, ?, =, &, dots, or hyphens.
        - **$**: Asserts the end of a line.
        
        This regular expression is designed to match URLs starting with "http", "https", or "ftp", followed by a domain name and an optional path.
        """)
    elif selected_sample == "Phone Number":
        st.write("""
        - **^**: Indicates the start of the string.
        - **\\+65**: Matches the country code for Singapore, which is "+65".
        - **\\d{8}**: Matches any digit exactly 8 times.
        - **$**: Indicates the end of the string.
        
        Therefore, the regular expression **^\\+65\\d{8}$** will match strings that start with "+65" (the country code for Singapore) followed by 8 digits, ensuring that it represents a Singapore handphone number.
        """)

    # Add the link to more information about regular expressions
    st.markdown(
        'To find out more about regular expressions, visit this [website](https://regex-generator-lyzr.streamlit.app/).'
    )
