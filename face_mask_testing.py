import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import json


# Model reconstruction from JSON file
with open(r"C:\Users\t2001\OneDrive\Desktop\ISB 2021\IOT with ML\FMD project\FMD ml model output\model_architecture_FaceMask_Detection.json", 'r') as f:
    model=model_from_json(f.read())

# Load weights into the new model
model.load_weights(r"C:\Users\t2001\OneDrive\Desktop\ISB 2021\IOT with ML\FMD project\FMD ml model output\FaceMask_Detection_weights.h5")

#model.summary()

# Model testing
import cv2
import numpy as np

label_1 = {0:"Covid Safe",1:"Covid Unsafe"}
label_2 = {0:"With Mask",1:"Without Mask"}
color_label = {0: (0,255,0),1 : (0,0,255)}

cap = cv2.VideoCapture(0) 

cascade = cv2.CascadeClassifier(r'C:\Users\t2001\OneDrive\Desktop\ISB 2021\IOT with ML\FMD project\haarcascade_frontalface_default.xml')


while True:
    (rval, frame) = cap.read()
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray,1.1,4)
    
    for x,y,w,h in faces:
        face_image = frame[y:y+h,x:x+w]
        resize_img  = cv2.resize(face_image,(150,150))
        normalized = resize_img/255.0
        reshape = np.reshape(normalized,(1,150,150,3))
        reshape = np.vstack([reshape])
        result = model.predict(reshape)
        result = result[0][0]
        
        if result <= 0.5:
            #with mask
            cv2.rectangle(frame,(x,y),(x+w,y+h),color_label[0],3)
            cv2.rectangle(frame,(x,y-50),(x+w,y),color_label[0],-1)
            cv2.putText(frame,label_1[0],(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.rectangle(frame,(x,y-100),(x+w,y-50),color_label[0],-1)
            cv2.putText(frame,label_2[0],(x,y-60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,25,250),2)

            
        elif result > 0.5:
            #without mask
            cv2.rectangle(frame,(x,y),(x+w,y+h),color_label[1],3)
            cv2.rectangle(frame,(x,y-50),(x+w,y),color_label[1],-1)
            cv2.putText(frame,label_1[1],(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            cv2.rectangle(frame,(x,y-100),(x+w,y-50),color_label[1],-1)
            cv2.putText(frame,label_2[1],(x,y-60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,250,25),2)
            
            
    cv2.imshow('LIVE',   frame)
    key = cv2.waitKey(10)
    
    if key==27:
        break

cap.release()

cv2.destroyAllWindows()
