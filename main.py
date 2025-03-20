import streamlit as st
from streamlit.components.v1 import html
from web_generator import *


def main():
    st.set_page_config(page_title="Website Preview", layout="wide")
    
    # st.title("Website Template Preview")
    
    st.markdown(
        "<h1 style='text-align: center;'>Website Template Preview</h1>",
        unsafe_allow_html=True,
    )
    
    form = st.form(key='my_form')
    name=form.text_input(label='Name')
    profession=form.text_input(label='Profession')
    color=form.text_input(label='Color')
    submit_button = form.form_submit_button(label='Submit')

    col1, col2= st.columns(2)
    print(name,profession)
    default_html=generate_website(name, profession,color_input=color)

    # Text area for HTML code
#     default_html = """<!DOCTYPE html>
# <html>
# <head>
#     <title>Sample Website</title>
#     <style>
#         body { font-family: Arial; text-align: center; margin-top: 50px; }
#         h1 { color: #3498db; }
#         .container { max-width: 800px; margin: auto; }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>Hello from Streamlit!</h1>
#         <p>This is a sample website preview. Replace this with your own HTML.</p>
#         <button onclick="showMessage()">Click me</button>
#     </div>
    
#     <script>
#         function showMessage() {
#             alert('Button clicked!');
#         }
#     </script>
# </body>
# </html>
# """

    
    with col1:
        with st.expander("Code Editor", expanded=True):
            html_code = st.text_area("Paste your HTML code here", value=default_html, height=800)
        
        # Controls
        # col1, col2 = st.columns([2, 1])
        # with col1:
        #     preview_height = st.slider("Preview Height (px)", min_value=400, max_value=2000, value=800, step=100)
        # with col2:
            preview_button = st.button("Update Preview", type="primary")
        
    # Display the preview
    with col2:
        if preview_button or 'html_code' in st.session_state:
            if preview_button:
                st.session_state.html_code = html_code
            
            st.markdown("### Website Preview")
            st.markdown("---")
            
            # Render the HTML
            try:
                html(st.session_state.html_code,height=800, scrolling=True)
            except Exception as e:
                st.error(f"Error rendering HTML: {e}")


if __name__ == "__main__":
    main()