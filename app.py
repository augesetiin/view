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
                _, ext = os.path.splitext(file)
                ext = ext.lower()

                # Map file extensions to language names for syntax highlighting
                LANG_MAP = {
                    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                    '.tsx': 'tsx', '.jsx': 'jsx', '.html': 'html', '.htm': 'html',
                    '.css': 'css', '.json': 'json', '.xml': 'xml', '.yaml': 'yaml',
                    '.yml': 'yaml', '.toml': 'toml', '.md': 'markdown',
                    '.csv': 'csv', '.sql': 'sql', '.sh': 'bash', '.bat': 'batch',
                    '.ps1': 'powershell', '.java': 'java', '.c': 'c', '.cpp': 'cpp',
                    '.h': 'c', '.hpp': 'cpp', '.cs': 'csharp', '.go': 'go',
                    '.rs': 'rust', '.rb': 'ruby', '.php': 'php', '.swift': 'swift',
                    '.kt': 'kotlin', '.dart': 'dart', '.lua': 'lua', '.r': 'r',
                    '.pl': 'perl', '.scala': 'scala', '.vue': 'html',
                    '.svelte': 'html', '.ini': 'ini', '.cfg': 'ini',
                    '.log': 'log', '.txt': 'text', '.env': 'bash',
                    '.gitignore': 'text', '.dockerignore': 'text',
                    '.dockerfile': 'dockerfile',
                }

                # Extensions that should be treated as readable text
                TEXT_EXTENSIONS = set(LANG_MAP.keys())

                # Check if file is a text-based file
                is_text_file = (
                    (mime_type and mime_type.startswith('text'))
                    or ext in TEXT_EXTENSIONS
                    or (mime_type and mime_type in (
                        'application/json', 'application/xml',
                        'application/javascript', 'application/x-yaml',
                        'application/x-sh', 'application/x-python',
                    ))
                )

                if mime_type and mime_type.startswith('image'):
                    st.image(file_path)
                elif mime_type and mime_type.startswith('audio'):
                    st.audio(file_path)
                elif mime_type and mime_type.startswith('video'):
                    st.video(file_path)
                elif mime_type and mime_type == 'application/pdf':
                    try:
                        from streamlit_pdf_viewer import pdf_viewer
                        st.markdown("### Preview")
                        st.caption("You can freely highlight and copy text directly from the document below.")
                        # render_text=True enables the text selection layer over the PDF
                        pdf_viewer(file_path, render_text=True)
                    except ImportError:
                        st.error("Please add 'streamlit-pdf-viewer' to your requirements.txt or install it using pip.")
                    except Exception as e:
                        st.error(f"Could not load PDF: {e}")
                elif is_text_file:
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                            content = f.read()
                        
                        # Use raw HTML <pre> block for pure browser-native selection and copying
                        html_content = f"""
                        <div style="
                            background-color: #1e1e1e;
                            color: #d4d4d4;
                            padding: 1rem;
                            border-radius: 0.5rem;
                            overflow-x: auto;
                            max-height: 500px;
                            overflow-y: auto;
                            font-family: monospace;
                            border: 1px solid #333;
                            user-select: text;
                        ">
                            <pre style="margin: 0; white-space: pre-wrap; word-wrap: break-word;">{content.replace('<', '&lt;').replace('>', '&gt;')}</pre>
                        </div>
                        """
                        st.markdown(html_content, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Could not read file: {e}")
                else:
                    # Try to read as text anyway before giving up
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="strict") as f:
                            content = f.read()
                        
                        html_content = f"""
                        <div style="
                            background-color: #1e1e1e;
                            color: #d4d4d4;
                            padding: 1rem;
                            border-radius: 0.5rem;
                            overflow-x: auto;
                            max-height: 500px;
                            overflow-y: auto;
                            font-family: monospace;
                            border: 1px solid #333;
                            user-select: text;
                        ">
                            <pre style="margin: 0; white-space: pre-wrap; word-wrap: break-word;">{content.replace('<', '&lt;').replace('>', '&gt;')}</pre>
                        </div>
                        """
                        st.markdown(html_content, unsafe_allow_html=True)
                    except Exception:
                        st.warning("Preview not available for this file type. Please download to view.")
            
            st.divider()
