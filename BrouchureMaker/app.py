import streamlit as st
from llmController import llm1_controller,llm2_controller
from makeBrouchure import generate_brochure_html


st.set_page_config(layout="wide")
st.title("📖 Brouchure Maker")

if "img_links" not in st.session_state:
    st.session_state.img_links = []
if "state_step" not in st.session_state:
    st.session_state.state_step = "form_entry"
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None
if "selected_img_flag" not in st.session_state:
    st.session_state.selected_img_flag = False
if "llm_response" not in st.session_state:
    st.session_state.llm_response = None
if "llm2_text" not in st.session_state:
    st.session_state.llm2_text = ""
if "llm2_processed" not in st.session_state:
    st.session_state.llm2_processed = False
    
with st.sidebar:
    st.subheader("Brouchure Settings")
    with st.form("Brouchure Form"):
        url=st.text_input("Enter Company/Event website URL", placeholder="https://example.com/")
        tone = st.selectbox("Choose Content Tone", ["Business", "Humorous/Jovial", "Snarky", "Professional"])
        type_select=st.radio("Company/Event",options=["Company","Event"])
        name=st.text_input("Please name the Company/Event Name")
        submit_btn=st.form_submit_button("submit")

if submit_btn and url:
    with st.spinner("Analyzing website links and scraping assets..."):
        response, img_links = llm1_controller(url,type_select)
        st.session_state.llm_response = response
        st.session_state.img_links = img_links if isinstance(img_links, list) else []
        st.session_state.selected_img = None
        st.session_state.selected_img_flag = False
        st.session_state.llm2_text = ""
        st.session_state.llm2_processed = False
        st.session_state.state_step="image_selection"
        st.rerun()
        
if st.session_state.state_step=="image_selection":
    tab1,tab2,tab3= st.tabs(["🌐 Scraped Web Images", "📤 Upload Custom Image", "No Image"])

    with tab1:
        if st.session_state.img_links:
            st.subheader("Select an Image from website")
            st.write("Clcik the button of the image")
            cols=st.columns(4)
            for index,img_link in enumerate(st.session_state.img_links):
                with cols[index%4]:
                    try:
                        st.image(img_link,use_container_width=True)
                        if st.button(f"Select button {index+1}",key=f"btn-{index}"):
                            st.session_state.selected_img=img_link
                            st.session_state.selected_img_flag = True
                            st.session_state.state_step = "final_render"
                            st.rerun()
                    except Exception as e:
                        st.caption("Unable to load the preview")
        else:
            st.info("No images were found on the scraped webpage. Please use the upload tab instead.")
    with tab2:
        st.subheader("Upload a custom image")
        uploaded_img=st.file_uploader("Upload",type=["png", "jpg", "jpeg"])
        if st.button("Use Uploaded Image", key="confirm_upload_btn"):
                st.session_state.selected_img = uploaded_img
                st.session_state.selected_img_flag = True
                st.session_state.state_step = "final_render"
                st.rerun()
    with tab3:
        st.subheader("Skip Graphic Element")
        st.write("Proceeding without a graphic placeholder.")
        if st.button("Confirm: Skip Graphics Layout", key="confirm_no_image_btn"):
            st.session_state.selected_img = None
            st.session_state.selected_img_flag = True
            st.session_state.state_step = "final_render"
            st.rerun()
            
    
if st.session_state.state_step == "final_render":
    if st.session_state.selected_img_flag:
        if st.session_state.selected_img:
            st.success("✅ Image selected successfully!")
            st.image(st.session_state.selected_img, caption="Active Brochure Graphic Selection", width=300)
        else:
            st.info("ℹ️ Proceeding without image layout graphics.")
        
    if st.session_state.llm_response and st.session_state.selected_img_flag and not st.session_state.llm2_processed:
        with st.spinner("Processing....Please wait"):
            text1=llm2_controller(st.session_state.llm_response,tone,name,type_select)
            st.session_state.llm2_text=text1
            st.session_state.llm2_processed = True
            st.rerun()
        
    if st.session_state.llm2_text and st.session_state.llm2_processed:
        st.markdown("-------")
        st.subheader("⬇️ PDF preview and download")
        htmlfile=generate_brochure_html(st.session_state.llm2_text,st.session_state.selected_img,name)
        st.iframe(htmlfile, height=600)
        st.download_button(label="Download Print-Ready Brochure (HTML/CSS)-Save as PDF with ctrl+P",
                        data=htmlfile,
                        file_name=f"{name.lower().replace(" ","_")}_brouchure.html",
                        mime="text/html")