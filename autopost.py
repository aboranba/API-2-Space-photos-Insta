import glob
import os
import sys
import time
from io import open
from PIL import Image

sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

def thumbnail_images():
  all_images = os.listdir('images')
  for image in all_images:
    image_name = f'images/{image}'
    image = Image.open(image_name)
    image.thumbnail((1080, 1080*image.size[1]/image.size[0]))
    if image.size[1]>1350:
        coordinates = (0, (image.size[1]-1350)/2, image.width, image.height-(image.size[1]-1350)/2)
        image = image.crop(coordinates)
    image_rgb = image.convert("RGB")
    image_name = image_name.replace('.', ' ').split()[0]
    image_rgb.save(f'{image_name}.jpg', format="JPEG")

if __name__ == '__main__':
    thumbnail_images()

    posted_pic_list = []
    try:
        with open("pics.txt", "r", encoding="utf8") as f:
            posted_pic_list = f.read().splitlines()
    except Exception:
        posted_pic_list = []

    timeout = 3

    bot = Bot()
    bot.login()

    while True:
        folder_path = "./images"
        pics = glob.glob(folder_path + "/*.jpg")
        pics = sorted(pics)
        try:
            for pic in pics:
                if pic in posted_pic_list:
                    continue

                #pic_name = pic[:-4].split("-")
                #pic_name = "-".join(pic_name[1:])
                pic_name = pic[:-4]

                print("upload: " + pic_name)

                description_file = folder_path + "/" + pic_name + ".txt"

                if os.path.isfile(description_file):
                    with open(description_file, "r") as file:
                        caption = file.read()
                else:
                    caption = pic_name#.replace("-", " ")

                bot.upload_photo(pic, caption=caption)
                if bot.api.last_response.status_code != 200:
                    print(bot.api.last_response)
                    # snd msg
                    break

                if pic not in posted_pic_list:
                    posted_pic_list.append(pic)
                    with open("pics.txt", "a", encoding="utf8") as f:
                        f.write(pic + "\n")

                time.sleep(timeout)

        except Exception as e:
            print(str(e))
        time.sleep(60)  