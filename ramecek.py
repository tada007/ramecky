from PIL import Image, ImageDraw
import os
import streamlit as st
from io import BytesIO

# Pfad zum Ordner für die gespeicherten Bilder mit Rahmen
output_ordner = r'\output'

if not os.path.exists(output_ordner):
    os.makedirs(output_ordner)

# Pfad zum vorgegebenen Logo (korrigieren!)
logo_pfad = r"Logo_De Wit.png"  # Ersetze dies mit dem tatsächlichen Pfad zu deinem Logo

st.title("Generátor fotorámečků")

st.header("Nahrajte obrázky")
uploaded_files = st.file_uploader(
    "Vyberte obrázky", accept_multiple_files=True
)

# Logo hinzufügen (fest vorgegeben)
add_logo = st.checkbox('Přidat logo_1')
add_logo2 = st.checkbox('Přidat logo_2 (zatím nefunkční)')

# Schieberegler für die Logo-Größe (wird nur angezeigt, wenn die Checkbox aktiviert ist)
logo_percentage = 10
if add_logo or add_logo2:
    logo_percentage = st.slider('Velikost loga', min_value=5, max_value=30, value=10)

def add_split_frame(image, logo=None, logo_percentage=10):
    border_size = 8
    width, height = image.size

    # Neue Größe des Bildes mit Rahmen
    new_width = width + 2 * border_size
    new_height = height + 2 * border_size

    # Neues Bild mit dem Rahmen (linke Farbe Weiß, rechte Farbe Blau)
    new_image = Image.new("RGB", (new_width, new_height), "#FFFFFF")
    draw = ImageDraw.Draw(new_image)

    # Rechte Hälfte des Rahmens (rechts, unten)
    draw.rectangle([new_width // 2, 0, new_width, border_size], fill="#004f85")  # oberer Rahmen (rechts)
    draw.rectangle([new_width // 2, new_height - border_size, new_width, new_height], fill="#004f85")  # unterer Rahmen (rechts)
    draw.rectangle([new_width - border_size, 0, new_width, new_height], fill="#004f85")  # rechter Rahmen

    # Füge das Originalbild in die Mitte des neuen Bildes ein
    new_image.paste(image, (border_size, border_size))

    # Logo hinzufügen, falls vorhanden
    if logo:
        try:
            logo = Image.open(logo_pfad).convert("RGBA")  # Konvertiere das Logo in RGBA
            logo_width, logo_height = logo.size

            # Skalieren des Logos proportional, basierend auf dem kleineren Wert von Breite oder Höhe des Originalbildes
            scale_factor = min(width, height) * (logo_percentage / 100)
            aspect_ratio = logo_width / logo_height
            new_logo_width = int(scale_factor * aspect_ratio)
            new_logo_height = int(scale_factor)

            logo = logo.resize((new_logo_width, new_logo_height))

            # Positionierung des Logos (unten rechts)
            position = (new_width - logo.width - border_size, new_height - logo.height - border_size)
            new_image.paste(logo, position, logo)  # Verwende das Logo als Maske
        except Exception as e:
            st.error(f"Chyba při přidávání loga: {e}", "kontaktujte mě na tadeas.reindl@gmail.com ")

    return new_image


if st.button("Upravit obrázky"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_with_frame = add_split_frame(image, add_logo, logo_percentage)  # Logo hinzufügen, wenn ausgewählt

            # Bild im Speicher speichern
            img_bytes = BytesIO()
            image_with_frame.save(img_bytes, format=image.format)
            img_bytes = img_bytes.getvalue()

            # Download-Button für jedes bearbeitete Bild
            st.download_button(
                label=f"Download {uploaded_file.name}",
                data=img_bytes,
                file_name=f"framed_{uploaded_file.name}",
                mime=f"image/{image.format.lower()}",
            )
    else:
        st.warning("Nejprve prosím nahrajte obrázky.")
