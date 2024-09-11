import streamlit as st
from deep_translator import GoogleTranslator

# Streamlit Interface
st.markdown("""
    <style>
    body {
        background-color: #f0f0f0; /* Light grey background */
        color: black; /* Black text color */
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #0056b3; /* Blue color for the title */
        text-align: center;
        margin-top: 20px;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .input-box {
        border: 2px solid #0056b3; /* Blue border */
        border-radius: 8px;
        padding: 12px;
        background-color: #ffffff; /* White background for the input box */
        margin: 0 auto;
        max-width: 600px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
    }
    .button {
        background-color: #0056b3; /* Blue button */
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1.2em;
        margin-top: 20px;
        display: block;
        margin: 20px auto;
    }
    .button:hover {
        background-color: #003d80; /* Darker blue on hover */
    }
    .output {
        border: 2px solid #0056b3; /* Blue border */
        border-radius: 8px;
        padding: 12px;
        background-color: #ffffff; /* White background for the output box */
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
        text-align: center;
        font-size: 1.2em;
        margin-top: 20px;
        color: black; /* Black color for output text */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><div class="title">Language Translator</div></div>', unsafe_allow_html=True)
st.write("Enter the text to translate and select the target language:")

# Google Translator
def translate_text(text, target_lang):
    translator = GoogleTranslator(target=target_lang)
    return translator.translate(text)

# Input text from user
input_text = st.text_input("Input Text", key='input', label_visibility="collapsed", help="Enter the text you want to translate", placeholder="Enter text here...")

# Updated language options
languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Hindi': 'hi',
    'Chinese (Simplified)': 'zh-cn',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Malayalam': 'ml',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Kannada': 'kn'
}

# Display language selection
target_language = st.selectbox("Select Target Language", list(languages.keys()))

# Perform translation on button click
if st.button("Translate", key='translate'):
    if input_text:
        translated_text = translate_text(input_text, languages[target_language])
        st.markdown(f'<div class="output"><strong>Translated Text:</strong><br>{translated_text}</div>', unsafe_allow_html=True)
