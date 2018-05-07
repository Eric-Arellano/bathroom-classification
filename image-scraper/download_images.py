import os
from pathlib import Path
from typing import List

import imutils
import numpy as np
from selenium import webdriver

Query = str
Url = str


def main() -> None:
    urls = get_urls_multiple_queries(['bathroom sign',
                                      'male bathroom sign',
                                      'men bathroom sign',
                                      'female bathroom sign',
                                      'women bathroom sign',
                                      'unisex bathroom sign',
                                      'family bathroom sign',
                                      'ada bathroom sign',
                                      'accessible bathroom sign',
                                      'gender neutral bathroom sign',
                                      'gender inclusive bathroom sign',
                                      'all gender bathroom sign',
                                      ])
    images = download_as_np_arrays(urls)
    images = remove_corrupt_images(images)
    images = deduplicate(images)
    save_as_files(images)


def get_urls_multiple_queries(queries: List[Query]) -> List[Url]:
    """
    Return concatenated URLs of all search results on Google Images for every query.
    """
    distinct_urls = [get_urls(query) for query in queries]
    flattened = [y for x in distinct_urls for y in x]
    print(f'Total image URLs: {len(flattened)}')
    return flattened


def get_urls(query: Query) -> List[Url]:
    """
    Return URLs of all search results on Google Images for query.
    """
    print(f'Getting image URLs for "{query}".')
    # build driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    # get page
    encoded_query = query.replace(' ', '+')
    driver.get(f'https://www.google.com/search?tbm=isch&q={encoded_query}')
    # scrape image URLs
    result = driver.execute_script(r'''
        const nodes = document.querySelectorAll('.rg_di .rg_meta')
        const urls = Array.from(nodes).map(x => JSON.parse(x.textContent).ou).join('\n');
        return urls;
        ''')
    driver.close()
    return result.split('\n')


def download_as_np_arrays(urls: List[Url]) -> List[np.ndarray]:
    """
    Get image and convert to a Numpy array representing the image.
    """

    def get_image(url: Url) -> np.ndarray:
        try:
            print(f'Attempting to download {url}.')
            return imutils.url_to_image(url)
        except:
            print(f'Failed...skipping.')
            pass

    return [get_image(url) for url in urls]


def remove_corrupt_images(images: List[np.ndarray]) -> List[np.ndarray]:
    print(f'Size before removing corrupt images: {len(images)}')
    cleaned = [image for image in images if image is not None]
    print(f'Size after removing corrupt images: {len(cleaned)}')
    return cleaned


def deduplicate(images: List[np.ndarray]) -> List[np.ndarray]:
    """
    Remove any identical images.
    """
    print(f'Size before de-duplication: {len(images)}')
    uniques = []
    for image in images:
        if not any(np.array_equal(image, unique_image) for unique_image in uniques):
            uniques.append(image)
    print(f'Size after de-duplication: {len(uniques)}')
    return uniques


def save_as_files(images: List[np.ndarray]) -> None:
    """
    Save as Numpy files with names indexed from 0 to n.
    """
    current_file_path = Path(os.path.realpath(__file__))
    data_folder = str(current_file_path.parents[1].joinpath('data'))
    for index, image in enumerate(images):
        file_name = f'{data_folder}/{str(index).zfill(4)}.npy'
        np.save(file_name, image)


if __name__ == '__main__':
    main()
