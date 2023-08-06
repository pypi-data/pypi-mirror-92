from PIL import Image, ImageFont, ImageDraw
import os


def generate_icon(char: str):
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/NotoSans-Bold.ttf", 50
    )
    draw.text((0, 0), char, font=font)
    image.save(f"icons/{char}.png", "PNG")


def main():
    try:
        os.mkdir("icons")
    except FileExistsError:
        pass

    for i in range(0, 8):
        generate_icon(str(i))
    generate_icon("A")
    generate_icon("F")
    generate_icon("D")


if __name__ == "__main__":
    main()
