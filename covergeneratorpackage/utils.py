from math import floor
from os import PathLike
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont


def get_scaled_dimensions_by_height(
    new_height: int, dimensions: tuple[int]
) -> tuple[int]:
    old_width, old_height = dimensions
    new_width = floor(new_height * old_width / old_height)
    return (new_width, new_height)


def get_scaled_dimensions_by_width(
    new_width: int, dimensions: tuple[int]
) -> tuple[int]:
    old_width, old_height = dimensions
    new_height = floor(new_width * old_height / old_width)
    return (new_width, new_height)


def textwrapped(text: str, font: ImageFont, maxwidth: int) -> str:
    text = text.strip()
    draw = ImageDraw.Draw(Image.new(mode="RGB", size=(100, 100)))
    space_width = draw.textlength(text=" ", font=font)
    wrapped_lines = []
    for line in text.split("\n"):
        line_width = draw.textlength(text=line, font=font)
        if line_width <= maxwidth:
            wrapped_lines.append(line)
            continue
        current_line = ""
        current_line_width = 0
        for token in line.split(" "):
            if current_line != "":
                # add space to current line
                current_line += " "
                current_line_width += space_width
            token_width = draw.textlength(text=token, font=font)
            if current_line_width + token_width > maxwidth:
                # start a new line
                wrapped_lines.append(current_line)
                current_line = token
                current_line_width = token_width
            else:
                # add token to current line
                current_line += token
                current_line_width += token_width
        wrapped_lines.append(current_line)
    return "\n".join(wrapped_lines)


def upscaleimage(
    input_path: PathLike | str | bytes,
    output_path: PathLike | str | bytes,
    denoise: int = 0,
    scale: int = 1,
) -> None:
    input_path = Path(input_path).absolute()
    output_path = Path(output_path.absolute())
    input_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    args = [
        "./waifu2x/waifu2x-ncnn-vulkan",
        "-i",
        str(input_path),
        "-o",
        str(output_path),
        "-n",
        str(int(denoise)),
        "-s",
        str(int(scale)),
    ]
    subprocess.run(args, check=True)
