import streamlit as st
import os
import time
import glob
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from deep_translator import GoogleTranslator


# ---- Estilo personalizado: paleta azul petróleo + terracota (Miguel Ruiz) ----
try:
    _icon = Image.open('logo_mr.png')
except Exception:
    _icon = "📄"
st.set_page_config(page_title="OCR + Audio · Miguel Ruiz", page_icon=_icon, layout="centered")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&family=Inter:wght@300;400;600&display=swap');
    .stApp {
        background: linear-gradient(135deg, #1b3a4b 0%, #14303d 100%);
        color: #e8eef0;
        font-family: 'Inter', sans-serif;
    }
    .stApp, .stApp p, .stApp li, .stApp span, .stApp label,
    .stMarkdown, [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {
        color: #e8eef0 !important;
    }
    h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif !important; color: #e07a5f !important; }
    .stTextInput input, .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div, .stNumberInput input {
        background-color: #f3f6f7 !important; color: #14303d !important;
    }
    input::placeholder, textarea::placeholder { color: #5c7079 !important; }
    [data-testid="stNotification"] * { color: #14303d !important; }
    section[data-testid="stSidebar"] { background: #12272f; }
    section[data-testid="stSidebar"] * { color: #e8eef0 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #e07a5f !important; }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #f3f6f7 !important; color: #14303d !important;
    }
    .stButton>button {
        background-color: #e07a5f; color: #fff !important; border-radius: 10px; border: none; font-weight: 600;
    }
    .stButton>button:hover { background-color: #c9583c; color: #fff !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


text = " "

def text_to_speech(input_language, output_language, text, tld):
    trans_text = GoogleTranslator(source=input_language, target=output_language).translate(text)
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text




def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
  



st.title("Reconocimiento Óptico de Caracteres (OCR) 🔤🔊")
st.caption("Lee texto de una imagen, tradúcelo y escúchalo en audio — por Miguel Ruiz")
st.subheader("Elige la fuente de la imagen: puede venir de la cámara o cargando un archivo")

cam_ = st.checkbox("Usar Cámara")

if cam_ :
   img_file_buffer = st.camera_input("Toma una Foto")
else :
   img_file_buffer = None
   
with st.sidebar:
      st.markdown("<h2 style=\"font-family:'Montserrat', sans-serif; color:#f2cc8f;\">Miguel Ruiz</h2>", unsafe_allow_html=True)
      st.subheader("Procesamiento para Cámara")
      filtro = st.radio("Filtro para imagen con cámara",('Sí', 'No'))

bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg"])
if bg_image is not None:
    uploaded_file=bg_image
    st.image(uploaded_file, caption='Imagen cargada.', use_container_width=True)
    
    # Guardar la imagen en el sistema de archivos
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())
    
    st.success(f"Imagen guardada como {uploaded_file.name}")
    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text= pytesseract.image_to_string(img_rgb)
st.write(text)  
    
      
if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    
    if filtro == 'Sí':
         cv2_img=cv2.bitwise_not(cv2_img)
    else:
        cv2_img= cv2_img
          
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text=pytesseract.image_to_string(img_rgb) 
    st.write(text) 

with st.sidebar:
      st.subheader("Parámetros de traducción")
      
      try:
          os.mkdir("temp")
      except:
          pass
      #st.title("Text to speech")

      #text = st.text_input("Enter text")
      in_lang = st.selectbox(
          "Seleccione el lenguaje de entrada",
          ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
      )
      if in_lang == "Ingles":
          input_language = "en"
      elif in_lang == "Español":
          input_language = "es"
      elif in_lang == "Bengali":
          input_language = "bn"
      elif in_lang == "koreano":
          input_language = "ko"
      elif in_lang == "Mandarin":
          input_language = "zh-cn"
      elif in_lang == "Japones":
          input_language = "ja"
      
      out_lang = st.selectbox(
          "Seleccione el lenguaje de salida",
          ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
      )
      if out_lang == "Ingles":
          output_language = "en"
      elif out_lang == "Español":
          output_language = "es"
      elif out_lang == "Bengali":
          output_language = "bn"
      elif out_lang == "koreano":
          output_language = "ko"
      elif out_lang == "Chinese":
          output_language = "zh-cn"
      elif out_lang == "Japones":
          output_language = "ja"
      
      english_accent = st.selectbox(
          "Seleccione el acento",
          (
              "Default",
              "India",
              "United Kingdom",
              "United States",
              "Canada",
              "Australia",
              "Ireland",
              "South Africa",
          ),
      )
      
      if english_accent == "Default":
          tld = "com"
      elif english_accent == "India":
          tld = "co.in"
      
      elif english_accent == "United Kingdom":
          tld = "co.uk"
      elif english_accent == "United States":
          tld = "com"
      elif english_accent == "Canada":
          tld = "ca"
      elif english_accent == "Australia":
          tld = "com.au"
      elif english_accent == "Ireland":
          tld = "ie"
      elif english_accent == "South Africa":
          tld = "co.za"

      display_output_text = st.checkbox("Mostrar texto")

      if st.button("Convertir a audio 🔊"):
          result, output_text = text_to_speech(input_language, output_language, text, tld)
          audio_file = open(f"temp/{result}.mp3", "rb")
          audio_bytes = audio_file.read()
          st.markdown(f"## Tu audio:")
          st.audio(audio_bytes, format="audio/mp3", start_time=0)
      
          if display_output_text:
              st.markdown(f"## Texto de salida:")
              st.write(f" {output_text}")




 
    
    
