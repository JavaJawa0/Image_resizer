import streamlit as st
from PIL import Image
import pillow_heif
import io

# HEIC támogatás regisztrálása
pillow_heif.register_heif_opener()

# --- OLDAL BEÁLLÍTÁSAI ---
st.set_page_config(page_title="JavaJawa Pic Compressor", page_icon="🖼️")

# --- CSS STÍLUSOK (Neon Beige & Pacek UI) ---
st.markdown(
    """
    <style>
    /* 1. Fő háttér: Neon Beige (#fedcba) */
    .stApp {
        background-color: #fedcba !important;
    }

    /* 2. Címek és szövegek: Sötétbarna */
    h1, h2, h3, p, label, .stMarkdown {
        color: #4a3a2a !important;
    }

    /* 3. Feltöltő doboz stílusa */
    [data-testid="stFileUploadDropzone"] {
        background-color: #262730 !important; /* Sötét sáv */
        border: 2px dashed #4a3a2a !important;
        border-radius: 15px;
    }

    /* 4. Feltöltő dobozon belüli szövegek és gomb: FEHÉR */
    [data-testid="stFileUploadDropzone"] * {
        color: white !important;
    }

    [data-testid="stFileUploadDropzone"] svg path {
        fill: white !important;
    }

    [data-testid="stFileUploadDropzone"] button {
        border-color: white !important;
    }

    /* 5. Csúszka és egyéb widgetek színeinek finomítása */
    .stSlider label {
        color: #4a3a2a !important;
        font-weight: bold;
    }

    /* 6. Hibaüzenetek olvashatósága */
    .stAlert p {
        color: #4a3a2a !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- ALKALMAZÁS LOGIKA ---

st.title("🖼️ JavaJawa Pic Compressor")
st.write("Töltsd fel a képet, és hozd ki belőle a legkisebb méretet pacek minőségben!")

uploaded_file = st.file_uploader("Válassz ki egy képet (JPG, PNG, HEIC)", type=["jpg", "jpeg", "png", "heic"])

if uploaded_file is not None:
    # Eredeti fájlméret kiszámítása
    original_size = uploaded_file.size / (1024 * 1024)

    # Kép megnyitása
    image = Image.open(uploaded_file)

    # Automatikus HEIC felismerés és konverzió
    if uploaded_file.name.lower().endswith(".heic"):
        st.info("🍎 Apple HEIC formátum észlelve - Konvertálás...")

    # Megjelenítés két oszlopban
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption=f"Eredeti kép ({original_size:.2f} MB)", use_container_width=True)

    with col2:
        st.subheader("Beállítások")

        # Minőség csúszka
        quality = st.slider("Tömörítés mértéke (Minőség)", 1, 100, 75)

        # TÖMÖRÍTÉS FOLYAMATA
        buf = io.BytesIO()

        # KRITIKUS JAVÍTÁS: Mindig RGB-be konvertálunk mentés előtt (megoldja az OSError-t)
        # Ez eltávolítja az átlátszóságot (Alfa csatorna), amit a JPEG nem tud kezelni.
        rgb_image = image.convert("RGB")

        rgb_image.save(buf, format="JPEG", quality=quality, optimize=True)
        compressed_data = buf.getvalue()
        compressed_size = len(compressed_data) / (1024 * 1024)

        # Százalékos megtakarítás
        reduction = 100 - (compressed_size / original_size * 100)

        # Eredmény mutatása
        st.metric("Becsült új méret", f"{compressed_size:.2f} MB", f"-{reduction:.1f}%")

        # Letöltés gomb
        st.download_button(
            label="✨ Tömörített kép letöltése",
            data=compressed_data,
            file_name="JavaJawa_compressed.jpg",
            mime="image/jpeg",
            use_container_width=True
        )

    if reduction > 0:
        st.success(f"Pacek! A fájlméret {reduction:.1f}%-kal lett kisebb.")
    else:
        st.warning("A jelenlegi beállításokkal a fájlméret nem csökkent. Próbálj alacsonyabb minőséget!")