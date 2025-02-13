import time
import pygame as pg
from PIL import Image
import numpy as np
import os
import sys


def ascii_pixel(r: int, g: int, b: int, sign: str = " ") -> str:
    """
    Generates a string to display a pixel in the terminal with a specified background and character.

    :param r: int - red color value (0-255)
    :param g: int - green color value (0-255)
    :param b: int - blue color value (0-255)
    :param sign: str - character to be displayed (default is a space)
    :return: str - string with ANSI code for colored background and character
    """
    return f"\033[48;2;{r};{g};{b}m {sign} \033[0m"


def compress_image(input_path, output_path, max_size):
    with Image.open(input_path) as img:
        img.thumbnail(max_size)
        img.save(output_path)


def PrintImg2Terminal(image_path__: str, cell_mode: int = 0) -> str or None:
    term_picture: str = ""

    if not os.path.exists(image_path__):
        print(f"File not found: {image_path__}")
        return None

    try:
        img_array = np.array(Image.open(image_path__).convert("RGB"))

        sign_: str = " "
        if cell_mode == 1:
            sign_ = "."
        elif cell_mode == 2:
            sign_ = "+"
        elif cell_mode == 3:
            sign_ = "*"
        elif cell_mode == 4:
            sign_ = "x"
        elif cell_mode == 5:
            sign_ = "!"

        for row in img_array:
            term_picture += f"{''.join(ascii_pixel(r, g, b, sign_) for r, g, b in row)}\n"
        return term_picture
    except Exception as e:
        print(f"Error preparing the image: {e}")
        return None


def PrintGIF2Terminal(gif_path: str, max_size=(64, 64), cell_mode: int = 0) -> list[str] or None:
    frames = []

    with Image.open(gif_path) as gif:
        try:
            while True:
                temp_frame_path = 'temp_frame.png'
                gif.save(temp_frame_path)

                compressed_frame_path = 'compressed_frame.png'
                compress_image(temp_frame_path, compressed_frame_path, max_size)

                terminal_representation = PrintImg2Terminal(compressed_frame_path, cell_mode)
                if terminal_representation is not None:
                    frames.append(terminal_representation)

                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

    return frames


def main() -> int:
    if len(sys.argv) != 6:
        print(
            f"Usage: python {sys.argv[0]} <path_for_gif> <path_for_music> <delay> <compress_size_x> <compress_size_y> ")
        sys.exit(1)
    else:
        gif_path = sys.argv[1]
        music_path = str(sys.argv[2]).upper()
        delay = float(sys.argv[3])
        compress_size_x = int(sys.argv[4])
        compress_size_y = int(sys.argv[5])

    os.system("cls") if os.name == "nt" else os.system("clear")
    print("Please, wait..")

    gif = PrintGIF2Terminal(gif_path, (compress_size_x, compress_size_y))

    if music_path != "NONE":
        pg.mixer.init()
        pg.mixer.music.load(music_path)
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.15)

    while True:
        os.system("cls") if os.name == "nt" else os.system("clear")
        for frame in gif:
            print(frame)
            if delay > 0:
                time.sleep(delay)
            os.system("cls") if os.name == "nt" else os.system("clear")


if __name__ == "__main__":
    main()
