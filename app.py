import streamlit as st
import os

st.set_page_config(page_title="File Share App", page_icon="📁", layout="centered")

st.title("📁 File Upload & View App")

# Create an uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Options
option = st.sidebar.radio("Select an option", ("Upload File", "View Files"))

if option == "Upload File":
    st.header("Upload a File")
    # Using accept_multiple_files=False for simplicity, though it's the default
    uploaded_file = st.file_uploader("Choose a file")
    
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' saved successfully! You can now access it from the 'View Files' tab.")
        
elif option == "View Files":
    st.header("View and Download Files")
    files = os.listdir(UPLOAD_DIR)
    
    if len(files) == 0:
        st.info("No files uploaded yet.")
    else:
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file)
            
            # Create a simple layout to display file name and a download button side-by-side
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📄 **{file}**")
            with col2:
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Download",
                        data=f,
                        file_name=file,
                        mime="application/octet-stream",
                        key=f"download_{file}"
                    )