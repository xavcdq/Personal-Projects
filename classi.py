import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
import requests

# Load a pre-trained model
model = models.resnet18(pretrained=True)
model.eval()

# Define the transformation for the input image
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load the labels
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
response = requests.get(LABELS_URL)
labels = response.json()

def predict():
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"], key = "predict")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Preprocess the image
        img_t = transform(image)
        batch_t = torch.unsqueeze(img_t, 0)

        # Make a prediction
        with torch.no_grad():
            out = model(batch_t)
        
        _, index = torch.max(out, 1)
        label = labels[index]
        st.write(f"Prediction: **{label}**")


# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)
    
#     label = predict(image)
#     st.write(f"Prediction: **{label}**")
