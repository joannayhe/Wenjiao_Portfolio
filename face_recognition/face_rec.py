#!/usr/bin/env python
# coding: utf-8

# In[1]:


import zipfile

from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!


# In[2]:


# character recognition function
def char_rec(img,wrd):
    #img=img.convert('L')
    text = pytesseract.image_to_string(img)
    #text=text.lower()
    #wrd=wrd.lower()
    found=False
    if wrd in text:
        found=True
    return found

#test=char_rec(img_num,'Christopher')
#print(test)


# In[3]:


# detect faces in the file and creat contact sheet
def detect_faces(img_arr):
    gray = cv.cvtColor(img_arr, cv.COLOR_BGR2GRAY)
    #print(gray)
    faces = face_cascade.detectMultiScale(gray,1.35,4)
    if faces==():
        contact_sheet=Image.new(img.mode,(500,30),color='white')
        d=ImageDraw.Draw(contact_sheet)
        text=d.multiline_text((0,0),'Results found in file {} \nBut there were no faces in that file!'.format(i), fill='black')

    else:
        contact_sheet=Image.new(img.mode,(500,15+100*(faces.shape[0]//5+1)))
        d=ImageDraw.Draw(contact_sheet)
        text=d.text((0,0),'Results found in file {}'.format(i))
        x1=0
        y1=15
        for (x,y,w,h) in faces:
            img_face = img.crop(box=(x,y,x+w,y+h))
            img_face.thumbnail((100,100))
            contact_sheet.paste(img_face,(x1,y1))
            x1=x1+100
            if x1==500:
                y1=y1+100
                x1=0
    display(contact_sheet)

#detect_faces(img_num)


# In[4]:


#open and iterate through objects in zipfile
with zipfile.ZipFile('readonly/small_img.zip','r') as test_zip:
    lst=test_zip.namelist()
    for i in lst:
        img_name=test_zip.open(i)
        img=Image.open(img_name)
        img.save('img.png')
        img_num=cv.imread('img.png')
        #print(img_num)
        check=char_rec(img_num, 'Chris')
        if check:
            detect_faces(img_num)


# In[ ]:


with zipfile.ZipFile('readonly/images.zip','r') as img_zip:
    lst=img_zip.namelist()
    #print(lst)
    for i in lst:
        #i=lst[0]
        img_name=img_zip.open(i)
        img=Image.open(img_name)
        img.save('img.png')
        img_num=cv.imread('img.png')
        #print(img_num)
        check=char_rec(img_num, 'Mark')
        if check:
            detect_faces(img_num)
            


# In[ ]:




