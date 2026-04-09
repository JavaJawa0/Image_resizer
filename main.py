import streamlit as st
from PIL import Image

st.title("Képméret Csökkentő")

uploaded_file = st.file_uploader("Válassz ki egy képet...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Eredeti kép', use_column_width=True)

    # Csúszka a minőséghez
    quality = st.slider("Minőség (0-100)", 1, 100, 80)

    if st.button("Csökkentés és Mentés"):
        # Itt történik a mágia
        image.save("resized.jpg", quality=quality, optimize=True)
        with open("resized.jpg", "rb") as file:
            st.download_button(
                label="Letöltés",
                data=file,
                file_name="csokkentett_kep.jpg",
                mime="image/jpeg"
            )