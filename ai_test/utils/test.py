import os

print(os.getcwd())
print(os.path.join('images', 'result', 'result.jpg'))


dir = os.path.join('images', 'result', 'result.jpg')

from PIL import Image

img = Image.open(dir)
img.show()