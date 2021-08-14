import streamlit as st
import io
import requests
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

st.title("顔認識アプリ")

subscription_key = '40dde87bd94b4d96bdedd427171e6f15'
assert subscription_key
face_api_url = 'https://20210812yama.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an image...", type='jpg')

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()  # バイナリデータ取得

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headpose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    res = requests.post(face_api_url, params=params,
                        headers=headers, data=binary_img)

    results = res.json()
    ttfontname = "C:\\Windows\\Fonts\\meiryob.ttc"
    fontsize = 64
    font = ImageFont.truetype(ttfontname, fontsize)
    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'],
                       rect['top']+rect['height'])], fill=None, outline='blue', width=5)
        faceAttributes = result['faceAttributes']
        gender = faceAttributes['gender']
        age = faceAttributes['age']
        draw.text((rect['left'], rect['top'] - 70), gender, font=font)
        draw.text((rect['left'] + 250, rect['top'] - 70),
                  'age={0}'.format(age), font=font)

    st.image(img, caption='Uploaded Image.', use_column_width=True)
