from enum import Enum

import aiohttp
import aiofiles
import asyncio
import requests
from pathlib import Path
import time


class FileType(Enum):
    TEXT = 1
    IMAGE = 2


def make_file_name_(
    url: str, file_type: FileType = FileType.TEXT, target_dir: str = "."
) -> str:
    """
    Генерирует имя файла для сохранения на диск
    """
    abs_path_to_dir = Path().absolute() / Path(target_dir)
    if not abs_path_to_dir.is_dir():
        abs_path_to_dir.mkdir()
    match file_type:
        case FileType.TEXT:
            file_name = (
                f'{url[8:].rstrip("/").replace("/", "__").replace(".", "_")}.html'
            )
        case FileType.IMAGE:
            file_name = url.split("/")[-1]
    return abs_path_to_dir / file_name


def load_file_by_url(
    url: str, file_type: FileType = FileType.TEXT, target_dir: str = "."
) -> None:
    """
    Синхронно загружает файл по url и сохраняет его на диск в папку target_dir
    Если target_dir не существует, она создается
    """
    func_start_time = time.time()

    response = requests.get(url)

    match file_type:
        case FileType.TEXT:
            data = response.text
            mode = "w"
        case FileType.IMAGE:
            data = response.content
            mode = "wb"

    file_name = make_file_name_(url, file_type, target_dir)
    with open(file_name, mode=mode) as f:
        f.write(data)
    print(
        f"Data {url} saved to {file_name} in {time.time() - func_start_time:0.2f} sec."
    )


async def aload_file_by_url(
    url: str, file_type: FileType = FileType.TEXT, target_dir: str = "."
) -> None:
    """
    Асинхронно загружает файл по url и сохраняет его на диск в папку target_dir
    Если target_dir не существует, она создается
    """
    async with aiohttp.ClientSession() as session:
        func_start_time = time.time()
        async with session.get(url) as response:
            match file_type:
                case FileType.TEXT:
                    data = await response.text()
                    mode = "w"
                case FileType.IMAGE:
                    data = await response.read()
                    mode = "wb"

            file_name = make_file_name_(url, file_type, target_dir)
            async with aiofiles.open(file_name, mode=mode) as f:
                await f.write(data)
            print(
                f"Data {url} saved to {file_name} in {time.time() - func_start_time:0.2f} sec."
            )


async def main():
    url_1 = "https://www.geeksforgeeks.org/wp-content/uploads/gq/2014/01/QuickSort2.png"
    url_2 = "https://habr.com/ru/all/"
    tasks = []
    t1 = asyncio.create_task(
        aload_file_by_url(url_1, file_type=FileType.IMAGE, target_dir="tmp")
    )
    t2 = asyncio.create_task(aload_file_by_url(url_2, target_dir="tmp"))
    tasks.append(t1)
    tasks.append(t2)
    await asyncio.gather(*tasks)


start_time = time.time()

if __name__ == "__main__":
    asyncio.run(main())
    print(f"All done in {time.time() - start_time:0.2f} sec.")
