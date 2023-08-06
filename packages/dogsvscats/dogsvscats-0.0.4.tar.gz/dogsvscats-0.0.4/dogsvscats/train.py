import torch.optim as optim
import torch.nn as nn
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader
from dogsvscats.model.model import train_model, get_model
from dogsvscats.data.transforms import train_tfs, val_tfs
from dogsvscats.data.dataset import get_datasets
from dogsvscats import config


image_datasets = get_datasets(
    sample_size=config.SAMPLE_SIZE,
    train_tfs=train_tfs,
    val_tfs=val_tfs,
)

dataloaders = {
    x: DataLoader(
        image_datasets[x],
        batch_size=config.BS,
        shuffle=True,
        num_workers=config.NW,
    )
    for x in ["train", "val"]
}

dataset_sizes = {x: len(image_datasets[x]) for x in ["train", "val"]}
class_names = image_datasets["train"].classes

model = get_model()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=config.LR, momentum=0.9)
scheduler = lr_scheduler.ReduceLROnPlateau(
    optimizer, patience=config.SCHEDULER_PATIENCE, verbose=True
)

model = train_model(
    model,
    dataloaders,
    dataset_sizes,
    criterion,
    optimizer,
    scheduler,
)
