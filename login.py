import streamlit as st

# Function to check if the user is logged in
def is_user_authenticated():
    return "is_authenticated" in st.session_state and st.session_state.is_authenticated

# Login page
def login():
    st.title("Login Page")

    # Create a username input
    username = st.text_input("Username")

    # Create a password input with the `type` parameter set to password
    password = st.text_input("Password", type="password")

    # Check if the login button is pressed
    if st.button("Login"):
        # Hardcoded username and password for demonstration purposes
        if username == "demo" and password == "demo123":
            st.session_state.is_authenticated = True
            st.success("Login Successful!")
            # Redirect to another page after successful login
            st.experimental_rerun()
        else:
            st.error("Invalid username or password. Please try again.")
