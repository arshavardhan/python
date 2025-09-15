import streamlit as st
import random
import string
import os
import sqlite3
import psutil  # For system performance metrics
import datetime
import plotly.express as px  
import pandas as pd
import io

# Database connection function
def create_connection():
    conn = sqlite3.connect("database.db")
    return conn

# Function to create tables for users, issues, and settings
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    # User table with default status column
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'Approved'
        )
    ''')
    # Issues table with timestamp and default status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            issue TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Settings table for site status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settingss (
            role TEXT PRIMARY KEY,
            site_status TEXT DEFAULT 'Operational'
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        feedback_text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    cursor.execute('''

    CREATE TABLE  IF NOT EXISTS  employee_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_content BLOB NOT NULL,
    topic TEXT NOT NULL,
    subtopic TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()



# Function to add a user with default status "Approved"
def add_user(username, role):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM user WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        st.error("Username already exists. Please choose a different username.")
        conn.close()
        return
    
    password = generate_password()
    cursor.execute("INSERT INTO user (username, password, role, status) VALUES (?, ?, ?, 'Approved')", (username, password, role))
    conn.commit()
    user_id = cursor.lastrowid
    st.success(f"User '{username}' added with password: '{password}', ID: {user_id}.")
    conn.close()

# Function to delete a user by ID
def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id=?", (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        st.error(f"No user found with ID '{user_id}'.")
    else:
        st.success(f"User with ID '{user_id}' deleted.")
    conn.close()

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to validate user login and check if account status is approved
def validate_user(username, password, role):
    conn = create_connection()
    cursor = conn.cursor()
    
    # Query to fetch user details based on username and role
    cursor.execute("SELECT * FROM user WHERE username=? AND role=?", (username, role))
    user = cursor.fetchone()
    conn.close()
    
    # Check if user exists
    if user:
        stored_password = user[2]  # Assuming user[2] contains the stored password
        if user[4] == "Approved" and stored_password == password:  # Check the stored password
            return True  # User is approved and login is successful
        elif user[4] == "Blocked":
            st.error("Your account is blocked. Please contact the administrator.")
    else:
        st.error("Invalid username or password or role.")  # Handle invalid credentials

    return False  # Default return for failed login attempts

def submit_feedback(user_id, feedback):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (user_id, feedback_text) VALUES (?, ?)", (user_id, feedback))
    conn.commit()
    conn.close()
# Function to change user status
def change_user_status(user_id, new_status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET status=? WHERE id=?", (new_status, user_id))
    conn.commit()
    if cursor.rowcount == 0:
        st.error(f"No user found with ID '{user_id}'.")
    else:
        st.success(f"User with ID '{user_id}' status changed to '{new_status}'.")
    conn.close()

# Function to submit a new issue
def submit_issue(username, issue):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO issues (username, issue) VALUES (?, ?)", (username, issue))
    conn.commit()
    st.success("Issue submitted successfully.")
    conn.close()

def submit_issue(username, issue):
    conn = create_connection()
    cursor = conn.cursor()
    # Insert issue into the issues table
    try:
        cursor.execute("""
            INSERT INTO issues (username, issue ) 
            VALUES (?, ?)
        """, (username, issue))
        
        # Commit the transaction
        conn.commit()
        st.info("Issue successfully inserted into the issues table.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        
    finally:
        conn.close()
# Function to fetch all issues for the administrator
def fetch_issues():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM issues ORDER BY created_at DESC")
    issues = cursor.fetchall()
    conn.close()
    return issues

# Function to update issue status
def update_issue_status(issue_id, new_status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE issues SET status=? WHERE id=?", (new_status, issue_id))
    conn.commit()
    if cursor.rowcount == 0:
        st.error(f"No issue found with ID '{issue_id}'.")
    else:
        st.success(f"Issue ID '{issue_id}' status changed to '{new_status}'.")
    conn.close()

# Function to initialize settings for Employee and Trainer roles
def initialize_settings():
    conn = create_connection()
    cursor = conn.cursor()
    for role in ["Employee", "Trainer"]:
        cursor.execute("INSERT OR IGNORE INTO settingss (role, site_status) VALUES (?, 'Operational')", (role,))
    conn.commit()
    conn.close()

# Fetch current site status for a specific role
def fetch_site_status(role):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT site_status FROM settingss WHERE role = ?", (role,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Operational"

# Function to get the total number of users
def get_total_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    total_users = cursor.fetchone()[0]
    conn.close()
    return total_users

# Function to get the total number of issues
def get_total_issues():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM issues")
    total_issues = cursor.fetchone()[0]
    conn.close()
    return total_issues

# Update site status for a specific role
def update_site_status(role, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE settingss SET site_status = ? WHERE role = ?", (status, role))
    conn.commit()
    conn.close()

# Dashboard redirection based on site status
def role_dashboard(role):
    site_status = fetch_site_status(role)
    if site_status == "Under Maintenance":
        st.warning(f"The {role} section is currently under maintenance.")
    elif role == "Administrator":
        admin_dashboard()
    elif role == "Trainer":
        trainer_dashboard()
    elif role == "Employee":
        employee_dashboard(st.session_state.username)
  

def reporting_dashboard():
    
    st.subheader("Reporting Module")
    total_users = get_total_users()
    total_issues = get_total_issues()

    data = {'Category': ['Total Users', 'Total Issues'], 'Count': [total_users, total_issues]}
    df = pd.DataFrame(data)

    fig = px.pie(df, values='Count', names='Category', title='Users and Issues Distribution')
    st.plotly_chart(fig)

# Main Admin Dashboard
def admin_dashboard():
    st.sidebar.title("Admin Dashboard")
    main_option = st.sidebar.selectbox("Choose a module", [
        "User Management", "System Monitoring", "Reporting", "Issue Resolution", "Settings Management"
    ])

       # Adding human logo and username at the top right corner
    logo_url = "https://i.pinimg.com/564x/9e/5b/c0/9e5bc04372764479079dcbd8f0196318.jpg"  # Replace with your logo URL
    st.markdown(
        f"""
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <img src="{logo_url}" alt="User Logo" style="width: 40px; height: 40px; border-radius: 50%;">
            
        </div>
        """, unsafe_allow_html=True
    )

    
        

    if main_option == "User Management":
        user_management()
    elif main_option == "System Monitoring":
        system_monitoring()
    elif main_option == "Reporting":
        st.subheader("Reporting")
        if st.button("Generate Report"):
            reporting_dashboard()
    elif main_option == "Issue Resolution":
        issue_resolution()
    elif main_option == "Settings Management":
        settings_management()

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
      

# System monitoring function
def system_monitoring():
    st.subheader("System Monitoring")

    # Collect system metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    # Prepare data for the table
    metrics_data = {
        "Metric": ["CPU Usage", "Memory Usage", "Disk Usage"],
        "Value": [f"{cpu_usage}%", f"{memory_usage}%", f"{disk_usage}%"]
    }

    # Create a DataFrame for the metrics
    metrics_df = pd.DataFrame(metrics_data)

    # Display the metrics in a table
    st.table(metrics_df)
    st.write(f"Last login time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Login Page
def login_page():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Enter your username")
    password = st.sidebar.text_input("Enter your password", type='password')
    role = st.sidebar.selectbox("Select your role", ["Administrator", "Employee", "Trainer"])

    if st.sidebar.button("Login"):
        if not username or not password or not role:
            st.error("Please fill in all fields: username, password, and role.")
        elif validate_user(username, password, role):
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.logged_in = True
          
def distribute_file(file_id, file_content, topic, subtopic, timestamp):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO employee_files (file_name, file_content, topic, subtopic, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (f"{topic}_{subtopic}.csv", file_content, topic, subtopic, timestamp)
    )
    conn.commit()
    conn.close()
def display_and_distribute_question_banks():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Fetch generated files
    generated_files_df = fetch_generated_files()
    

    # Initialize an empty list to store selected IDs
    selected_ids = []
    
    # Loop over each row to add checkboxes for selection
    for index, row in generated_files_df.iterrows():
        # Checkbox for selecting the row
        if st.checkbox(f"Select ID: {row['id']} - Topic: {row['topic']}, Subtopic: {row['subtopic']}", key=f"checkbox_{index}"):
            selected_ids.append(row['id'])
    
    # Create a section for download and distribute buttons after selecting rows
    if selected_ids:
        st.write("### Actions for Selected Files")
        
        for selected_id in selected_ids:
            # Fetch the corresponding row data
            row = generated_files_df[generated_files_df['id'] == selected_id].iloc[0]
            
            # Prepare the file content for download
            file_data = row['file_data']  # Ensure this matches the correct column name for the CSV content
            
            # Create columns for buttons
            col1, col2 = st.columns(2)

            # Download button
            with col1:
                st.download_button(
                    label="Download CSV",
                    data=file_data,
                    file_name=f"{row['topic']}_{row['subtopic']}.csv",
                    mime="text/csv"
                )

            # Distribute button
            with col2:
                if st.button("Distribute", key=f"distribute_{selected_id}"):
                    try:
                        distribute_file(row['id'], file_data, row['topic'], row['subtopic'], row['timestamp'])
                        st.success(f"File '{row['topic']}_{row['subtopic']}.csv' distributed successfully.")
                    except Exception as e:
                        st.error(f"An error occurred while distributing the file: {e}")









# User Management Function
def user_management():
    action = st.selectbox("Select an action", ["Add User", "Delete User", "Permission Access Control"])

    if action == "Add User":
        username = st.text_input("Enter username")
        role = st.selectbox("Select role", ["Employee", "Trainer"])
        if st.button("Add User"):
            if username:
                add_user(username, role)
            else:
                st.error("Please enter a username.")

    elif action == "Delete User":
        user_id_to_delete = st.text_input("Enter user ID to delete")
        if st.button("Delete User") and user_id_to_delete:
            try:
                delete_user(int(user_id_to_delete))
            except ValueError:
                st.error("Please enter a valid user ID.")

    elif action == "Permission Access Control":
        # Fetch all users
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, status FROM user WHERE role IN ('Employee', 'Trainer')")
        users = cursor.fetchall()
        conn.close()

        if users:
            # Create a dropdown for selecting users
            user_options = [f"{user[1]} (ID: {user[0]}) - Status: {user[2]}" for user in users]
            selected_user = st.selectbox("Select a user to manage", user_options)

            # Get the selected user's ID and current status
            selected_user_id = int(selected_user.split(" (ID: ")[1].split(")")[0])
            current_status = next(user[2] for user in users if user[0] == selected_user_id)

            # Display current status and provide options to change status
            st.write(f"Current Status: {current_status}")
            new_status = st.selectbox("Change Status", ["Approved", "Blocked"], index=0 if current_status == "Approved" else 1)

            if st.button("Update Status"):
                change_user_status(selected_user_id, new_status)

# Question Bank Generation Model Code
from langchain_google_genai import GoogleGenerativeAI

def generate_questions(topic, subtopic, difficulty, num_questions):
    """
    Generates questions based on topic, subtopic, difficulty, and number of questions.

    Parameters:
    - topic (str): The main topic for question generation.
    - subtopic (str): The subtopic within the main topic.
    - difficulty (str): Difficulty level (Easy, Medium, Hard).
    - num_questions (int): Number of questions to generate.

    Returns:
    - list: A list of generated questions.
    """
    api_key = "AIzaSyD8NPCi9lmN6PayjGNuH2D4DewkKmFzvuY"  # Replace with your actual API key
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=1.0)
    questions = []

    for i in range(num_questions):
        prompt = f"Generate a {difficulty.lower()} question on {topic} with a focus on {subtopic}."

        try:
            response = llm.generate([prompt])
            if response and len(response.generations) > 0:
                question = response.generations[0][0].text.strip()
                questions.append({"Question": question})
            else:
                questions.append({"Question": "No question generated."})
        except Exception as e:
            questions.append({"Question": f"Error generating question: {e}"})

    return questions
def get_feedback():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
def load_topics():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT DISTINCT topic FROM generated_files"
    topics = pd.read_sql_query(query, conn)
    conn.close()
    return topics

def load_self_data(topic):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT file_data FROM generated_files WHERE topic = '{topic}'"
    self_data_df = pd.read_sql_query(query, conn)
    
    # Convert BLOB to string (assuming the BLOB contains UTF-8 encoded text)
    self_data_df['file_data'] = self_data_df['file_data'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
    
    conn.close()
    return self_data_df
def get_file_data():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM generated_files"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def fetch_generated_files():
    conn = create_connection()
    cursor = conn.cursor()
    df = pd.read_sql_query("SELECT id, topic, subtopic, file_data, timestamp FROM generated_files", conn)
    conn.close()
    return df
def get_employee_files():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, topic, subtopic, file_content, timestamp FROM employee_files ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
import requests
     # Replace with your actual API URL

# Function to create a downloadable file
def create_downloadable_file(file_content, filename):
    return io.BytesIO(file_content)
# Function to update the generated file in the database
def update_generated_file(file_id, updated_file_data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE generated_files
        SET file_data = ?
        WHERE id = ?
    ''', (updated_file_data, file_id))
    conn.commit()
    conn.close()


def save_file_to_database(topic, subtopic, file_data):
    conn = create_connection()
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generated_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            subtopic TEXT,
            file_data BLOB,
            timestamp TEXT
        )
    ''')

    # Insert the generated file with topic, subtopic, and timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO generated_files (topic, subtopic, file_data, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (topic, subtopic, file_data, timestamp))

    conn.commit()
    conn.close()

def convert_file_data_to_df(file_data):
    return pd.read_csv(io.BytesIO(file_data))


def trainer_dashboard():
    # Check if the user is logged in
    if st.session_state.get("logged_in", False):
        st.sidebar.title("Trainer Dashboard")
        
        main_option = st.sidebar.selectbox("Choose a module", [
            "Question Bank Generation", "Review and Edit", "Download and Distribute", "Feedback Collection","Issue Submission"
        ])

        # Header and Logo
        logo_url = "https://i.pinimg.com/564x/9e/5b/c0/9e5bc04372764479079dcbd8f0196318.jpg"  # Replace with your logo URL
        st.markdown(
            f"""
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <img src="{logo_url}" alt="User Logo" style="width: 40px; height: 40px; border-radius: 50%;">
            </div>
            """, unsafe_allow_html=True
        )

       # Question Bank Generation in Streamlit
    if main_option == "Question Bank Generation":
        st.subheader("Question Bank Generation")
        topic = st.text_input("Enter Topic:")
        subtopic = st.text_input("Enter Subtopic:")
        difficulty_level = st.selectbox("Select Difficulty Level:", ["Easy", "Medium", "Hard"])
        num_questions = st.number_input("Number of Questions:", min_value=1, max_value=100)
        if st.button("Generate Question Bank"):
            if topic and subtopic:
                questions = generate_questions(topic, subtopic, difficulty_level, num_questions)
                df = pd.DataFrame(questions, columns=["Question"])
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                save_file_to_database(topic, subtopic, csv)
                st.success(f"Generated and saved question file for Topic: {topic}, Subtopic: {subtopic}.")
                st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f'{topic}_{subtopic}_questions.csv',
                mime='text/csv'
                )
            else:
                st.warning("Please enter both topic and subtopic.")


        # Review and Edit
    elif main_option == "Review and Edit":
        st.subheader("Review and Edit Question Banks")
        generated_files_df = fetch_generated_files()
        if generated_files_df.empty:
            st.warning("No generated files found in the database. Please ensure that files are generated and stored before trying to review and edit.")
            st.info("You can generate new question banks from the 'Generate Questions' section.")
        else:
            st.dataframe(generated_files_df[['id', 'topic', 'subtopic', 'timestamp']])
            file_id = st.selectbox("Select a File ID to Edit:", generated_files_df['id'].tolist())
            selected_file = generated_files_df[generated_files_df['id'] == file_id].iloc[0]
            topic = selected_file['topic']
            subtopic = selected_file['subtopic']
            file_data = selected_file['file_data']
            df_to_edit = convert_file_data_to_df(file_data)
            csv_content = df_to_edit.to_csv(index=False)
            edited_csv_content = st.text_area("Edit the CSV content:", value=csv_content, height=300)
        if st.button("Save Changes"):
            updated_df = pd.read_csv(io.StringIO(edited_csv_content))
            updated_csv = updated_df.to_csv(index=False).encode('utf-8')
            update_generated_file(file_id, updated_csv)
            st.success("The question bank has been updated successfully!")


        # Download and Distribute
    elif main_option == "Download and Distribute":
            st.subheader("Download and Distribute Question Banks")
            downloadable_banks = display_and_distribute_question_banks()  # Ensure this function is defined
            

        # Feedback Collection
    elif main_option == "Feedback Collection":
            st.subheader(" Feedback Collection")
            feedback_data = get_feedback()
            if feedback_data:
                feedback_df = pd.DataFrame(feedback_data, columns=["ID", "User ID", "Feedback", "Timestamp"])
                st.table(feedback_df)  # Display feedback in a table format
            else:
                st.info("No feedback available. Be the first to share your thoughts!")
    elif main_option == "Issue Submission":
        st.subheader("Issue Submission")
        username = st.text_input("Username")
        issue = st.text_area("Describe your issue")
        if st.button("Submit Issue"):
            if username and issue:
                submit_issue(username, issue)
                st.success("Issue submitted successfully.")
            else:
                st.error("Please provide both username and issue description.")
           
            

        # Logout button in the sidebar
    if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""


# Employee Dashboard Function
def employee_dashboard(username):
    if st.session_state.get("logged_in", False):
        st.sidebar.title("Employee Dashboard")
        
        main_option = st.sidebar.selectbox("Choose a module", [
            "Self-Assessment", "Feedback Submission", "Learning and Development","Issue Submission"
        ])

        # Header and Logo
        logo_url = "https://i.pinimg.com/564x/9e/5b/c0/9e5bc04372764479079dcbd8f0196318.jpg"  # Replace with your logo URL
        st.markdown(
            f"""
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <img src="{logo_url}" alt="User Logo" style="width: 40px; height: 40px; border-radius: 50%;">
            </div>
            """, unsafe_allow_html=True
        )

       # Question Bank Generation in Streamlit
    if main_option == "Self-Assessment":
        file_data_df = get_file_data()
        topics = file_data_df['topic'].unique()
        selected_topic = st.selectbox("Select Topic", topics)
        filtered_data_df = file_data_df[file_data_df['topic'] == selected_topic]
        user_answers = {}
        if selected_topic: 
            if not filtered_data_df.empty:
                for index, row in filtered_data_df.iterrows():
                    st.info(f"Subtopic: {row['subtopic']}")
                    st.text_area("File Data:", row['file_data'], height=200, key=row['id'])
                    answer = st.text_area("Your Answer:", key=f"answer_{row['id']}")
                    if st.button("Submit Answer", key=f"submit_{row['id']}"):
                        if answer:
                            user_answers[row['id']] = answer  # Store user answer using row ID
                            st.info("your assignment submitted successfully , Result will release soon...")
                        else:
                            st.warning("Please provide an answer before submitting.")
            else:
                st.info("No questions available for the selected topic.")



    elif main_option == "Feedback Submission":
        st.subheader("Feedback Submission")
        user_id = st.number_input("Enter your User ID:", min_value=1)  # Assuming user ID is a positive integer
        feedback_text = st.text_area("Write your feedback here:", height=150)
        if st.button("Submit Feedback"):
            if feedback_text:
                submit_feedback(user_id, feedback_text)
                st.success("Feedback submitted successfully!")
            else:
                st.warning("Please enter your feedback before submitting.")
       


        # Download and Distribute
    elif main_option == "Learning and Development":
            st.subheader("Learning and Development")
            employee_files = get_employee_files()
            if employee_files:
                files_df = pd.DataFrame(employee_files, columns=["ID", "Topic", "Subtopic", "File Content", "Timestamp"])
                topic_options = files_df["Topic"].unique()
                selected_topic = st.selectbox("Select a Topic", topic_options)
                subtopics_df = files_df[files_df["Topic"] == selected_topic]
                subtopic_options = subtopics_df["Subtopic"].unique()
                selected_subtopic = st.selectbox("Select a Subtopic", subtopic_options)
                filtered_files = subtopics_df[subtopics_df["Subtopic"] == selected_subtopic]
                for _, row in filtered_files.iterrows():
                    st.info(f"Topic: {row['Topic']} - Subtopic: {row['Subtopic']}")
                    st.write(f"Uploaded on: {row['Timestamp']}")
                    file_content = row["File Content"]
                    filename = f"{row['Topic']}_{row['Subtopic']}.csv"
                    downloadable_file = create_downloadable_file(file_content, filename)
                    st.download_button(
                        label="Download File",
                        data=downloadable_file,
                        file_name=filename,
                        mime="text/csv"
                        )
            else:
                st.info("No learning and development resources are currently available.")
    elif main_option == "Issue Submission":
        st.subheader("Issue Submission")
        username = st.text_input("Username")
        issue = st.text_area("Describe your issue")
        if st.button("Submit Issue"):
            if username and issue:
                submit_issue(username, issue)
                st.success("Issue submitted successfully.")
            else:
                st.error("Please provide both username and issue description.")
           
            

                
               
        



    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
           
def issue_resolution():
    st.subheader("Issue Resolution")
    issues = fetch_issues()
    if issues:
        issue_options = {f"ID: {issue[0]} | User: {issue[1]} | Status: {issue[3]} | {issue[2]}": issue for issue in issues}
        selected_issue = st.selectbox("Select Issue to Manage", list(issue_options.keys()))
        selected_issue_id = issue_options[selected_issue][0]
        new_status = st.selectbox("Select new issue status", ["Open", "Resolved", "In Progress"])
        if st.button("Change Issue Status"):
            update_issue_status(selected_issue_id, new_status)
    else:
        st.info("No issues found.")
# Settings Management Function
def settings_management():
    st.subheader("Settings Management")
    selected_role = st.selectbox("Select Role", ["Employee", "Trainer"])
    current_status = fetch_site_status(selected_role)

    st.write(f"Current site status for {selected_role}: {current_status}")

    if st.button("Change Status"):
        new_status = "Under Maintenance" if current_status == "Operational" else "Operational"
        update_site_status(selected_role, new_status)
        st.success(f"Site status for {selected_role} changed to '{new_status}'.")

# Main function to run the app
def main():
    create_tables()
    initialize_settings()

    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        role_dashboard(st.session_state.role)

if __name__ == "_main_":
    main()