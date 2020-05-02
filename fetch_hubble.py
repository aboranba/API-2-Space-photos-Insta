import requests
from pathlib import Path
import os

def download_image(url,file_name,folder_name):
  Path(folder_name).mkdir(parents=True, exist_ok=True)
  response = requests.get(url)
  response.raise_for_status()
  with open(f'{folder_name}/{file_name}', 'wb') as file:
      file.write(response.content)

def get_extension(url):
  extension = url.replace('.', ' ').split()[-1]
  return extension

def fetch_hubble_image(image_id):
  response = requests.get(f'http://hubblesite.org/api/v3/image/{image_id}')
  response.raise_for_status()
  images = response.json()['image_files']
  last_image_raw_url = f'https://{images[-1]["file_url"][2:]}'
  download_image(last_image_raw_url,f'{image_id}.{get_extension(last_image_raw_url)}','images')

def fetch_hubble_collection():
  payload = {"page":"all", "collection_name":"wallpaper"}
  response = requests.get(f'http://hubblesite.org/api/v3/images', params=payload) 
  response.raise_for_status()
  imgs = response.json()
  for img in imgs:
    fetch_hubble_image(img['id'])

if __name__ == '__main__':
    fetch_hubble_collection()