import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt = """You're an expert YouTube video summarizer. You will recieve the transcript text and your task is to summarize the video. Here is the transript text: \n"""

def generate_gemini_content(transcript_text):
    model=genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content(prompt+f"Transcript text: {transcript_text}")
    return response.text

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript+=" "+i["text"]
        return transcript    
        
    except Exception as e:
        raise e
    
    
    
st.title("YouTube Transcript to Summary")
youtube_link = st.text_input("Enter YouTube Video Link:")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcipt_text = extract_transcript_details(youtube_link)
    if transcipt_text:
        summary = generate_gemini_content(transcipt_text)
        st.markdown("## Detailed Notes:")
        st.write(summary)


