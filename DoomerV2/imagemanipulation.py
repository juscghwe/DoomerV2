import os
from PIL import Image, ImageEnhance

namespace=["wallbloodeye","wallbrick","wallcolumn","wallwhite"]
size = 64

for name in namespace:
    game_folder = os.path.dirname(__file__)
    originalimg = Image.open(f"images/gameobjects/{name}.png")

    ''' Preview for Editor '''
    preview = originalimg.resize((10, 10))
    preview.save(f"images/mapeditor/{name}.png")

    ''' Stripes for Texturing - side==0'''
    for i in range(size):
        cropped = originalimg.crop((i,0,i + 1,size))
        cropped.save(f"images/gameobjects/{name}/{name}{i}.png")

    ''' Stripes for Texturing - side==1'''
    originalenhance = ImageEnhance.Brightness(originalimg)
    darker = originalenhance.enhance(0.5)
    darker.save(f"images/gameobjects/{name}_shadowed.png")

    for i in range(size):
        cropped = darker.crop((i,0,i + 1,size))
        cropped.save(f"images/gameobjects/{name}/{name}{i+size}.png")