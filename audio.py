import streamlit as st
import requests

# Function to recognize the song
def recognize_song(api_key, audio_file):
    # Convert uploaded file to bytes for API
    files = {
        'file': ('audio.mp3', audio_file, 'audio/mpeg')
    }
    
    # Send request to Audd.io API
    response = requests.post(
        'https://api.audd.io/',
        data={'api_token': api_key, 'return': 'timecode,apple_music,spotify'},
        files=files
    )
    
    # Parse response
    if response.status_code == 200:
        result = response.json()
        if 'result' in result and result['result']:
            return result['result']
        else:
            return "No song identified."
    else:
        return f"Error: {response.status_code}"


def song():
    # API key for Audd.io
    api_key = st.text_input("Enter your Audd.io API key", type="password")

    uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav", "m4a"])

    if uploaded_file and api_key:
        st.write("Identifying the song...")
        result = recognize_song(api_key, uploaded_file)
        
        if isinstance(result, dict):
            st.write("Song Identified!")
            st.write(f"**Title:** {result['title']}")
            st.write(f"**Artist:** {result['artist']}")
            st.write(f"**Album:** {result.get('album', 'N/A')}")
            
            if 'spotify' in result:
                st.write(f"[Listen on Spotify]({result['spotify']['external_urls']['spotify']})")
            if 'apple_music' in result:
                st.write(f"[Listen on Apple Music]({result['apple_music']['url']})")
        else:
            st.write(result)

