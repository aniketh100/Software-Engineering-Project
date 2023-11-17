import streamlit as st
from googletrans import Translator, LANGUAGES
from PyPDF2 import PdfReader
from fpdf import FPDF
from gtts import gTTS
import base64
import time

def bulk():
    if "translation_result" not in st.session_state:
        st.session_state.translation_result = None

    st.sidebar.title("MENU")
    options = ["TEXT", "PDF", "MANUAL"]
    choice = st.sidebar.selectbox("Select Option", options)
    contents=None
   


    if choice == "TEXT":
        st.sidebar.info("Translate a Text File")
        file = st.file_uploader("Upload Text File", type=["txt"])
      
        if file is not None:
            contents = file.read().decode('utf-8')  # Decode bytes to string
    elif choice == "PDF":
  
        st.sidebar.info("Translate a PDF File")
        file = st.file_uploader("Upload PDF File", type=["pdf"])
        print(file,type(file))
        if file is not None:
            pdf_reader = PdfReader(file)
            contents = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                contents += page.extract_text()
    elif choice == "MANUAL":
        st.sidebar.info("Translate Manually Entered Text")
        contents = st.text_area("Enter Text")

   
    selected_language = st.sidebar.selectbox("Select Target Language", list(LANGUAGES.values()), index=list(LANGUAGES.keys()).index('fr'))

    lang_code = next(key for key, value in LANGUAGES.items() if value == selected_language)

    if st.button("Translate") and contents is not None:
        st.session_state.translation_result = translate(contents, selected_language)
        if st.session_state.translation_result is not None:
            st.success(st.session_state.translation_result)
    
       

    if st.button("Save as PDF") and st.session_state.translation_result is not None:
        save_as_pdf(st.session_state.translation_result, lang_code)

    if st.button("Audio Playback") and st.session_state.translation_result is not None:
        play_audio(st.session_state.translation_result, lang_code)


def translate(contents, lang):
    translator = Translator()
    translated = translator.translate(contents, dest=lang)
    return translated.text


def save_as_pdf(text, lang):
    pdf = FPDF()
    pdf.add_page()

    font_path = get_font_path(lang)
    font_name = get_font_name(lang)

    pdf.add_font(font_name, '', font_path, uni=True)
    pdf.set_font(font_name, size=14)

    # print(text)

    # Check if text is not None before processing
    if text is not None:
      
        cleaned_text = text.replace("\r", "")
        pdf.multi_cell(h=14, align="L", w=0, txt=cleaned_text, border=0)

 
    timestamp = int(time.time())
    output_filename = f"translatedfile_{timestamp}.pdf"
    
    # Specify the full path where the file can be written
    output_path = f"C:/Users/anany/Downloads/{output_filename}" #path where u want to save
    pdf.output(output_path)
    st.success(f"Translated file saved as {output_filename} in Downloads")

    # Return the generated filename for use in the download link
    # return output_filename

def get_font_name(lang):
    # Define font names for different languages
    font_names = {
        'kn': 'Malige',
        'ta': 'Hindi',
        'te': 'Telugu',
        'ml': 'Malayalam',
        'hi': 'Hindi',
        "default": 'DejaVu',
    }
    return font_names.get(lang, font_names["default"])

def get_font_path(lang):
    # Define font paths for different languages
    font_paths = {
        'kn': '\\fonts\\Malige-n.ttf',
        'ta': '\\fonts\\Lohit-Tamil.ttf',
        'te': '\\fonts\\Lohit-Telugu.ttf',
        'ml': '\\fonts\\RaghuMalayalamSans2.ttf',
        'hi': '\\fonts\\Mangal Regular.ttf',
        "default": '\\fonts\\DejaVuSans.ttf',
    }
    return font_paths.get(lang, font_paths["default"])


def play_audio(text, lang):
    try:
        output_audio = gTTS(text=text, lang=lang, slow=True)
        output_audio.save("output_audio.mp3")
        audio_file = open("output_audio.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Add download button
        st.markdown(get_binary_file_downloader_html("output_audio.mp3", 'Audio File'), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating audio playback: {e}")

# Helper function for creating a download link
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
    return href

if __name__ == "__main__":
    st.title("PDF TO AUDIO CONVERSION & TRANSLATION TOOL")
    bulk()
