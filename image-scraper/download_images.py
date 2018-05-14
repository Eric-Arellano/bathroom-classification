import os
from pathlib import Path
from typing import List

import cv2
import requests
from selenium import webdriver

Query = str
Url = str
FilePath = str


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
    image_data = download(urls)
    image_data = remove_empty_images(image_data)
    image_data = deduplicate(image_data)
    file_paths = save_images(image_data)
    remove_corrupt_images(file_paths)


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


def download(urls: List[Url]) -> List[bytes]:
    """
    Get image file.
    """

    def get_image(url: Url) -> bytes:
        try:
            print(f'Attempting to download {url}.')
            r = requests.get(url, timeout=45)
            return r.content
        except:
            print(f'Failed...skipping.')

    return [get_image(url) for url in urls]


def remove_empty_images(image_data: List[bytes]) -> List[bytes]:
    """
    Remove any bytes that are None.
    """
    print(f'Size before removing empty images: {len(image_data)}')
    cleaned = [image for image in image_data if image is not None]
    print(f'Size after removing empty images: {len(cleaned)}')
    return cleaned


def deduplicate(image_data: List[bytes]) -> List[bytes]:
    """
    Remove any identical images.
    """
    print(f'Size before de-duplication: {len(image_data)}')
    uniques = []
    for image in image_data:
        if not any(image == unique_image for unique_image in uniques):
            uniques.append(image)
    print(f'Size after de-duplication: {len(uniques)}')
    return uniques


def save_images(image_data: List[bytes]) -> List[FilePath]:
    """
    Save as .jpg files with names indexed from 0 to n.
    """
    current_file_path = Path(os.path.realpath(__file__))
    data_folder = str(current_file_path.parents[1].joinpath('data'))
    file_paths = []
    for index, image in enumerate(image_data):
        file_name = f'{data_folder}/{str(index).zfill(4)}.jpg'
        file_paths.append(file_name)
        with open(file_name, 'wb') as file:
            file.write(image)
    return file_paths


def remove_corrupt_images(file_paths: List[FilePath]) -> None:
    print(f'Size before removing corrupt images: {len(file_paths)}')
    corrupt = [file_path for file_path in file_paths
               if cv2.imread(file_path) is None]
    print(f'Size after removing corrupt images: {len(file_paths) - len(corrupt)}')
    for file in corrupt:
        os.remove(file)


if __name__ == '__main__':
    main()
