from typing import List, Tuple
from glob import glob

import numpy as np
import cv2

FilePath = str
Classification = Tuple[str, str]


def main() -> None:
    images = load_images()
    classifications = classify_images(images)
    save_as_csv(classifications)


def load_images() -> List[np.ndarray]:
    images = [cv2.imread(file) for file in glob('../data/*.jpg')]
    print(f'Number of images loaded: {len(images)}')
    return images


def classify_images(image_path: List[np.ndarray]) -> List[Classification]:
    cv2.namedWindow()
    cv2.imshow('image', )


def save_as_csv(classifications: List[Classification]) -> None:
    raise NotImplementedError


if __name__ == '__main__':
    main()
