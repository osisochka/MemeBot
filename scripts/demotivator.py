from PIL import Image, ImageDraw, ImageFont
import io
import textwrap


def create_demotivator_in_memory(image, bottom_text: str) -> bytes:

    border_size = 20
    padding = 40
    bg_color = (0, 0, 0)

    img_width, img_height = image.size
    total_width = img_width + 2 * border_size
    total_height = img_height + 2 * border_size + 150

    demotivator = Image.new("RGB", (total_width, total_height), bg_color)

    demotivator.paste(image, (border_size, border_size))

    draw = ImageDraw.Draw(demotivator)
    draw.rectangle(
        [
            (border_size - 2, border_size - 2),
            (border_size + img_width + 2, border_size + img_height + 2),
        ],
        outline="white",
        width=2,
    )

    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    avg_char_width = font.getlength("a")
    max_text_width = img_width - 2 * padding
    max_chars_per_line = int(max_text_width / avg_char_width)
    wrapped_text = textwrap.fill(bottom_text, width=max_chars_per_line)

    text_x = total_width // 2
    text_y = border_size + img_height + padding

    draw.multiline_text(
        (text_x, text_y),
        wrapped_text,
        font=font,
        fill="white",
        align="center",
        anchor="ma",
    )

    output_buffer = io.BytesIO()
    demotivator.save(output_buffer, format="JPEG", quality=95)

    return output_buffer.getvalue()
