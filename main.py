from PIL import Image, ImageOps, ImageDraw
import os

# Pfad zum Ordner mit den Bildern
ordner_pfad = r'C:\Users\tadea\Downloads\FotoMarek'
# Pfad zum Ordner für die gespeicherten Bilder mit Rahmen
output_ordner = r'C:\Users\tadea\Downloads\FotoMarekNovy'

# Wenn der Ausgabepfad nicht existiert, wird er erstellt
if not os.path.exists(output_ordner):
    os.makedirs(output_ordner)

# Funktion, um den geteilten Rahmen hinzuzufügen
def add_split_frame(image, left_color, right_color):
    border_size = 8
    width, height = image.size

    # Neue Größe des Bildes mit Rahmen
    new_width = width + 2 * border_size
    new_height = height + 2 * border_size

    # Neues Bild mit dem Rahmen
    new_image = Image.new("RGB", (new_width, new_height), left_color)
    draw = ImageDraw.Draw(new_image)

    # Rechte Hälfte des Rahmens (rechts, unten)
    draw.rectangle([new_width // 2, 0, new_width, border_size], fill=right_color)  # oberer Rahmen (rechts)
    draw.rectangle([new_width // 2, new_height - border_size, new_width, new_height], fill=right_color)  # unterer Rahmen (rechts)
    draw.rectangle([new_width - border_size, 0, new_width, new_height], fill=right_color)  # rechter Rahmen

    # Füge das Originalbild in die Mitte des neuen Bildes ein
    new_image.paste(image, (border_size, border_size))

    return new_image

# Gehe durch den Ordner und bearbeite jedes Bild
for filename in os.listdir(ordner_pfad):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        bild_pfad = os.path.join(ordner_pfad, filename)
        image = Image.open(bild_pfad)

        # Definiere die Farben mit Hex-Codes
        left_color = "#FFFFFF"  # Weiß
        right_color = "#004f85"  # Blau

        # Füge den geteilten Rahmen hinzu
        image_with_frame = add_split_frame(image, left_color, right_color)

        # Speichere das Bild mit Rahmen im Ausgabeordner
        output_path = os.path.join(output_ordner, filename)
        image_with_frame.save(output_path)

print("Alle Bilder wurden erfolgreich mit einem Rahmen versehen.")
