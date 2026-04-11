import streamlit as st
from PIL import Image
import pillow_heif
import io
import os

import streamlit as st

import streamlit as st

# --- AZ ÖSSZES STÍLUS EGYBEN (HÁTTÉR + FEHÉR SZÖVEG) ---
st.markdown(
    """
    <style>
    /* 1. Háttérszín fixálása */
    .stApp {
        background-color: #fedcba !important;
    }

    /* 2. Feltöltő doboz sötétítése és stílusa */
    [data-testid="stFileUploadDropzone"] {
        background-color: #262730 !important;
        border: 2px dashed #4a3a2a !important;
        border-radius: 15px;
    }

    /* 3. ATOMBIZTOS FEHÉR SZÖVEG (mindenre a dobozon belül) */
    /* Ez eléri a gombot, a kisbetűs részt és a leírást is */
    [data-testid="stFileUploadDropzone"] * {
        color: white !important;
    }

    /* 4. Az ikon kényszerített fehérítése */
    [data-testid="stFileUploadDropzone"] svg path {
        fill: white !important;
    }

    /* 5. A gomb körüli keret fehérítése (ha van) */
    [data-testid="stFileUploadDropzone"] button {
        border-color: white !important;
    }

    /* 6. A címsorok sötétbarnája, hogy jól látszódjanak a beige háttéren */
    h1, h2, h3, .stMarkdown p {
        color: #4a3a2a !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# HEIC támogatás regisztrálása
pillow_heif.register_heif_opener()

st.set_page_config(page_title="Profi Képkomprimáló", page_icon="🖼️")

st.title("🖼️ Képméret Csökkentő & HEIC Konverter")
st.write("Töltsd fel a képed, állítsd be a tömörítést, és töltsd le JPG-ben!")

uploaded_file = st.file_uploader("Válassz ki egy képet (JPG, PNG, HEIC)", type=["jpg", "jpeg", "png", "heic"])

if uploaded_file is not None:
    # Eredeti méret kiszámítása megabájtban
    original_size = uploaded_file.size / (1024 * 1024)

    # Kép megnyitása és konvertálása
    image = Image.open(uploaded_file)
    if uploaded_file.name.lower().endswith(".heic"):
        image = image.convert("RGB")
        st.info("🍎 HEIC formátum észlelve - Átalakítás JPG-re...")

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption=f"Eredeti kép ({original_size:.2f} MB)", use_container_width=True)

    with col2:
        st.subheader("Beállítások")
        # A csúszka: itt állítja be a felhasználó a tömörítés mértékét
        # A 100-as minőség a legkisebb tömörítés, az 1-es a legnagyobb.
        quality = st.slider("Célzott minőség (Minél kisebb, annál jobb tömörítés)", 1, 100, 70)

        # Mentés memóriába a kiválasztott minőséggel
        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=quality, optimize=True)
        compressed_data = buf.getvalue()
        compressed_size = len(compressed_data) / (1024 * 1024)

        # Százalékos megtakarítás kiszámítása
        reduction = 100 - (compressed_size / original_size * 100)

        st.metric("Becsült új méret", f"{compressed_size:.2f} MB", f"-{int(reduction)}%")
        st.download_button(
            label="✨ Tömörített kép letöltése",
            data=compressed_data,
            file_name="tomoritett_kep.jpg",
            mime="image/jpeg",
            use_container_width=True
        )

    if reduction > 0:
        st.success(f"Siker! A kép méretét {reduction:.1f}%-kal csökkentetted.")