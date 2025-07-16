import torchvision.transforms as transforms

from models.efficientnet_model import EffModel
from models.resnet_model import ResNet
from models.vision_transformer_model import VITModel


def prepare_photo(pictute):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    return transform(pictute)

def get_answer(prediction):
    if prediction > 0.5:
        return 'Этот мем подходит для группы!'
    else:
        return 'Этот мем не совсем той тематики!'

def predict(model, photo):
    if model == 'resnet':
        model = ResNet()
    elif model == 'efficientnet':
        model = EffModel()
    elif model == 'vit':
        model = VITModel()

    picture = prepare_photo(photo)

    return get_answer(model.forward(picture))