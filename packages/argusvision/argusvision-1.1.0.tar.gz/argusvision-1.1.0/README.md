# Argus Vision

argusvision package provides easy to use access to image embedding models pretrained on Bing data - Argus Vision models.
Interface is based on popular torchvision.

In version 1.0, supported model is Argus Vision V6 - resnext101 32x8d

Please note that provided models are offering image embeddings
## Installation
``pip install argusvision``

For Windows, torch needs to be install from wheel file.
Please download the latest torch from here: https://download.pytorch.org/whl/torch_stable.html
and then install it using: pip install <.whl file>

## Usage
Input images should be in <b>BGR</b> format of shape (3 x H x W), where H and W are expected to be at least 224.
The images have to be loaded in to a range of [0, 1] and then normalized using mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225].

Example script:  
```
import argusvision
import torch

# This will load pretrained model
model = argusvision.models.resnext101_32x8d()

# This will initialize weights with default values
model = argusvision.models.resnext101_32x8d(pretrained=False) 

# Load model to CPU memory, interface is the same as torchvision
model = argusvision.resnext101_32x8d(map_location=torch.device('cpu')) 
```

Example of creating image embeddings:
```
import argusvision
from torchvision import transforms
import torch
from PIL import Image

def get_image():
    img = cv2.imread('example.jpg', cv2.IMREAD_COLOR)
    img = cv2.resize(img, (256, 256))
    img = img[16:256-16, 16:256-16]
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return preprocess(image).unsqueeze(0) # Unsqueeze only required when there's 1 image in images batch

model = argusvision.models.resnext101_32x8d(map_location=torch.device('cpu'))
features = model(get_image())
print(features.shape)
```
Should output
```
...
torch.Size([1, 2048])
```
### Benchmarks
Here are the evaluations of the popular datasets  
Model | CIFAR-10 | STL-10
--- | --- | ---
Torchvision, ResNext101 32x8d | 90% | 81.1%
Argusvision, ResNext101 32x8d | 92.6% | 84.2%
