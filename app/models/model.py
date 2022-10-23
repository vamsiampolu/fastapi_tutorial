from enum import Enum


class ModelName(str, Enum):
    Alexnet = "alexnet"
    Resnet = "resnet"
    Lenet = "lenet"
