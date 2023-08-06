from pathlib import Path
import torch

PROJECT_PATH = Path("/home/alberto/workspace/dogsvscats")
DATA_PATH = PROJECT_PATH / "data"
TRAIN_DATA_PATH = DATA_PATH / "train"
TEST_DATA_PATH = DATA_PATH / "test1"
MODEL_DATA_PATH = DATA_PATH / "model"

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

NUM_EPOCHS = 50
EARLY_STOPPING_PATIENCE = 10
SCHEDULER_PATIENCE = 5
LR = 0.01
BS = 128
NW = 4
SAMPLE_SIZE = 1

CLASSES = {0: "cat", 1: "dog"}
INV_CLASSES = {v: k for k, v in CLASSES.items()}
