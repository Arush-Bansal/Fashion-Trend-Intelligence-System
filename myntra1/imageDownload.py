import requests
import os

def saveImage(image_url, imageTitle):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(f"images/{imageTitle}.jpg", 'wb') as file:
        file.write(response.content)
    print(f"Image saved as {imageTitle}")
