import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
from tensorflow.keras.applications.resnet50 import preprocess_input

# Tu codigo aqui

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('mi_modelo_pokemon.keras')
    with open('clases_pokemon.json', 'r') as f:
        class_indices = json.load(f)

    idx_to_class = {v: k for k, v in class_indices.items()}
    return model, idx_to_class

modelo, idx_to_class = load_model()

st.title('Clasificador por Tipo de Pokemon')
st.write('Sube una imagen de un Pokémon para descubrir su tipo predominante.')

uploaded_file = st.file_uploader('Elige una imagen de un Pokemon', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Imagen subida', use_container_width=True)

    st.write("Analizando...")

    IMG_SIZE = 160
    img_resized = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img_resized)

    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    pred = modelo.predict(img_array, verbose=0)[0]

    st.subheader('Predicciones:')

    for idx in pred.argsort()[::-1]:
        nombre = idx_to_class[idx].replace('_', ' ').title()
        prob = pred[idx]
        st.write(f"**{nombre}**: {prob:.1%}")
        st.progress(float(prob))