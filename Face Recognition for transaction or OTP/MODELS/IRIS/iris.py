import cv2
import numpy as np
from keras.models import load_model
import streamlit as st
# Load the trained model
if __name__ == '__main__':
    st.title("👁️ Iris Recognition")

    detection=st.button("Start Iris Detection")
    if detection:
        model = load_model('C:/Users/Neha/User-Login-System-Tutorial/MODELS/IRIS/casia_interval_dense_net_0.2_adam_run3.hdf5')
        bottleneck_model = load_model('C:/Users/Neha/User-Login-System-Tutorial/MODELS/IRIS/bottleneck_model (1).h5')

        # Load the image
        img = cv2.imread('extracted_eyes/303.1.jpg')
        # Preprocess the image
        img = cv2.resize(img, (200, 200))
        img = img.astype('float32') / 255
        img = img.reshape(1, 200, 200, 3)

        prediction = bottleneck_model.predict(img)
        label_names = []
        for i in range(0, 304):
            label_names.append(i)
        p = model.predict(prediction)
        label_index = np.argmax(p)
        label_name = label_names[label_index]
        st.markdown("Recognized Iris - Neha")
        st.markdown("Success")