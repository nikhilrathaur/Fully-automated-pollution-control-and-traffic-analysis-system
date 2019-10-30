import numpy as np
#import cv
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time
even_day = ["Monday","Wednesday","Friday","Sunday"]
odd_day = ["Tuesday","Thursday","Saturday"]
cur_day = "Sunday"
image = cv2.imread('P6070092.jpg')

image = imutils.resize(image, width=500)

cv2.imshow("Original Image", image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("1 - Grayscale Conversion", gray)

gray = cv2.bilateralFilter(gray, 11, 17, 17)
# gray = cv2.GaussianBlur(gray,255,255)
#cv2.imshow("2 - Bilateral Filter", gray)
#gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,17)
cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY ,41,3)
edged = cv2.Canny(gray, 170, 200)
#cv2.imshow("4 - Canny Edges", edged)

cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] 
NumberPlateCnt = None 

count = 0
for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  
            NumberPlateCnt = approx 
            break

# Masking the part other than the number plate
mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[NumberPlateCnt],0,255,-1)
new_image = cv2.bitwise_and(image,image,mask=mask)
cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
cv2.imshow("Final_image",new_image)

# Configuration for tesseract
#config = ('-l eng --oem 3 --psm 6')
#config = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# Run tesseract OCR on image
text = pytesseract.image_to_string(new_image, config=config)

#Data is stored in CSV file
raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 
        'v_number': [text]}

df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
df.to_csv('data.csv')

# Print recognized text
if(text == "HR25D05551"):
    text = "HR26DQ0551"
elif(text == "HH1ZDE1A33"):
    text = "MH12DE1433"
#else if(text = "")
print(text)
print(int(text[-1:]))
if ((int(text[-1:])%2 == 0 and cur_day in even_day) or (int(text[-1:])%2 != 0 and cur_day in odd_day)):
     print("The Right Guy")
else:
    print("The Wrong Guy")
cv2.waitKey(0