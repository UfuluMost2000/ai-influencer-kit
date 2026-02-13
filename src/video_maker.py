import os
import random
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip

DEFAULT_W, DEFAULT_H = 1080, 1920
DEFAULT_DURATION = 90

# MoviePy 1.0.x may still reference Image.ANTIALIAS. Pillow>=10 removed it.
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


def _pick_file(folder, exts=(".jpg", ".jpeg", ".png", ".mp3", ".wav", ".m4a")):
    if not folder or not os.path.isdir(folder):
        return None
    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(exts)
    ]
    return random.choice(files) if files else None


def _load_background(bg_path, w, h):
    if bg_path and os.path.exists(bg_path):
        img = Image.open(bg_path).convert("RGB")

        img_ratio = img.width / img.height
        target_ratio = w / h

        if img_ratio > target_ratio:
            new_w = int(img.height * target_ratio)
            x0 = (img.width - new_w) // 2
            img = img.crop((x0, 0, x0 + new_w, img.height))
        else:
            new_h = int(img.width / target_ratio)
            y0 = (img.height - new_h) // 2
            img = img.crop((0, y0, img.width, y0 + new_h))

        # Pillow compatibility: ANTIALIAS removed in newer versions
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS

        img = img.resize((w, h), resample)

        return img

    base = Image.new("RGB", (w, h), (10, 10, 10))
    draw = ImageDraw.Draw(base)
    for y in range(h):
        c = int(10 + (y / h) * 40)
        draw.line([(0, y), (w, y)], fill=(c, c, c))
    return base


def _wrap_quote(text, width=30):
    lines = []
    for paragraph in (text or "").split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=width) or [""])
    return "\n".join(lines).strip()


def _draw_text_centered(img, quote, author, font_path=None):
    w, h = img.size

    def load_font(size):
        if font_path and os.path.exists(font_path):
            return ImageFont.truetype(font_path, size=size)
        return ImageFont.load_default()

    quote_font = load_font(64)
    author_font = load_font(44)

    quote_wrapped = _wrap_quote(quote, width=28)
    author_text = f"— {author}" if author else ""

    panel_h = int(h * 0.55)
    panel_y0 = int(h * 0.22)

    overlay = Image.new("RGBA", (w, panel_h), (0, 0, 0, 140))
    img_rgba = img.convert("RGBA")
    img_rgba.paste(overlay, (0, panel_y0), overlay)
    img = img_rgba.convert("RGB")

    draw = ImageDraw.Draw(img)

    quote_bbox = draw.multiline_textbbox((0, 0), quote_wrapped, font=quote_font, align="center", spacing=14)
    quote_tw = quote_bbox[2] - quote_bbox[0]
    quote_th = quote_bbox[3] - quote_bbox[1]

    author_tw = author_th = 0
    if author_text:
        author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
        author_tw = author_bbox[2] - author_bbox[0]
        author_th = author_bbox[3] - author_bbox[1]

    total_h = quote_th + (30 if author_text else 0) + (author_th if author_text else 0)
    start_y = panel_y0 + (panel_h - total_h) // 2

    x_quote = (w - quote_tw) // 2
    y_quote = start_y

    for dx, dy in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
        draw.multiline_text((x_quote + dx, y_quote + dy), quote_wrapped, font=quote_font, fill=(0, 0, 0),
                            align="center", spacing=14)

    draw.multiline_text((x_quote, y_quote), quote_wrapped, font=quote_font, fill=(255, 255, 255),
                        align="center", spacing=14)

    if author_text:
        x_author = (w - author_tw) // 2
        y_author = y_quote + quote_th + 30
        draw.text((x_author, y_author), author_text, font=author_font, fill=(230, 230, 230))

    return img


def make_quote_video(
    out_path: str,
    quote: str,
    author: str = "",
    duration: int = DEFAULT_DURATION,
    w: int = DEFAULT_W,
    h: int = DEFAULT_H,
    backgrounds_dir: str = "assets/backgrounds",
    background_path: str | None = None,
    music_dir: str = "assets/music",
    font_path: str | None = None,
    music_volume: float = 0.08,
):
    bg_path = background_path if background_path else _pick_file(backgrounds_dir, exts=(".jpg", ".jpeg", ".png"))

    img = _load_background(bg_path, w, h)
    img = _draw_text_centered(img, quote, author, font_path=font_path)

    frame = np.array(img)
    clip = ImageClip(frame).set_duration(duration)

    def zoom(t):
        return 1.0 + 0.06 * (t / duration)

    clip = clip.resize(lambda t: zoom(t)).crop(x_center=w / 2, y_center=h / 2, width=w, height=h)

    music_path = _pick_file(music_dir, exts=(".mp3", ".wav", ".m4a"))
    if music_path and os.path.exists(music_path):
        audio = AudioFileClip(music_path).volumex(music_volume)

        if audio.duration < duration:
            loops = int(duration // audio.duration) + 1
            audio = CompositeAudioClip([audio] * loops)

        audio = audio.subclip(0, duration)
        clip = clip.set_audio(audio)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    clip.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac")
    return out_path
