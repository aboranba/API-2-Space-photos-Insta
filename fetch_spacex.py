import requests
from pathlib import Path
import os

def download_image(url,file_name,folder_name):
  Path(folder_name).mkdir(parents=True, exist_ok=True)
  response = requests.get(url)
  response.raise_for_status()
  with open(f'{folder_name}/{file_name}', 'wb') as file:
      file.write(response.content)

def fetch_spacex_last_launch():
  response = requests.get('https://api.spacexdata.com/v3/launches/latest')
  response.raise_for_status()
  images = response.json()['links']['flickr_images']
  for image_number, image in enumerate(images):
    file_name = f'spacex{image_number+1}.jpg'
    folder_name = 'images'
    download_image(image,file_name,folder_name)

if __name__ == '__main__':
  fetch_spacex_last_launch()

       