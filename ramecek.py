from PIL import Image, ImageDraw
import os
import streamlit as st
from io import BytesIO

# Pfad zum Ordner für die gespeicherten Bilder mit Rahmen
output_ordner = os.path.join(os.getcwd(), 'output')

if not os.path.exists(output_ordner):
    os.makedirs(output_ordner)

# Pfade zu den Logos
logo_pfad1 = r"Logo_1.png"  # Ersetze dies mit dem tatsächlichen Pfad zu deinem ersten Logo
logo_pfad2 = r"Logo_2.png"  # Ersetze dies mit dem tatsächlichen Pfad zu deinem zweiten Logo

# Lade Logos für die Vorschau
logo1_preview = Image.open(logo_pfad1).resize((50, 50))
logo2_preview = Image.open(logo_pfad2).resize((50, 50))

st.title("Generátor fotorámečků")
st.write("---")  # Horizontale Linie für die Trennung

# Bild-Upload
st.header("Nahrajte obrázky")
uploaded_files = st.file_uploader("Vyberte obrázky", accept_multiple_files=True)

# Initialisiere Session State für ausgewählte Werte
if "selected_logo" not in st.session_state:
    st.session_state["selected_logo"] = None
if "logo_percentage" not in st.session_state:
    st.session_state["logo_percentage"] = 10
if "logo_position" not in st.session_state:
    st.session_state["logo_position"] = "Dole vpravo"

# Auswahl des Logos mit Session State
st.write("### Vyberte logo:")
col1, col2 = st.columns(2)
with col1:
    if st.button("Vybrat logo 1"):
        st.session_state["selected_logo"] = logo_pfad1
        st.image(logo1_preview, caption="Logo 1")
with col2:
    if st.button("Vybrat logo 2"):
        st.session_state["selected_logo"] = logo_pfad2
        st.image(logo2_preview, caption="Logo 2")

# Widgets für Logo-Größe und -Position, die direkt den Session State aktualisieren
st.session_state["logo_percentage"] = st.slider(
    'Velikost loga (v % obrázku)',
    min_value=5,
    max_value=30,
    value=st.session_state["logo_percentage"]
)

st.session_state["logo_position"] = st.selectbox(
    "Umístění loga",
    ["Nahoře vlevo", "Nahoře uprostřed", "Nahoře vpravo", 
     "Uprostřed vlevo", "Uprostřed", "Uprostřed vpravo", 
     "Dole vlevo", "Dole uprostřed", "Dole vpravo"],
    index=["Nahoře vlevo", "Nahoře uprostřed", "Nahoře vpravo", 
           "Uprostřed vlevo", "Uprostřed", "Uprostřed vpravo", 
           "Dole vlevo", "Dole uprostřed", "Dole vpravo"].index(st.session_state["logo_position"])
)

# Verwende Werte aus dem Session State
selected_logo = st.session_state["selected_logo"]
logo_percentage = st.session_state["logo_percentage"]
logo_position = st.session_state["logo_position"]

# Funktion für das Hinzufügen des Rahmens und des Logos
def add_split_frame(image, logo_path=None, logo_percentage=10, logo_position="Dole vpravo"):
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

    # Logo hinzufügen, falls ein gültiger Logo-Pfad angegeben ist
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_width, logo_height = logo.size

            # Skalieren des Logos proportional
            scale_factor = min(width, height) * (logo_percentage / 100)
            aspect_ratio = logo_width / logo_height
            new_logo_width = int(scale_factor * aspect_ratio)
            new_logo_height = int(scale_factor)

            logo = logo.resize((new_logo_width, new_logo_height))

            # Bestimmen der Position des Logos
            pos_dict = {
                "Nahoře vlevo": (border_size, border_size),
                "Nahoře uprostřed": ((new_width - logo.width) // 2, border_size),
                "Nahoře vpravo": (new_width - logo.width - border_size, border_size),
                "Uprostřed vlevo": (border_size, (new_height - logo.height) // 2),
                "Uprostřed": ((new_width - logo.width) // 2, (new_height - logo.height) // 2),
                "Uprostřed vpravo": (new_width - logo.width - border_size, (new_height - logo.height) // 2),
                "Dole vlevo": (border_size, new_height - logo.height - border_size),
                "Dole uprostřed": ((new_width - logo.width) // 2, new_height - logo.height - border_size),
                "Dole vpravo": (new_width - logo.width - border_size, new_height - logo.height - border_size),
            }

            position = pos_dict.get(logo_position, (new_width - logo.width - border_size, new_height - logo.height - border_size))

            # Füge das Logo an der gewählten Position ein
            new_image.paste(logo, position, logo)
        except Exception as e:
            st.error(f"Chyba při přidávání loga: {e}")

    return new_image

# Button zum Bearbeiten und Speichern der Bilder
if st.button("Upravit obrázky"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_with_frame = add_split_frame(image, selected_logo, logo_percentage, logo_position)

            # Bild im Speicher speichern
            img_bytes = BytesIO()
            image_with_frame.save(img_bytes, format=image.format)
            img_bytes = img_bytes.getvalue()

            # Download-Button für jedes bearbeitete Bild
            st.download_button(
                label=f"Stáhnout {uploaded_file.name}",
                data=img_bytes,
                file_name=f"orámovaný_{uploaded_file.name}",
                mime=f"image/{image.format.lower()}",
            )
    else:
        st.warning("Nahrajte prosím nejprve obrázky.")
