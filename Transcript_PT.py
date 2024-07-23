import assemblyai as aai
import streamlit as st
from pydub import AudioSegment
import os

aai.settings.api_key = ["auth_key"]

supported_languages_for_best = {"en","en_au","en_uk","en_us","es","fr","de","it",
                                "pt","nl","hi","ja","zh","fi","ko","pl","ru","tr","uk","vi",}
@st.cache_data
def convert_video_to_mp3(video_path):
    try:
        audio = AudioSegment.from_file(video_path, format="mp4")
        mp3_path = video_path.replace(".mp4", ".mp3")
        audio.export(mp3_path, format="mp3")
        st.success(f"{os.path.basename(video_path)} has been successfully converted to MP3.")
        return mp3_path
    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
        return None

@st.cache_data    
def detect_language(audio_url):
    config = aai.TranscriptionConfig(
        audio_end_at=60000,  # first 60 seconds (in milliseconds)
        language_detection=True,
        speech_model=aai.SpeechModel.nano,
    )
    transcript = transcriber.transcribe(audio_url, config=config)
    return transcript.json_response["language_code"]

@st.cache_data
def transcribe_file(audio_url, language_code):
    config = aai.TranscriptionConfig(
        language_code=language_code,
        summary_model="informative",
        summary_type="bullets_verbose",
        speech_model=(
            aai.SpeechModel.best
            if language_code in supported_languages_for_best
            else aai.SpeechModel.nano
        ),
    )
    transcript = transcriber.transcribe(audio_url, config=config)
    return transcript.json_response

#config = aai.TranscriptionConfig(
  #language_code="pt",
  #language_detection=True,
  #summarization=True,
  #summary_model=aai.SummarizationModel.informative,
  #summary_type=aai.SummarizationType.bullets_verbose)

transcriber = aai.Transcriber()

#transcript = transcriber.transcribe(audio_url, config)

#print(transcript.summary)

st.title("Local Video to MP3 Analyzer")
st.markdown("With this app, you can analyze a video from your local machine to see its content summary and sentiment analysis.")
st.markdown("Make sure your local file path is correctly provided.")

#audio_url = "C:\\AI\\Video\\CHAMADA FAROL SAGRES.mp3"


def main():
    video_path = st.text_input("Enter the local path of the video:", value="C:\\AI\\Video\\A04GEO9 CORRECAO 2.mp4")

    if st.button("Analyze Video"):
        if video_path and os.path.exists(video_path):
            mp3_path = convert_video_to_mp3(video_path)
            if mp3_path:
                language_code = detect_language(mp3_path)#(audio_url)
                if language_code:
                    transcript = transcribe_file(mp3_path, language_code)#(audio_url, language_code)
                    st.header("Transcribe of this video")
                    st.write(transcript.get("text","")[:10000], "...")
        else:
            st.error("Please provide a valid local file path.")


if __name__ == '__main__':
    main()

#language_code = detect_language(audio_url)
#print("Identified language:", language_code)

#transcript = transcribe_file(audio_url, language_code)
#print("Transcript:", transcript.text[:6000], "...")


