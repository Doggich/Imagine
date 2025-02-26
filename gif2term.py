import time
import pygame as pg
from PIL import Image
import numpy as np
import argparse
import os


def clear_terminal():
    print("\033[H", end='')


def ascii_pixel(r: int, g: int, b: int, sign: str = " ") -> str:
    return f"\033[48;2;{r};{g};{b}m {sign} \033[0m"


def compress_image_in_memory(image: Image.Image, max_size) -> Image.Image:
    image.thumbnail(max_size)
    return image


def PrintImg2Terminal(image: Image.Image) -> str or None:
    term_picture: str = ""

    if image is None:
        print("Invalid image provided.")
        return None

    img_array = np.array(image.convert("RGB"))

    for row in img_array:
        term_picture += ''.join(ascii_pixel(r, g, b) for r, g, b in row) + "\n"

    return term_picture


def PrintGIF2Terminal(gif_path: str, max_size=(64, 64)) -> list[str] or None:
    frames = []

    if not os.path.exists(gif_path):
        print(f"File not found: {gif_path}")
        return None

    with Image.open(gif_path) as gif:
        try:
            while True:

                frame = gif.copy()

                compressed_frame = compress_image_in_memory(frame, max_size)

                terminal_representation = PrintImg2Terminal(compressed_frame)
                if terminal_representation is not None:
                    frames.append(terminal_representation)
                gif.seek(gif.tell() + 1)

        except EOFError:
            pass

    return frames


def main() -> int:
    parser = argparse.ArgumentParser(description="Show .gif file on terminal")

    parser.add_argument("gif_path", type=str, help="Путь к GIF файлу")
    parser.add_argument("music_path", type=str, help="Путь к музыкальному файлу (или 'NONE' для отключения музыки)")
    parser.add_argument("delay", type=float, help="Задержка между кадрами в секундах")
    parser.add_argument("compress_size_x", type=int, help="Размер сжатия по оси X")
    parser.add_argument("compress_size_y", type=int, help="Размер сжатия по оси Y")

    args = parser.parse_args()

    gif_path = args.gif_path
    music_path = args.music_path.upper()
    delay = args.delay
    compress_size_x = args.compress_size_x
    compress_size_y = args.compress_size_y

    os.system("cls")

    clear_terminal()
    print("Please, wait..")

    gif = PrintGIF2Terminal(gif_path, (compress_size_x, compress_size_y))

    if music_path != "NONE":
        pg.mixer.init()
        pg.mixer.music.load(music_path)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.15)

    while True:
        clear_terminal()
        for frame in gif:
            print(frame)
            if delay > 0:
                time.sleep(delay)
            clear_terminal()


if __name__ == "__main__":
    main()
    os.system("cls")
