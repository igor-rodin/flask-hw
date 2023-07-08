import threading
import time
from model import load_file_by_url, FileType


def thread_load(
    urls: list[str], file_type: FileType = FileType.TEXT, target_dir="."
) -> None:
    """
    Загружает и сохраняет на диск список urls с использованием многопоточности
    """
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(
            target=load_file_by_url, args=[url, file_type, target_dir]
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Общее время загрузки {time.time() - start_time:0.2f} сек.")


if __name__ == "__main__":
    urls = [
        "https://www.google.ru/",
        "https://gb.ru/",
        "https://ya.ru/",
        "https://www.python.org/",
        "https://dev.to/listings",
    ]

    urls_img = [
        "https://img.freepik.com/premium-photo/marbled-greek-goddess-with-gold-headdress_52683-102859.jpg",
        "https://img.freepik.com/premium-photo/realistic-mouth-lips-with-melting-effect_52683-105398.jpg",
        "https://img.freepik.com/premium-photo/toy-rabbit-jacket-riding-mini-motorcycle-created-with-generative-ai-technology_746009-172.jpg",
        "https://img.freepik.com/free-photo/children-s-fantasy-tale-with-bison_23-2150165796.jpg",
        "https://habrastorage.org/r/w780/getpro/habr/upload_files/9f2/693/0b3/9f26930b3a1ac0050181c9eb4b3da366.jpeg",
        "https://habrastorage.org/r/w780/getpro/habr/upload_files/318/e82/980/318e82980552281a11475db39f1f5932.jpeg",
    ]

    thread_load(urls, file_type=FileType.TEXT, target_dir="tmp")
