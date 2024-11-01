from PIL import Image, ImageDraw
import os
import streamlit as st
from io import BytesIO

# Pfad zum Ordner für die gespeicherten Bilder mit Rahmen
output_ordner = r'\output'

if not os.path.exists(output_ordner):
    os.makedirs(output_ordner)

# Pfade zu den Logos
logo_pfad1 = r"Logo1.png"  # Ersetze dies mit dem tatsächlichen Pfad zu deinem ersten Logo
logo_pfad2 = r"Logo2.png"  # Ersetze dies mit dem tatsächlichen Pfad zu deinem zweiten Logo

st.title("Generátor fotorámečků")

st.header("Nahrajte obrázky")
uploaded_files = st.file_uploader(
    "Vyberte obrázky", accept_multiple_files=True
)

# Auswahl des Logos und die Position des Logos
selected_logo = st.radio("Wählen Sie ein Logo:", ("Logo 1", "Logo 2"))
logo_pfad = logo_pfad1 if selected_logo == "Logo 1" else logo_pfad2

# Schieberegler für die Logo-Größe (wird nur angezeigt, wenn die Checkbox aktiviert ist)
logo_percentage = st.slider('Velikost loga', min_value=5, max_value=30, value=10)

# Logo-Position auswählen
logo_position = st.selectbox(
    "Position des Logos:",
    ["Oben links", "Oben mitte", "Oben rechts", "Mitte links", "Mitte rechts", "Unten links", "Unten mitte", "Unten rechts"]
)

def add_split_frame(image, logo_path=None, logo_percentage=10, logo_position="Unten rechts"):
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
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")  # Konvertiere das Logo in RGBA
            logo_width, logo_height = logo.size

            # Skalieren des Logos proportional, basierend auf dem kleineren Wert von Breite oder Höhe des Originalbildes
            scale_factor = min(width, height) * (logo_percentage / 100)
            aspect_ratio = logo_width / logo_height
            new_logo_width = int(scale_factor * aspect_ratio)
            new_logo_height = int(scale_factor)

            logo = logo.resize((new_logo_width, new_logo_height))

            # Bestimmen der Position des Logos
            pos_dict = {
                "Oben links": (border_size, border_size),
                "Oben mitte": ((new_width - logo.width) // 2, border_size),
                "Oben rechts": (new_width - logo.width - border_size, border_size),
                "Mitte links": (border_size, (new_height - logo.height) // 2),
                "Mitte rechts": (new_width - logo.width - border_size, (new_height - logo.height) // 2),
                "Unten links": (border_size, new_height - logo.height - border_size),
                "Unten mitte": ((new_width - logo.width) // 2, new_height - logo.height - border_size),
                "Unten rechts": (new_width - logo.width - border_size, new_height - logo.height - border_size),
            }

            position = pos_dict.get(logo_position, (new_width - logo.width - border_size, new_height - logo.height - border_size))

            # Füge das Logo an der gewählten Position ein
            new_image.paste(logo, position, logo)  # Verwende das Logo als Maske
        except Exception as e:
            st.error(f"Chyba při přidávání loga: {e}", "kontaktujte mě na tadeas.reindl@gmail.com ")

    return new_image

if st.button("Upravit obrázky"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_with_frame = add_split_frame(image, logo_pfad, logo_percentage, logo_position)  # Logo hinzufügen, wenn ausgewählt

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

