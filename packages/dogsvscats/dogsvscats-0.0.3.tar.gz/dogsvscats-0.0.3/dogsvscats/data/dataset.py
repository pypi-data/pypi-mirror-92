from torch.utils.data import Dataset
import pandas as pd
import os
import re
from typing import Any, Dict, Tuple
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from torchvision import transforms
from dogsvscats import config

default_tfs = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


def df_from_dir_files(directory_path, pattern=None):
    """
    Returns a Pandas DataFrame from the files inside a directory. If
    pattern is set, labels are extracted from file names.
    """
    data = list()

    files = [f.name for f in os.scandir(directory_path) if f.is_file()]
    for f in files:
        path = os.path.join(os.path.abspath(directory_path), f)
        if pattern is not None:
            label = re.search(pattern, f).group(1)
            data.append((f, path, label))
        else:
            data.append((f, path))

    if pattern is not None:
        df = pd.DataFrame(data, columns=["filename", "path", "label"])
    else:
        df = pd.DataFrame(data, columns=["filename", "path"])

    return df


def pil_loader(path: str) -> Image.Image:
    with open(path, "rb") as f:
        img = Image.open(f)
        return img.convert("RGB")


class DataFrameDataset(Dataset):
    def __init__(self, df: pd.DataFrame, transform=None):
        self.df = df
        self.transform = transform
        self.classes = config.CLASSES
        inv_classes = {v: k for k, v in self.classes.items()}
        self.df.label = self.df.label.map(inv_classes)

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        path = self.df.loc[idx, "path"]
        target = self.df.loc[idx, "label"]
        sample = pil_loader(path)
        if self.transform is not None:
            sample = self.transform(sample)

        return sample, target


def get_datasets(
    val_size: float = 0.1,
    sample_size: float = 1,
    train_tfs=default_tfs,
    val_tfs=default_tfs,
) -> Dict:
    df = df_from_dir_files(config.TRAIN_DATA_PATH, pattern="([a-z]+)")

    val_size = val_size * sample_size
    train_size = sample_size - val_size

    X_train, X_val, y_train, y_val = train_test_split(
        df.drop(columns=["label"]),
        df.label,
        test_size=val_size,
        train_size=train_size,
        stratify=df.label,
    )

    train_df = pd.concat([X_train, y_train], axis="columns").reset_index(drop=True)
    val_df = pd.concat([X_val, y_val], axis="columns").reset_index(drop=True)

    train_ds = DataFrameDataset(train_df, transform=train_tfs)
    val_ds = DataFrameDataset(val_df, transform=val_tfs)

    return {"train": train_ds, "val": val_ds}


def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
