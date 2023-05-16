#Imports
import time
import cv2
from PIL import Image
import numpy as np


# Function to apply watermark and save image:
def apply_watermark(img_path, wm_path, xPosition, yPosition, transparency):
    start = time.time()
    
    #reading images
    img = cv2.imread(img_path)
    wm = cv2.imread(wm_path)
    #print(img,wm)

    #getting image and wm sizes
    h_wm, w_wm, _ = wm.shape
    h_img, w_img, _ = img.shape
    print("img shape:",img.shape," wm shape:", wm.shape)

    #checking that the watermark is smaller than image (both HEIGHT and WIDTH)
    #if the wm is bigger then it will be resized so that both h_wm<h_img/2 and w_wm<w_img/2
    if h_wm > h_img or w_wm > w_img:
        wm = resize_watermark(img,wm)
        print(" resized wm:",wm.shape)
        h_wm, w_wm, _ = wm.shape

    #getting positioning center
    # X
    if xPosition == 'LEFT':
        pos_center_x = int(w_wm/2)
    elif xPosition == 'RIGHT':
        pos_center_x = int(w_img-w_wm/2) #NU MERGE pentru ca destionation are WIDTH mai mica decat wm 
        #print(pos_center_x)
    elif xPosition == 'CENTER':
        pos_center_x = int(w_img/2)
    else:
        print("X positioning wrong argument", xPosition)

    # Y
    if yPosition == 'TOP':
        pos_center_y = int(h_wm/2)
    elif yPosition == 'BOTTOM':
        pos_center_y = int(h_img - h_wm/2)
    elif yPosition == 'CENTER':
        pos_center_y = int(h_img/2)
    else:
        print("Y positioning wrong argument", yPosition)

    print("X:",pos_center_x," Y:",pos_center_y)

    #calculating watermark boundries
    wm_top = pos_center_y - int(h_wm/2)
    wm_bottom = wm_top + h_wm
    wm_left = pos_center_x - int(w_wm/2)
    wm_right = wm_left + w_wm
    print("Boundries: top-",wm_top," bottom-",wm_bottom," left-",wm_left," right-", wm_right)
    
    #applying the watermark
    destination = img[wm_top:wm_bottom, wm_left:wm_right]
    #print(destination.shape, wm.shape)
    result = cv2.addWeighted(destination,transparency, wm, 0.5, 0)

    #saving the watermarked image
    img[wm_top:wm_bottom, wm_left:wm_right] = result

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    end = time.time()
    print("timp:",end - start)

    return img

def apply_text(img_path, text, xPosition, yPosition, transparency):
    #reading images
    img = cv2.imread(img_path)
    print(img.shape)
    #getting sizes
    h_img, w_img, _ = img.shape

    #defining font options
    font = cv2.FONT_HERSHEY_DUPLEX
    font_color = (255, 255, 255)
    thick = 1
    font_size = 0.9
    (text_width, text_height) = cv2.getTextSize(text, font, font_size, thick)[0]
    text_height += 15

    #Creating a mask to insert the text into
    mask = np.zeros((text_height, text_width,3), dtype=np.uint8)
    print(mask.shape)
    mask = cv2.putText(mask,text,(0,20),font,font_size,font_color,thick,cv2.LINE_AA)

    if img.shape[1] < mask.shape[1]:
        mask = cv2.resize(mask, (img.shape[1], text_height))
    
    #getting wm/mask sizes
    wm = mask
    h_wm, w_wm, _ = wm.shape

    #getting positioning center
    # X
    if xPosition == 'LEFT':
        pos_center_x = int(w_wm/2)
    elif xPosition == 'RIGHT':
        pos_center_x = int(w_img-w_wm/2) #NU MERGE pentru ca destionation are WIDTH mai mica decat wm 
        #print(pos_center_x)
    elif xPosition == 'CENTER':
        pos_center_x = int(w_img/2)
    else:
        print("X positioning wrong argument", xPosition)

    # Y
    if yPosition == 'TOP':
        pos_center_y = int(h_wm/2)
    elif yPosition == 'BOTTOM':
        pos_center_y = int(h_img - h_wm/2)
    elif yPosition == 'CENTER':
        pos_center_y = int(h_img/2)
    else:
        print("Y positioning wrong argument", yPosition)

    print("X:",pos_center_x," Y:",pos_center_y)

    #calculating watermark boundries
    wm_top = pos_center_y - int(h_wm/2)
    wm_bottom = wm_top + h_wm
    wm_left = pos_center_x - int(w_wm/2)
    wm_right = wm_left + w_wm
    print("Boundries: top-",wm_top," bottom-",wm_bottom," left-",wm_left," right-", wm_right)
    
    #applying the watermark
    destination = img[wm_top:wm_bottom, wm_left:wm_right]
    #print(destination.shape, wm.shape)
    result = cv2.addWeighted(destination,transparency, wm, 0.5, 0)

    #saving the watermarked image
    img[wm_top:wm_bottom, wm_left:wm_right] = result

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #cv2.imwrite('./images/result_text.png',img)
    return img

def save_img_to_path(img, path):
    img.save(path)

# Function to resize the watermark
def resize_watermark(img, wm):
    resize_ratio = 100

    h_wm, w_wm, _ = wm.shape
    h_img, w_img, _ = img.shape
    #print("Resize FN: img shape:",img.shape," wm shape:", wm.shape)

    if h_wm > h_img:
        print("Bigger height")
        resize_ratio = ((h_img/2)*100)/h_wm

    if w_wm > w_img:
        print("Bigger width")
        if(((w_img/2)*100)/w_wm < resize_ratio):
            resize_ratio = ((w_img/2)*100)/w_wm

    width = int(wm.shape[1] * resize_ratio / 100)
    height = int(wm.shape[0] * resize_ratio / 100)
    dim = (width, height)

    resized = cv2.resize(wm, dim, interpolation = cv2.INTER_AREA)

    return resized

# Function to resize any image based on the width !!!PIL IMAGE
def resize_image_by_width(img, width):

    height = int((img.size[1] * width)/img.size[0])
    dim = (width, height)

    resized = img.resize(dim)

    return resized

def resize_image_by_height(img, height):

    width = int((img.size[0] * height)/img.size[1])
    dim = (width, height)

    resized = img.resize(dim)

    return resized


#apply_watermark('./images/img.png','./images/wm.png','RIGHT','TOP',0.5)
#apply_text('./images/img.png', "text", 'LEFT', "BOTTOM", 0.5)
