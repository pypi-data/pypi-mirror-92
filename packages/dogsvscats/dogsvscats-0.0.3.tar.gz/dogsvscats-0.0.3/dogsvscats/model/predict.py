import torch
from torchvision import transforms
from dogsvscats import config
from dogsvscats.data.dataset import pil_loader


def predict_image(
    model,
    image_path,
):
    model.eval()

    tfs = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    sample = pil_loader(image_path)
    sample = tfs(sample)
    sample = sample.unsqueeze(0)
    sample = sample.to(config.DEVICE)
    output = model(sample)
    _, preds = torch.max(output, 1)

    return preds.cpu().numpy()[0]
