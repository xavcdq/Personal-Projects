import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# Function to hash passwords and security answers
def hash_text(text):
    return hashlib.sha256(str.encode(text)).hexdigest()

def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create the table with the correct schema
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            role TEXT,
            password TEXT,
            security_question_1 TEXT,
            security_answer_1 TEXT,
            security_question_2 TEXT,
            security_answer_2 TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user to the database
def add_user(first_name, last_name, username, email, role, password, 
             security_question_1, security_answer_1, 
             security_question_2, security_answer_2):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (first_name, last_name, username, email, role, password, 
        security_question_1, security_answer_1, security_question_2, security_answer_2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, username, email, role, hash_text(password), 
          security_question_1, hash_text(security_answer_1),
          security_question_2, hash_text(security_answer_2)))
    conn.commit()
    conn.close()

# Function to check login and retrieve user details
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT first_name, last_name, username, role FROM users WHERE username = ? AND password = ?', 
              (username, hash_text(password)))
    user = c.fetchone()
    conn.close()
    return user

# Function to check if email exists
def email_exists(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT email FROM users WHERE email = ?', (email,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

# Function to verify security answers
def verify_security_answers(email, answer_1, answer_2):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT security_answer_1, security_answer_2 FROM users WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    if row:
        hashed_answer_1, hashed_answer_2 = row
        return hash_text(answer_1.lower()) == hashed_answer_1 and hash_text(answer_2.lower()) == hashed_answer_2
    return False

# Function to update password
def update_password(email, new_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET password = ? WHERE email = ?', 
              (hash_text(new_password), email))
    conn.commit()
    conn.close()


# Function to view all users (moderator-only access)
def view_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT first_name, last_name, username, email, role, password FROM users')
    users = c.fetchall()
    conn.close()
    return users

# Function to display users in a table format (for moderators)
def display_users():
    st.subheader("Registered Users")
    users = view_all_users()

    if users:
        # Convert the fetched data to a pandas DataFrame for better handling
        df = pd.DataFrame(users, columns=['First Name', 'Last Name', 'Username', 'Email', 'Role', 'Password'])
        df.index = df.index + 1  # Adjust the index to start from 1
        st.table(df)  # This will display the data with headers

        # Convert user data to CSV
        csv = df.to_csv(index=False).encode('utf-8')

        # Add a button to download the user database as a CSV file
        st.download_button(
            label="Download Table",
            data=csv,
            file_name='user_database.csv',
            mime='text/csv'
        )
    else:
        st.info("No users registered yet.")

def application_page():
    st.title("Application Page")

    functions = ["File Extraction", "Image Recognition", "Table Converter", "Car Plate Recognition", "RegEx Generator", "Song Recognition"]
    if st.session_state['role'] == "moderator":
        functions.append("User Database")

    # Unique key for function selectbox
    selected_function = st.selectbox("Select Function", functions, key="function_select")

    if selected_function == "File Extraction":
        # Create a dropdown to select the page with a unique key
        app = ["Extraction", "Images", "Summary", "Entities"]
        page = st.selectbox("Select a page:", app, key="page_select")

        if page == "Extraction":
            from main3 import extraction
            extraction()
                
        elif page == "Images":
            from main3 import main
            main()

        elif page == "Summary":
            from main3 import summarize_text
            summarize_text()

        elif page == "Entities":
            from main3 import extract_entities
            extract_entities()
                
    elif selected_function == "Image Recognition":
        from classi import predict
        predict()
    
    elif selected_function == "Table Converter":
        from table import table
        table()
    elif selected_function == "Car Plate Recognition":
        from carplate import main
        main()
    elif selected_function == "RegEx Generator":
        from reg import regex
        regex()
    elif selected_function == "Song Recognition":
        from audio import song
        song()
    elif selected_function == "User Database":
        display_users()


    # Ensure the sign-out button has a unique key
    if st.button("Sign Out", key="sign_out"):
        st.session_state.clear()  # Clear session state on sign out
        st.query_params.clear()  # Clear query parameters to refresh the page



# Registration page function
def registration_page():
    st.title("Create an Account")

    role = st.selectbox("Role", ["user", "moderator"])
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Define the list of security questions
    questions = ["What is your favorite food?", "What is your favorite color?", "What is the name of your first pet?"]

    # Initialize session state if not already set
    if 'security_question_1' not in st.session_state:
        st.session_state.security_question_1 = questions[0]
    if 'security_question_2' not in st.session_state:
        st.session_state.security_question_2 = questions[1]

    # Security Question 1 Dropdown
    st.session_state.security_question_1 = st.selectbox(
        "Security Question 1", 
        questions, 
        index=questions.index(st.session_state.security_question_1),
        on_change=lambda: st.session_state.update({'security_question_2': next(q for q in questions if q != st.session_state.security_question_1)})
    )

    # Update options for Security Question 2 based on the selection in Security Question 1
    available_questions = [q for q in questions if q != st.session_state.security_question_1]

    # Security Question 1 Answer
    security_answer_1 = st.text_input("Answer to Security Question 1")

    # Security Question 2 Dropdown
    st.session_state.security_question_2 = st.selectbox(
        "Security Question 2",
        available_questions,
        index=available_questions.index(st.session_state.security_question_2) if st.session_state.security_question_2 in available_questions else 0
    )

    # Security Question 2 Answer
    security_answer_2 = st.text_input("Answer to Security Question 2")

    if role == "moderator":
        verification_code = st.text_input("Verification Code", type="password")

    if st.button("Register"):
        # Check if all fields are filled
        if not all([first_name, last_name, username, email, password, confirm_password, security_answer_1, security_answer_2]):
            st.error("All fields are required.")
        elif role == "moderator" and verification_code != "12345678":
            st.error("Invalid verification code for moderator registration.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                add_user(first_name, last_name, username, email, role, password, st.session_state.security_question_1, security_answer_1, st.session_state.security_question_2, security_answer_2)
                st.success("You have successfully registered!")
                st.info("Go to the Login Menu to login")
            except sqlite3.IntegrityError:
                st.error("Username or email already exists. Please choose a different username or email.")
                
    return_to_home_button()

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send the verification code via email
def send_verification_email(to_email, verification_code):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'xavcdq@gmail.com'
    smtp_password = 'szii aqas oiue jrxh'
    
    subject = 'Password Reset Verification Code'
    body = f'''
    Dear User,

    You requested to reset your password. Please use the following verification code:

    {verification_code}

    If you did not request this change, please ignore this email.

    Best regards,
    Your Team
    '''

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def return_to_home_button():
    if st.button("Return to Home"):
        st.session_state['page'] = 'home'
        st.query_params.update({'page': 'home'})

def forgot_password_page():
    st.title("Forgot Password")

    if 'submitted_email' not in st.session_state:
        st.session_state.submitted_email = False
    if 'submitted_answers' not in st.session_state:
        st.session_state.submitted_answers = False

    if not st.session_state.submitted_email:
        with st.form(key='email_form'):
            email = st.text_input("Enter your email")
            submit_email = st.form_submit_button("Submit")

        if submit_email:
            if email and email_exists(email):
                st.session_state.submitted_email = True
                st.session_state.email = email
                st.success("Email found. Please answer the security questions.")
                
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                c.execute('SELECT security_question_1, security_question_2 FROM users WHERE email = ?', (email,))
                questions = c.fetchone()
                conn.close()

                if questions:
                    st.session_state.security_questions = questions
            else:
                st.error("Email does not exist.")
    else:
        if not st.session_state.submitted_answers:
            security_question_1, security_question_2 = st.session_state.security_questions
            
            with st.form(key='security_questions_form'):
                st.text(f"Security Question 1: {security_question_1}")
                answer_1 = st.text_input("Answer to Security Question 1", key='answer1')

                st.text(f"Security Question 2: {security_question_2}")
                answer_2 = st.text_input("Answer to Security Question 2", key='answer2')
                
                submit_answers = st.form_submit_button("Submit Answers")

            if submit_answers:
                if verify_security_answers(st.session_state.email, answer_1, answer_2):
                    verification_code = str(random.randint(1000, 9999))
                    
                    if send_verification_email(st.session_state.email, verification_code):
                        st.success("A verification code has been sent to your email. Please check your email to proceed.")
                        st.session_state.verification_code = verification_code
                        st.session_state.reset_email = st.session_state.email
                        st.session_state.page = 'verify_code'
                        st.query_params.update({'page': 'verify_code'})
                    else:
                        st.error("Failed to send verification code.")
                else:
                    st.error("Security answers do not match.")
    
    return_to_home_button()

def verify_code_page():
    st.title("Verify Code")

    # Input for verification code
    verification_code_input = st.text_input("Enter the verification code sent to your email")

    if st.button("Verify Code"):
        if verification_code_input == st.session_state.get('verification_code'):
            st.session_state['page'] = 'reset_password'
            st.query_params.update({'page': 'reset_password'})
        else:
            st.error("Invalid verification code.")

    if st.button("Return to Home"):
        st.session_state['page'] = 'home'
        st.query_params.update({'page': 'home'})

# Reset Password page function
def reset_password_page():
    st.title("Reset Password")

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if not all([new_password, confirm_password]):
            st.error("Both password fields are required.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            update_password(st.session_state['reset_email'], new_password)
            st.success("Password updated successfully!")
            st.session_state['page'] = 'home'
            st.query_params.update({'page': 'home'})

    if st.button("Return to Home"):
        st.session_state['page'] = 'home'
        st.query_params.update({'page': 'home'})

# Home page (Login) function
def home_page():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state['username'] = user[2]  # Save username in session state
            st.session_state['role'] = user[3]  # Save role in session state
            st.session_state['user_details'] = user  # Save user details (first_name, last_name)
            st.session_state['page'] = 'application'  # Redirect to the application page
            st.query_params.update({'page': 'application'})
        else:
            st.error("Invalid Username or Password")
    
    if st.button("Register"):
        st.session_state['page'] = 'register'
        st.query_params.update({'page': 'register'})

    if st.button("Forgot Password"):
        st.session_state['page'] = 'forgot_password'
        st.query_params.update({'page': 'forgot_password'})

def main():
    create_users_table()

    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    if st.query_params.get('page') == 'forgot_password':
        forgot_password_page()
    elif st.query_params.get('page') == 'verify_code':
        verify_code_page()
    elif st.query_params.get('page') == 'reset_password':
        reset_password_page()
    elif st.query_params.get('page') == 'register':
        registration_page()
    elif st.query_params.get('page') == 'application':
        application_page()
    else:
        home_page()

if __name__ == '__main__':
    main()
