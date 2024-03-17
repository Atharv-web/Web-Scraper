from bs4 import BeautifulSoup
import requests
import os
from  urllib.parse import unquote,urljoin


url  = input("Enter the url of the website")
def download_image(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    image_tag = soup.find_all('img') # getting all the image tags

    downloads_path = os.path.join(os.path.expanduser('~'),'downloads')
    num_downloads = 0
    # Downloading the images and saving
    for img_tag in image_tag:
        if num_downloads >= 20:
            break
        img_url = img_tag.get('src')
        if img_url:
            img_url = urljoin(url,img_url)  # joining the whole url if the url is relative
            img_name = os.path.basename(img_url)  # getting rhe image name from url

            img_data = requests.get(img_url).content
            with open(os.path.join(downloads_path,img_name), 'wb') as img_file:
                img_file.write(img_data)
                print(f"Downloaded: {img_name}")

        num_downloads += 1

download_image(url)
