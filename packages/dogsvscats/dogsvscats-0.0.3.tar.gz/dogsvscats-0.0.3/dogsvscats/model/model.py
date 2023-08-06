from torchvision import models
import torch.nn as nn
import torch
from torch.utils import model_zoo
from collections import namedtuple
import time
from dogsvscats import config
from dogsvscats.model.utils import EarlyStopping


MODEL = namedtuple("model", ["url"])

MODELS = {
    "resnet18_2021-01-26": MODEL(
        url="https://github.com/albertoburgosplaza/dogsvscats/releases/download/modelweights-v0.0.1/resnet18_2021-01-26.zip"  # noqa: E501
    )
}


def get_model(checkpoint_path=None, model_name=None):
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    model = model.to(config.DEVICE)

    state_dict = None
    if checkpoint_path:
        state_dict = torch.load(checkpoint_path)
    elif model_name:
        state_dict = model_zoo.load_url(
            MODELS[model_name].url, progress=True, map_location="cpu"
        )

    if state_dict:
        model.load_state_dict(state_dict)

    return model


def train_model(
    model,
    dataloaders,
    dataset_sizes,
    criterion,
    optimizer,
    scheduler,
    num_epochs=config.NUM_EPOCHS,
    earlystopping_patience=config.EARLY_STOPPING_PATIENCE,
    checkpoint_path=config.MODEL_DATA_PATH / "checkpoint.pt",
):
    since = time.time()

    early_stopping = EarlyStopping(
        patience=earlystopping_patience, path=checkpoint_path, verbose=True
    )

    for epoch in range(num_epochs):
        print("Epoch {}/{}".format(epoch, num_epochs - 1))
        print("-" * 10)

        # Each epoch has a training and validation phase
        for phase in ["train", "val"]:

            if phase == "train":
                model.train()  # Set model to training mode
            else:
                model.eval()  # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(config.DEVICE)
                labels = labels.to(config.DEVICE)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == "train":
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print("{} Loss: {:.4f} Acc: {:.4f}".format(phase, epoch_loss, epoch_acc))

            if phase == "val":
                scheduler.step(epoch_loss)
                early_stopping(epoch_loss, model)

        if early_stopping.early_stop:
            print("Early stopping")
            break

    time_elapsed = time.time() - since
    print(
        "Training complete in {:.0f}m {:.0f}s".format(
            time_elapsed // 60, time_elapsed % 60
        )
    )

    # load best model weights
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint)
    return model
