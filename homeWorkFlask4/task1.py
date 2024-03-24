import requests
import os
import time
import threading
import multiprocessing
import asyncio
import aiohttp
import sys


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_name = url.split('/')[-1]
        with open(image_name, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image_name}")
    else:
        print(f"Failed to download image from {url}")


def download_images_multithread(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Total time taken for multithreaded download: {end_time - start_time} seconds")


def download_images_multiprocess(urls):
    start_time = time.time()
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download_image, args=(url,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Total time taken for multiprocess download: {end_time - start_time} seconds")


async def download_image_async(url, session):
    async with session.get(url) as response:
        if response.status == 200:
            image_name = url.split('/')[-1]
            with open(image_name, 'wb') as f:
                f.write(await response.read())
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download image from {url}")


async def download_images_async(urls):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(url, session) for url in urls]
        await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Total time taken for async download: {end_time - start_time} seconds")


if __name__ == "__main__":
    urls = urls = ['https://pikabu.ru/story/prosto_krasivyie_kartinki_4582064',
                   "https://s00.yaplakal.com/pics/pics_original/3/1/2/18833213.jpg"

        ]

    if not urls:
        print("Please provide a list of URLs as command line arguments.")
    else:
        download_images_multithread(urls)
        download_images_multiprocess(urls)
        asyncio.run(download_images_async(urls))