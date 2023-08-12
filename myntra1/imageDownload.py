import os
# import requests

def baseName(url): return  os.path.basename(url)

# def saveImage(image_url):

#     response = requests.get(image_url)

#     if response.status_code == 200:
#         with open(f"./images/{baseName(image_url)}.jpg", "wb") as f:
#             f.write(response.content)
#             print("Image saved successfully.")
#     else:
#         print("Failed to fetch the image.")
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def saveImage(image_url):
    session = requests.Session()

    # Configure retries
    retries = Retry(total=5,
                   backoff_factor=0.1,
                   status_forcelist=[500, 502, 503, 504],
                   method_whitelist=frozenset(['HEAD', 'GET', 'OPTIONS']))

    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # Fetch the image using the session
    response = session.get(image_url)

    if response.status_code == 200:
        with open(f"./images/{baseName(image_url)}.jpg", "wb") as f:
            f.write(response.content)
            print("Image saved successfully.")
    else:
        print("Failed to fetch the image.")

