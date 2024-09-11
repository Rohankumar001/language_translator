import streamlit as st
import torch
import torch.nn as nn
from deep_translator import GoogleTranslator
import base64

# Function to load an image and convert it to base64 for use in CSS
def get_base64_image(img_path):
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Path to the image
img_path = "D:/Desktop/MCA 3rd sem/NLP/Language_Translator/translationimg.jpg"
img_base64 = get_base64_image(img_path)

# Check if the image was successfully converted to base64
if img_base64 is None:
    st.error("Image file not found. Please check the file path.")
else:
    # Define the Encoder class
    class Encoder(nn.Module):
        def __init__(self, input_dim, emb_dim, hidden_dim, n_layers, dropout):
            super().__init__()
            self.embedding = nn.Embedding(input_dim, emb_dim)
            self.rnn = nn.LSTM(emb_dim, hidden_dim, n_layers, dropout=dropout)
            self.dropout = nn.Dropout(dropout)
            
        def forward(self, src):
            embedded = self.dropout(self.embedding(src))
            outputs, (hidden, cell) = self.rnn(embedded)
            return hidden, cell

    # Define the Decoder class
    class Decoder(nn.Module):
        def __init__(self, output_dim, emb_dim, hidden_dim, n_layers, dropout):
            super().__init__()
            self.embedding = nn.Embedding(output_dim, emb_dim)
            self.rnn = nn.LSTM(emb_dim, hidden_dim, n_layers, dropout=dropout)
            self.fc_out = nn.Linear(hidden_dim, output_dim)
            self.dropout = nn.Dropout(dropout)
            
        def forward(self, input, hidden, cell):
            input = input.unsqueeze(0)
            embedded = self.dropout(self.embedding(input))
            output, (hidden, cell) = self.rnn(embedded, (hidden, cell))
            prediction = self.fc_out(output.squeeze(0))
            return prediction, hidden, cell

    # Define the Seq2Seq class
    class Seq2Seq(nn.Module):
        def __init__(self, encoder, decoder, device):
            super().__init__()
            self.encoder = encoder
            self.decoder = decoder
            self.device = device
            
        def forward(self, src, trg, teacher_forcing_ratio=0.5):
            trg_len = trg.shape[0]
            batch_size = trg.shape[1]
            trg_vocab_size = self.decoder.fc_out.out_features
            
            outputs = torch.zeros(trg_len, batch_size, trg_vocab_size).to(self.device)
            
            hidden, cell = self.encoder(src)
            
            input = trg[0, :]
            
            for t in range(1, trg_len):
                output, hidden, cell = self.decoder(input, hidden, cell)
                outputs[t] = output
                top1 = output.argmax(1)
                input = trg[t] if random.random() < teacher_forcing_ratio else top1
            
            return outputs

    # Streamlit Interface
    st.markdown(f"""
        <style>
        body {{
            background-image: url(data:image/jpeg;base64,{img_base64});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: black; /* Black text color */
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }}
        .title {{
            font-size: 2.5em;
            font-weight: bold;
            color: black; /* Black color for the title */
            text-align: center;
            margin-top: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .input-box {{
            border: 2px solid #0056b3; /* Blue border */
            border-radius: 8px;
            padding: 12px;
            background-color: #ffffff; /* White background for the input box */
            margin: 0 auto;
            max-width: 600px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
        }}
        .button {{
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
        }}
        .button:hover {{
            background-color: #003d80; /* Darker blue on hover */
        }}
        .output {{
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
        }}
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
