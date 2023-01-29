from os import PathLike
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .utils import get_scaled_dimensions_by_height, textwrapped, upscaleimage


def create_front_cover_image(
    bannerpath: PathLike | str | bytes = None,
    bannertype: str = None,
    boxartdenoise: int = 0,
    boxartpath: PathLike | str | bytes = None,
    boxartscale: int = 1,
) -> Image:
    banner_position = (0, 0)
    banner_size = (425, 75)
    cover_color = (7, 69, 94, 255)
    cover_size = (425, 600)
    if boxartpath is not None:
        upscaled_boxartpath = Path("boxart_upscaled.png")
        # create cover from boxart
        if boxartdenoise != 0 or boxartscale != 1:
            upscaleimage(
                boxartpath,
                upscaled_boxartpath,
                denoise=boxartdenoise,
                scale=boxartscale,
            )
            boxartpath = upscaled_boxartpath
        cover = Image.open(boxartpath)
        cover = cover.resize(cover_size)
        # delete upscaled image
        upscaled_boxartpath.unlink(missing_ok=True)
    else:
        # cover = create_front_banner(bannertype)
        cover = Image.new("RGBA", cover_size, color=cover_color)
    # add banner
    if bannerpath is not None:
        banner = Image.open(bannerpath)
    else:
        banner = create_front_banner(bannertype)
    banner = banner.resize(banner_size)
    cover.paste(banner, banner_position)
    return cover


def create_fullcover_image(
    gamecategory: str,
    title: str,
    description: str,
    backgroundpath: PathLike | str | bytes = None,
    bannerpath: PathLike | str | bytes = None,
    boxartdenoise: int = 0,
    boxartpath: PathLike | str | bytes = None,
    boxartscale: int = 1,
    screenshotpath: PathLike | str | bytes = None,
) -> Image:
    # create full cover
    cover = Image.new("RGBA", (900, 600))
    # create parts of image
    front_cover = create_front_cover_image(
        boxartpath=boxartpath,
        boxartdenoise=boxartdenoise,
        boxartscale=boxartscale,
        bannertype=gamecategory,
    )
    spine = create_spine_image(title, bannertype=gamecategory)
    rear_cover = create_rear_cover_image(
        title,
        description,
        backgroundpath=backgroundpath,
        bannerpath=bannerpath,
        screenshotpath=screenshotpath,
    )
    # piece together cover
    cover.paste(front_cover, (475, 0))
    cover.paste(spine, (425, 0))
    cover.paste(rear_cover, (0, 0))
    cover = cover.convert("RGB")
    return cover


def create_rear_cover_image(
    title: str,
    description: str,
    backgroundpath: PathLike | str | bytes = None,
    bannerpath: PathLike | str | bytes = None,
    screenshotpath: PathLike | str | bytes = None,
) -> Image:
    banner_size = (425, 96)
    cover_color = (7, 69, 94, 255)
    cover_size = (425, 600)
    card_color = (25, 34, 48, 255)
    card_margin = (25, 25)
    card_radius = 12
    if bannerpath is None:
        card_position = card_margin
        card_size = (
            cover_size[0] - 2 * card_margin[0],
            cover_size[1] - 2 * card_margin[1],
        )
    else:
        card_position = (
            card_margin[0],
            card_margin[1] + banner_size[1],
        )
        card_size = (
            cover_size[0] - 2 * card_margin[0],
            cover_size[1] - 2 * card_margin[1] - banner_size[1],
        )
    title_color = (255, 255, 255, 255)
    title_font_size = 16
    title_font = ImageFont.truetype(
        font="fonts/NotoSans-Bold.ttf", size=title_font_size
    )
    title_margin = (18, 10)
    title_position = (
        card_position[0] + title_margin[0],
        card_position[1] + title_margin[1],
    )
    screenshot_size = (376, 210)
    screenshot_position = (
        card_position[0],
        card_position[1] + title_margin[1] + 2 * title_font_size,
    )
    descr_margin = (title_margin[0], 8)
    descr_font_size = 14
    descr_font = ImageFont.truetype(
        font="fonts/NotoSans-Regular.ttf", size=descr_font_size
    )
    if screenshotpath is None:
        descr_position = (
            card_position[0] + descr_margin[0],
            title_position[1] + title_font_size + descr_margin[1],
        )
        descr_size = (
            card_size[0] - 2 * descr_margin[0],
            card_size[1] - descr_margin[1] - descr_position[1],
        )
    else:
        descr_position = (
            card_position[0] + descr_margin[0],
            screenshot_position[1] + screenshot_size[1] + descr_margin[1],
        )
        descr_size = (
            card_size[0] - 2 * descr_margin[0],
            card_size[1]
            - descr_margin[1]
            - (screenshot_position[1] + screenshot_size[1]),
        )
    # create cover
    cover = Image.new("RGBA", cover_size, color=cover_color)
    cover_draw = ImageDraw.Draw(cover)
    if backgroundpath is not None:
        background = Image.open(backgroundpath)
        background.resize(get_scaled_dimensions_by_height(cover_size[1], cover.size))
        background = background.crop(box=(0, 0, cover_size[0], cover_size[1]))
        cover.paste(background)
    # add banner
    if bannerpath is not None:
        banner = Image.open(bannerpath)
        banner = banner.resize(banner_size)
        cover.paste(banner)
    # add description card
    cover_draw.rounded_rectangle(
        (
            card_position[0],
            card_position[1],
            card_position[0] + card_size[0],
            card_position[1] + card_size[1],
        ),
        fill=card_color,
        radius=card_radius,
    )
    # add title
    cover_draw.text(
        title_position,
        title,
        font=title_font,
        fill=title_color,
    )
    # add screenshot
    if screenshotpath is not None:
        screenshot = Image.open(screenshotpath)
        screenshot = screenshot.resize(screenshot_size)
        cover.paste(screenshot, screenshot_position)
    # add description
    descr_str = textwrapped(description, descr_font, descr_size[0])
    cover_draw.text(
        descr_position,
        descr_str,
        font=descr_font,
        fill=(255, 255, 255),
    )
    return cover


def create_spine_image(
    title: str,
    bannerpath: PathLike | str | bytes = None,
    bannertype: str = None,
) -> Image:
    banner_position = (0, 0)
    banner_size = (152, 50)
    spine_color = (7, 69, 94, 255)
    spine_size = (600, 50)
    title_color = (255, 255, 255, 255)
    title_font_size = 26
    title_font = ImageFont.truetype(
        font="fonts/NotoSans-Regular.ttf", size=title_font_size
    )
    title_margin = (0, 18)
    title_position = (banner_size[0] + title_margin[1], spine_size[1] // 2)
    title_size = (spine_size[0] - banner_size[0] - (2 * title_margin[1]), spine_size[1])
    # create spine
    spine = Image.new("RGBA", spine_size, color=spine_color)
    spine_draw = ImageDraw.Draw(spine)
    # add banner
    if bannerpath is not None:
        banner = Image.open(bannerpath)
    else:
        banner = create_spine_banner(bannertype)
    banner = banner.resize(banner_size)
    spine.paste(banner, banner_position)
    # add title
    title, _, _ = textwrapped(title, title_font, title_size[0]).partition("\n")
    spine_draw.text(
        title_position,
        title,
        anchor="lm",
        fill=title_color,
        font=title_font,
    )
    # rotate spine
    spine = spine.transpose(Image.Transpose.ROTATE_270)
    return spine


def create_front_banner(gametype: str) -> Image:
    dimensions = (425, 75)
    title_position = (16, dimensions[1] // 2)
    font_color = (255, 255, 255, 255)
    font_size = 38
    if gametype == "arcade":
        title = "ARCADE"
        color = (0xFF, 0x8F, 0x00, 0xFF)  # amber 50 800
    elif gametype == "indie":
        title = "INDIE GAMES"
        color = (0x00, 0x91, 0xEA, 0xFF)  # light blue 50 A700
    elif gametype == "kinect":
        title = "KINECT"
        color = (0x28, 0x35, 0x93, 0xFF)  # indigo 800
    elif gametype == "xbox":
        title = "XBOX"
        color = (0, 0, 0, 255)  # black
    elif gametype == "xbox360":
        title = "XBOX 360"
        color = (0x2E, 0x7D, 0x32, 0xFF)  # green 50 800
    elif gametype == "homebrew":
        title = "HOMEBREW"
        color = (0xAD, 0x14, 0x57, 0xFF)  # pink 800
    else:
        title = "GAME"
        color = (0x42, 0x42, 0x42, 0xFF)  # gray 50 800
    font = ImageFont.truetype(font="fonts/NotoSans-Bold.ttf", size=font_size)
    banner = Image.new("RGBA", dimensions, color=color)
    banner_draw = ImageDraw.Draw(banner)
    banner_draw.text(
        title_position,
        title,
        font=font,
        anchor="lm",
        fill=font_color,
    )
    return banner


def create_spine_banner(gametype: str) -> Image:
    dimensions = (152, 50)
    title_position = (18, dimensions[1] // 2)
    font_color = (255, 255, 255, 255)
    font_size = 26
    if gametype == "arcade":
        title = "ARCADE"
        color = (0xFF, 0x8F, 0x00, 0xFF)  # amber 50 800
    elif gametype == "indie":
        title = "INDIE"
        color = (0x00, 0x91, 0xEA, 0xFF)  # light blue 50 A700
    elif gametype == "kinect":
        title = "KINECT"
        color = (0x28, 0x35, 0x93, 0xFF)  # indigo 800
    elif gametype == "xbox":
        title = "XBOX"
        color = (0, 0, 0, 255)  # black
    elif gametype == "xbox360":
        title = "XBOX 360"
        color = (0x2E, 0x7D, 0x32, 0xFF)  # green 50 800
        font_size = 24
    elif gametype == "homebrew":
        title = "HOMEBREW"
        color = (0xAD, 0x14, 0x57, 0xFF)  # pink 800
        font_size = 18
    else:
        title = "GAME"
        color = (0x42, 0x42, 0x42, 0xFF)  # gray 50 800
    font = ImageFont.truetype(font="fonts/NotoSans-Bold.ttf", size=font_size)
    banner = Image.new("RGBA", dimensions, color=color)
    banner_draw = ImageDraw.Draw(banner)
    banner_draw.text(
        title_position,
        title,
        font=font,
        anchor="lm",
        fill=font_color,
    )
    return banner
