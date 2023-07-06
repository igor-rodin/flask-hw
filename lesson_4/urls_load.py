import argparse
import asyncio
from pathlib import Path
from load_asinc import async_load
from load_pr import multiproces_load
from load_th import thread_load
from model import get_urls_from_file, FileType


def run():
    parser = argparse.ArgumentParser(
        description="Скачивает содержимое с заданных URL ресурсов"
    )

    group_source = parser.add_mutually_exclusive_group()
    group_source.add_argument(
        "-l",
        "--list",
        action="store_true",
        default=False,
        help="Источнок URL адресов для скачивания - список, передается в аргументах командной строки",
    )
    group_source.add_argument(
        "-f",
        "--file",
        action="store_true",
        default=True,
        help="Источнок URL адресов для скачивания - текстовый файл с содержимым со списком URL. Используется по умолчанию.",
    )

    parser.add_argument(
        "source", type=str, nargs="+", help="Список URL адресов для скачивания."
    )
    parser.add_argument(
        "-t",
        "--target-dir",
        type=str,
        default=".",
        help="Директория для скачивания. По умолчанию используется текущая",
    )

    parser.add_argument(
        "-r",
        "--resource-type",
        choices=["T", "I"],
        default="T",
        help="Тип ресурса для скачивниая. ('T' - плейн текст, 'I' - изображеиния). По умолчанию - 'T'",
    )

    parser.add_argument(
        "-m",
        "--mode",
        choices=["MT", "MP", "ASYNC"],
        default="ASYNC",
        help="Режим скачивания. ( 'MT' - многопоточный, 'MP' - многопросессорный, 'ASYNC' - асинхронный). По умолчанию используется 'ASYNC'",
    )

    args = parser.parse_args()

    match args.resource_type:
        case "T":
            file_type = FileType.TEXT
        case "I":
            file_type = FileType.IMAGE
    target_dir = args.target_dir
    try:
        urls = args.source if args.list else get_urls_from_file(args.source[0])
        match args.mode:
            case "MT":
                print(" Испульзуется многопоточный режим ".center(80, "*"))
                thread_load(urls, file_type=file_type, target_dir=target_dir)
            case "MP":
                print(" Испульзуется многопроцессорный режим".center(80, "*"))
                multiproces_load(urls, file_type=file_type, target_dir=target_dir)
            case "ASYNC":
                print(" Испульзуется асинхронный режим ".center(80, "*"))
                asyncio.run(
                    async_load(urls, file_type=file_type, target_dir=target_dir)
                )
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    run()
