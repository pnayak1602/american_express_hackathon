import numpy as np
import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from keras import backend as K
import subprocess
import streamlit.components.v1 as components
import pickle
import cv2 
import mtcnn
from architecture import *
from train_v2 import normalize,l2_normalizer
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import cv2
from tensorflow.keras.preprocessing.image import img_to_array
import os
from tensorflow.keras.models import model_from_json
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from test import show_new_page

def main():
    #Load models
    root_dir = os.getcwd()
    # Load Face Detection Model
    face_cascade = cv2.CascadeClassifier("C:/Users/Neha/User-Login-System-Tutorial/MODELS/haarcascade_frontalface_default.xml")
    # Load Anti-Spoofing Model graph
    json_file = open("C:/Users/Neha/User-Login-System-Tutorial/MODELS/antispoofing_model.json",'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load antispoofing model weights 
    model.load_weights("C:/Users/Neha/User-Login-System-Tutorial/MODELS/final.h5")
    print("Model loaded from disk")
    # video.open("http://192.168.1.101:8080/video")
    # vs = VideoStream(src=0).start()
    # time.sleep(2.0)

    st.title("👦🏻Face Liveness Detection")

    detection=st.button("Start Face Detection")
    label_count = 0 
    if detection:
        st.subheader("Look into the camera: ")
        video = cv2.VideoCapture(0)
        label_list = []
        
        frame_count = 0
        while (label_count!=100):
            try:
                ret,frame = video.read()
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in faces:  
                    face = frame[y-5:y+h+5,x-5:x+w+5]
                    resized_face = cv2.resize(face,(160,160))
                    resized_face = resized_face.astype("float") / 255.0
                    # resized_face = img_to_array(resized_face)
                    resized_face = np.expand_dims(resized_face, axis=0)
                    # pass the face ROI through the trained liveness detector
                    # model to determine if the face is "real" or "fake"
                    preds = model.predict(resized_face)[0]
                    print(preds)
                    if preds> 0.5:
                        label = 'spoof'
                        cv2.putText(frame, label, (x,y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                        cv2.rectangle(frame, (x, y), (x+w,y+h),
                            (0, 0, 255), 2)
                    else:
                        label = 'real'
                        cv2.putText(frame, label, (x,y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                        cv2.rectangle(frame, (x, y), (x+w,y+h),
                        (0, 255, 0), 2)
                    label_list.append(label)
                    label_count=len(label_list)
                    cv2.imshow('frame', frame)
                    if label_count==100:
                        video.release()        
                        cv2.destroyAllWindows()
                        break        
                # if label_count==100:
                #     st.markdown(label_list)
                #     break  
            except Exception as e:
                pass

        label_count = sum(1 for l in label_list if l == 'real')
        st.markdown(label_count)
        st.markdown(label_list)            
        if label_count >= 80:
            show_new_page()

def show_new_page():
    subprocess.run(['python', 'C:/Users/Neha/User-Login-System-Tutorial/Face-recognition-Using-Facenet-On-Tensorflow-2.X/detect.py'])



if __name__ == '__main__':
    main()
        
