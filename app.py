# Importing Necessary libraries
import streamlit as st
from utils import get_summary, transcribe_audio
import time

# Setting the page layout
st.set_page_config(layout="wide")

# App write up
st.markdown("<h1 style='text-align: Center; color: #FFFFF; font-weight: LIGHT; font-size: 37px;'>Audio Translator</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: Center; color: #FFFFF; font-size: 14px;'>This app helps you extract transcript from your audio files and calls using AssemblyAI and langchain openAI <br> Provide your audio file and specify the number of users to accurately translate your audio files. </h1>", unsafe_allow_html=True)


st.sidebar.header("AUDIO TRANSLATOR")
# Uploading the audio files
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

# Check if an audio file is uploaded
if audio_file is not None:
    #Process the uploaded audio file
    st.session_state.audio_uploaded = True
    st.audio(audio_file)
    st.sidebar.success("Audio file uploaded successfully!")
        

    # Select number of speakers
    st.sidebar.header("TRANSCRIPTION")
    speakers = st.sidebar.selectbox("How many speakers are in the audio", [1, 2, 3])

    # Create a transcribe button
    button = st.sidebar.button("Transcribe")

    # Add CSS to move the button to the right and change its color
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        float: right;
        background-color: red;
        color: white;
    }
    div.stButton > button:first-child:hover {
    background-color: darkred;
    }
    div.stButton > button:first-child:hover:after {
        content: "start transcription";
        position: absolute;
        left: 100;
        top: 100%;
        color: white;
        padding: 5px;
        border-radius: 5px;
        white-space: nowrap;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for the button
    if "load_state" not in st.session_state:
        st.session_state.load_state = False

    
    # A button for transcription
    if button or st.session_state.load_state:
        st.session_state.load_state = True
        # Perform transcription
        transcription = transcribe_audio(audio_file, speakers)
        st.sidebar.success("Audio transcribes successfully!")
        st.info("TRANSCRIPTION:")
        styled_container = f"""
        <div style="margin: auto; max-height: 400px; overflow-y: scroll;">
            {transcription}
        </div>
        """

        # Render the styled container with the transcription using Markdown
        st.markdown(styled_container, unsafe_allow_html=True)
            
        # Setting up Langugae and Summary Column 
        st.sidebar.header("GET SUMMARY")
        language = st.sidebar.selectbox("Choose language:", ["English", "French", "Spanish", "Hindu"])
        summary_type = st.sidebar.selectbox("Choose summary type:", ["one_sentence", "bullet_points", "short", "long"])

        # Adding a download button to download the transcript and a button to get script summary
        col1, col2= st.sidebar.columns(2)

        with col1:
            st.download_button('Download Script', transcription)
        with col2:
            st.session_state.show_summary = False
            if st.button("Get Summary", help="Click to get audio summary"):
                st.session_state.show_summary = True
        
        # Getting the summarry
        if 'show_summary' in st.session_state and st.session_state.show_summary:
            st.info("SUMMARY:") 
            summary = get_summary(transcription, language, summary_type)
            styled_container2 = f"""
            <div style="margin: auto; max-height: 400px; overflow-y: scroll;">
                {summary}
            </div>
            """
            st.markdown(styled_container2, unsafe_allow_html=True)


else:
    st.info("Please upload an audio file.")