import os
import requests
from bs4 import BeautifulSoup
import time
from termcolor import *
import colorama
import re

colorama.init()

class Post:
	def __init__(self,url,post_type):
		self.url = url
		self.post_type = post_type
	
	def content(self):
		print(self.url)
		print(self.post_type)

def image_ext(url):
	url = re.split('.jpg|.png|.jpeg|.gif',url)[0]
	try:
		res_jpg = requests.get(f"{url}.jpg").content
		if(res_jpg != b'<html>\n<head><title>404 Not Found</title></head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'):
			return f"{url}.jpg"
		res_png = requests.get(f"{url}.png").content
		if(res_png != b'<html>\n<head><title>404 Not Found</title></head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'):
			return f"{url}.png"
		res_jpeg = requests.get(f"{url}.jpeg").content
		if(res_jpeg != b'<html>\n<head><title>404 Not Found</title></head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'):
			return f"{url}.jpeg"
		res_gif = requests.get(f"{url}.gif").content
		if(res_gif != b'<html>\n<head><title>404 Not Found</title></head>\n<body>\n<center><h1>404 Not Found</h1></center>\n<hr><center>nginx</center>\n</body>\n</html>\n'):
			return f"{url}.gif"
	except:
		pass

def contentpresent(url):
    res = requests.get(url).text
    sf = BeautifulSoup(res, 'lxml')
    content = sf.findAll('span', {'class': 'thumb'})
    if(len(content) != 0):
        return True
    return False


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
    posts = []
    print("searching...")
    while(contentpresent(url) and len(img_array) < 50):
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
                if('//samples/' in img_url):
                    img_url = img_url.replace('samples','images')
                    img_url = img_url.replace('sample_','')
                    img_url = img_url.split('?')[0]
                    img_url = image_ext(img_url)
                #posts.append(Post(img_url,'image'))
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
        print(f'{len(img_array)} images detected!')
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