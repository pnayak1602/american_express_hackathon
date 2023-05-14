import numpy as np
import streamlit as st
import pandas as pd
import subprocess
from architecture import *
import os
from tensorflow.keras.models import model_from_json
from keras.applications.inception_resnet_v2 import InceptionResNetV2
def show_new_page():
    if st.button('NEXT'):
        subprocess.run(['python', 'C:/Users/Neha/User-Login-System-Tutorial/Face-recognition-Using-Facenet-On-Tensorflow-2.X/detect.py'])

    
    
