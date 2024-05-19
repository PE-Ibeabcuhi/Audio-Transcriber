import streamlit as st
import assemblyai as aai # Assembly AI Transcribe library
from langchain.chat_models import ChatOpenAI # Langchain AI chat library
from langchain.chains.summarize import load_summarize_chain # Langchain summarization library
from langchain.text_splitter import RecursiveCharacterTextSplitter # To split our transcript into pieces
import os #To access file repositories
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)

@st.cache_data
def transcribe_audio(audio, speakers_expected):
    """
    This function instializes AssemeblyAI transcription library to transcribe
    audio files and generate scripts. It accepts two arguments, the audio files, 
    and a specified number of speakers

    """
    # Set API key
    aai.settings.api_key = "488825166df34eb4bde6db2b168aab31"
    
    # Configure transcription
    config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=speakers_expected)
    
    # Initialize transcriber
    transcriber = aai.Transcriber()
    
    # Transcribe audio
    transcript = transcriber.transcribe(audio, config=config)

    # Initialize an empty string to store the transcript
    transcript_text = ""

    # Iterate through the utterances and append them to the transcript text
    for utterance in transcript.utterances:
        transcript_text += f"Speaker {utterance.speaker}: {utterance.text}\n\n"

    return transcript_text


def get_summary(content, Language, summary_type):
    os.environ['OPENAI_API_KEY'] = "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"
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=2000, chunk_overlap=250)
    texts = text_splitter.create_documents([content])

    llm = ChatOpenAI(temperature=0)

    summary_output_options = {
    'one_sentence' : """
     - Only one sentence
    """,
    
    'bullet_points': """
     - Bullet point format
     - Separate each bullet point with a new line
     - Each bullet point should be concise
    """,
    
    'short' : """
     - A few short sentences
     - Do not go longer than 4-5 sentences
    """,
    
    'long' : """
     - A verbose summary
     - You may do a few paragraphs to describe the transcript if needed
    """
    }

    template = """
    You are a helpful assistant that helps summarize informations from a call. Your goal is to identify the names of the speakers and write a summary from the perspective of the call reveiver
    to highlight key points that are relevant informations. Do not include Preambles and do not repeat names. If you don't know say I don't know.

    Respond with the following format
    {output_format}

    Respond with the following language
    {language}

    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template="{text}" # Simply just pass the text as a human message
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt_combine = ChatPromptTemplate.from_messages(messages=[system_message_prompt, human_message_prompt])

    chain = load_summarize_chain(llm,chain_type="map_reduce",combine_prompt=chat_prompt_combine,verbose=True)
    Language = Language
    user_selection = summary_type
    
    output = chain.run({"input_documents": texts, "language": Language, "output_format" : summary_output_options[user_selection]})

    return(output)




