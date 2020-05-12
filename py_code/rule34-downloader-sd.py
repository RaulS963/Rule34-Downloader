import os
import requests
from bs4 import BeautifulSoup
import time
from termcolor import *
import colorama
import re

colorama.init()

def contentpresent(url):
    res = requests.get(url).text
    sf = BeautifulSoup(res, 'lxml')
    content = sf.findAll('span', {'class': 'thumb'})
    if(len(content) != 0):
        return True
    return False

def download_prompt():
    num = input("Enter the no. of images that you want to download?: ")
    if(num.isnumeric() == False):
        cprint("invalid input!",'red')
        num = download_prompt()
    return int(num)
        

def main():
    cprint("==== Welcome to Rule34 downloader ====", 'red')
    print()
    cprint("Rule34 downloader allows you to download all the images present in Rule34.xxx site", 'yellow')
    cprint("Just enter the appropriate tags and it will download all images of that tag into your computer!", 'yellow')
    cprint("For tags follow the same convention that used in Rule34", 'yellow')
    cprint("For more information visit the https://github.com/RaulS963/Rule34-Downloader", 'yellow')
    print()
    prompt_txt = colored("Enter Tags: ",'green')
    print(f"{prompt_txt}",end='')
    tags = input().split()
    print(f'searching tags: {tags}')

    url = f"https://rule34.xxx/index.php?page=post&s=list&tags={'+'.join(tags)}+&pid=0"

    pid = 0
    page = 1
    display_msg = 0
    success_dwnld = 0
    img_array = []
    video_array = []
    print("searching...")
    while(contentpresent(url)):
        if(display_msg == 0):
            print()
            cprint("searching for image links....", "cyan")
            cprint("This process might take 2-3 mins to complete", "cyan")
            cprint("please be patient..", "cyan")
            print()
            display_msg += 1

        print(f'collecting images from page = {page} | pid = {pid}')
        res = requests.get(url).text
        soup = BeautifulSoup(res, 'lxml')
        thumbnails = soup.findAll("span", {'class': 'thumb'})
        temp_array = []
        temp_vid_array = []
        for i in thumbnails:
            link = f"https://rule34.xxx/{i.a['href']}"
            # main image
            main = requests.get(link).text
            soupf = BeautifulSoup(main, 'lxml')
            #find images/gifs
            try:
                img_url = soupf.find('img', {'id': 'image'})['src']
                temp_array.append(img_url)
            except:
                pass
            #find videos
            try:
                video_url = soupf.find("source",{'type':'video/mp4'})['src']
                temp_vid_array.append(video_url)
                #posts.append(Post(video_url,'video'))
            except:
                pass        
          
        
        pid = pid + len(temp_array)
        img_array.extend(temp_array)
        video_array.extend(temp_vid_array)
        print(f"page {page} done!",end=' ')
        cprint(f"[ total file count: {len(img_array) + len(video_array)} ; image: {len(img_array)} ; videos: {len(video_array)} ]",'magenta')
        url = f"https://rule34.xxx/index.php?page=post&s=list&tags={'+'.join(tags)}+&pid={pid}"
        page += 1
    
    #image-search over
    #image download begins
    print()
    count = 1
    if(len(img_array) == 0):
        cprint("== OOPSie!! ==",'red')
        cprint(">>> no images found with those tags!",'red')
        cprint(">>> Try with other tags",'red')
        cprint(">>> Or check the spellings",'red')
    else:
        total_images_count = len(img_array)
        print(f'{total_images_count} images detected!')
        if(total_images_count >= 150):
            cprint("Wow!! thats a lot of images!",'yellow')
            cprint("You can download all images [or] download limited no. of images",'yellow')
            txt = colored(f'Do you want to download all {total_images_count} files? (y/n): ','yellow')
            print(txt,end='')
            choice = input()
            if(choice.lower() == 'n'):
                num = download_prompt()
                img_array = img_array[:num]
                
        for img_url in img_array:
            f_ext = '.jpg'
            if('.png' in img_url):
                f_ext = '.png'
            elif('.jpeg' in img_url):
                f_ext = '.jpeg'
            elif('.gif' in img_url):
                f_ext = '.gif'
            
            img_url = img_url.split('?')[0]
            byte_data = requests.get(img_url).content
            if(os.path.isdir('rule34 images') == False):
                os.makedirs('rule34 images')
                print("created new directory 'rule34 images'!")
            try:
                file_name = 'rule34 images/' + str(time.time())[:-4] + f_ext
                f = open(file_name,'wb')
                f.write(byte_data)
                print(f"[{count}/{len(img_array)}] {img_url}  downloaded!")
                success_dwnld += 1
                count += 1
            except:
                print(f"{img_url}  an error occured!")
            finally:
                f.close()
        print(f"{success_dwnld} of {len(img_array)} images downloaded successfully")
        

while(True):
    main()
    print()
    cprint("Ready for another round!",'yellow')
    cprint("You can download more images by continuing..",'yellow')
    print()
    ch = input("Enter [c] to continue; else any other key to exit: ")
    if(ch.lower() != 'c'):
        break
    os.system('cls')



