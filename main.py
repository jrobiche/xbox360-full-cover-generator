#!/usr/bin/env python3

import argparse
from pathlib import Path
from covergeneratorpackage import create_fullcover_image


def parseargs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Full Cover Generator",
        description="Generate a full cover from a set of text and images.",
    )
    # parser.add_argument("title", type=str, help="game title")
    parser.add_argument("outfile", type=Path, help="location to save generated cover")
    default_category = "game"
    parser.add_argument(
        "--category",
        default=default_category,
        choices=[
            "arcade",
            "homebrew",
            "game",
            "indie",
            "kinect",
            "xbox",
            "xbox360",
        ],
        help=f"game category to determine which banner to use. Defaults to '{default_category}'",
        type=str,
    )
    parser.add_argument(
        "--title",
        help="game title",
        metavar="TEXT",
        type=str,
    )
    parser.add_argument(
        "--title-file",
        help="file containing game title",
        metavar="FILE",
        type=Path,
    )
    parser.add_argument(
        "--description",
        help="game description",
        metavar="TEXT",
        type=str,
    )
    parser.add_argument(
        "--description-file",
        help="file containing game description",
        metavar="FILE",
        type=Path,
    )
    parser.add_argument(
        "--front-boxart",
        help="image to use as the boxart on the front cover",
        metavar="FILE",
        type=Path,
    )
    default_front_boxart_denoise = 0
    parser.add_argument(
        "--front-boxart-denoise",
        choices=[-1, 0, 1, 2, 3],
        default=default_front_boxart_denoise,
        help=(
            "(Requires waifu2x) denoise boxart used on the front cover."
            f" Defaults to '{default_front_boxart_denoise}'"
        ),
        type=int,
    )
    default_front_boxart_scale = 1
    parser.add_argument(
        "--front-boxart-scale",
        choices=[1, 2, 4, 8, 16, 32],
        default=default_front_boxart_scale,
        help=(
            "(Requires waifu2x) scale boxart used on the front cover."
            f" Defaults to '{default_front_boxart_scale}'"
        ),
        type=int,
    )
    parser.add_argument(
        "--rear-background",
        help="image to use as the background on the rear cover",
        metavar="FILE",
        type=Path,
    )
    parser.add_argument(
        "--rear-banner",
        help="image to use as the banner on the rear cover",
        metavar="FILE",
        type=Path,
    )
    parser.add_argument(
        "--rear-screenshot",
        help="image to use as the screenshot on the rear cover",
        metavar="FILE",
        type=Path,
    )
    return parser.parse_args()


def main() -> None:
    args = parseargs()
    title = ""
    if args.title is not None:
        title = args.title
    elif args.title_file is not None:
        with open(args.title_file, "r", encoding="utf-8") as file:
            title = file.read()
    description = ""
    if args.description is not None:
        description = args.description
    elif args.description_file is not None:
        with open(args.description_file, "r", encoding="utf-8") as file:
            description = file.read()
    cover = create_fullcover_image(
        args.category,
        title,
        description,
        backgroundpath=args.rear_background,
        bannerpath=args.rear_banner,
        boxartdenoise=args.front_boxart_denoise,
        boxartpath=args.front_boxart,
        boxartscale=args.front_boxart_scale,
        screenshotpath=args.rear_screenshot,
    )
    cover.save(args.outfile, quality=100)


if __name__ == "__main__":
    main()
