import streamlit as st
from PIL import Image, ImageDraw, ImageOps

def add_circle_mask(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    size = (150, 150)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

def main():

    # Ajout de l'image en cercle
    image = add_circle_mask('photo.jpg')
    st.image(image, use_column_width=False, width=150)

    st.title('UrbanMatch')

    # Ajout de texte descriptif
    st.write(" Bienvenue sur l'application UrbainMatch")
    st.write("Cette application vous permettra de voir selon les critères que vous sélectionnez de savoir quelle ville vous convient le plus. N'hésitez pas à naviguer dans les différentes pages de l'application. En espérant pouvoir vous aider a trouver la ville que vous souhaitez. ")

    st.image("photo_ville.jpg",use_column_width=False, width=700)

if __name__ == '__main__':
    main()