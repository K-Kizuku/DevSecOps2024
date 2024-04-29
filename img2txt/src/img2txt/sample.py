import requests
from torchvision.io import read_image
from torchvision.models import resnet50, ResNet50_Weights
import os


def getCategoryName(path):
    img = read_image(path)
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights=weights)
    model.eval()
    preprocess = weights.transforms()
    batch = preprocess(img).unsqueeze(0)
    prediction = model(batch).squeeze(0).softmax(0)
    cid = prediction.argmax().item()
    return category_name = weights.meta["categories"][cid]


file_name = "orange.jpg"
url = f"https://github.com/opencv/opencv/blob/master/samples/data/{file_name}?raw=true"
response = requests.get(url)
blob = response.content

#file_name = 'pepsi.jpeg'
with open(file_name, "wb") as f:
    f.write(blob)

img = read_image(file_name)

