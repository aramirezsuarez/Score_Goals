# -*- coding: utf-8 -*-
"""reconocer_jugador.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nHdHeaJB8xNkP2HlYZxn_RehAiHCfOM3
"""

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import numpy as np

# Crear pie de pagina con los datos de contacto de los creadores
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        z-index: 10;
        width: 100%;
        background-color: rgb(14, 17, 23);
        color: black;
        text-align: center;
    }
    .footer p {
        color: white;
    }
</style>
<div class="footer">
    <p>App desarrollada por: <br />
    Andres Felipe Ramirez Suarez <br />
    Contactenos: <a href="#">aramirezsu@unal.edu.co</a>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

# Título de la aplicación
st.title("Adivina el Jugador por su Foto")

# URL de datos
url_players = ("https://raw.githubusercontent.com/aramirezsuarez"
              "/Score_Goals/main/datasets/players.csv")

# Carga DF desde URL
df_players = pd.read_csv(url_players)


def resize_image(image, new_size=(300, 300)):
    """
    Redimensiona una imagen utilizando el método `resize` de la biblioteca PIL.

    Parameters:
    - image (PIL.Image.Image): La imagen que se va a redimensionar.
    - new_size (tuple): Una tupla que especifica las nuevas dimensiones de la imagen.
                       Por defecto, se establece en (300, 300).

    Returns:
    - PIL.Image.Image: La imagen redimensionada.
    """

    return image.resize(new_size)


def guess_the_player(df):
    """
    Juego para adivinar el nombre de un jugador a partir de su imagen.

    Parameters:
    - df (pandas.DataFrame): Un DataFrame que contiene información
                            sobre jugadores,
                            incluyendo nombres y URL de imágenes.

    Returns:
    None

    El juego selecciona aleatoriamente un jugador del DataFrame,
    muestra su imagen reflejada horizontalmente y pide al usuario que
    adivine el nombre del jugador. El usuario puede ingresar su respuesta
    en un campo de texto. Se proporciona retroalimentación sobre si
    la respuesta es correcta o incorrecta.

    """

    random_row = df.sample()
    name = random_row['name'].values[0]
    image_url = random_row['image_url'].values[0]

    # Agregar un parámetro de consulta para forzar la recarga de la imagen
    image_url += "?t=" + str(np.random.randint(1, 1e8))

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Redimensionar la imagen antes de mostrarla
    img_resized = resize_image(img, new_size=(300, 300))

    # Espejo horizontal usando NumPy
    img_array = np.array(img_resized)
    img_array_flipped = np.fliplr(img_array)
    img_flipped = Image.fromarray(img_array_flipped)

    # Muestra la imagen espejada con un ancho específico
    st.image(img_flipped, width=300, use_column_width=False)

    if "user_guess" not in st.session_state:
        st.session_state.user_guess = ""

    user_guess = st.text_input("¿Cuál es el nombre del jugador?",
                               value=st.session_state.user_guess)

    if user_guess:
        user_guess = user_guess.strip()

        if user_guess.lower() == name.lower():
            st.success('¡Correcto!')
            st.session_state.user_guess = ""
        else:
            st.error(f'Incorrecto. El nombre del jugador es {name}.')
            st.session_state.user_guess = user_guess


guess_the_player(df_players)