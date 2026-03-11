import streamlit as st
import os
import mimetypes

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
            
            # Create a layout to display file name, view button, and download button side-by-side
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"📄 **{file}**")
            
            with col2:
                # Add a unique key for the view button
                view_button = st.button("View", key=f"view_{file}")
            
            with col3:
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Download",
                        data=f,
                        file_name=file,
                        mime="application/octet-stream",
                        key=f"download_{file}"
                    )
            
            if view_button:
                st.subheader(f"Preview: {file}")
                mime_type, _ = mimetypes.guess_type(file_path)
                
                if mime_type:
                    if mime_type.startswith('image'):
                        st.image(file_path)
                    elif mime_type.startswith('audio'):
                        st.audio(file_path)
                    elif mime_type.startswith('video'):
                        st.video(file_path)
                    elif mime_type.startswith('text') or file.endswith(('.py', '.md', '.csv', '.json')):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                st.text(f.read())
                        except Exception as e:
                            st.error(f"Could not read text file: {e}")
                    elif mime_type == 'application/pdf':
                        # For PDF viewing, you can use an iframe if encoded to base64
                        import base64
                        with open(file_path, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                    else:
                        st.warning("Preview not available for this file type. Please download to view.")
                else:
                    # Fallback for text if no mime type is found
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            st.text(f.read())
                    except:
                        st.warning("Preview not available for this file type. Please download to view.")
            
            st.divider()
