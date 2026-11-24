from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from zoneinfo import ZoneInfo
import calendar

now = datetime.now(ZoneInfo("Europe/Paris"))
total = 366 if calendar.isleap(now.year) else 365
day = now.timetuple().tm_yday
left = total - day

W, H = 1080, 2400
COLS, STEP, R = 17, 46.6, 16
X0, Y0 = 167, 765
YELLOW, ORANGE, GREY = (251, 191, 36), (245, 158, 11), (38, 38, 38)
LABEL = (100, 75, 15)

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except OSError:
        return ImageFont.load_default()

f_small = font("DejaVuSans.ttf", 16)
f_big = font("DejaVuSans-Bold.ttf", 30)

img = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(img)
rows = -(-total // COLS)

# points
for i in range(total):
    n = i + 1
    x = X0 + STEP * (i % COLS)
    y = Y0 + STEP * (i // COLS)
    col = YELLOW if n < day else ORANGE if n == day else GREY
    d.ellipse([x - R, y - R, x + R, y + R], fill=col)

# repères
d.text((151, 724), "DAY →", font=f_small, fill=LABEL, anchor="lm")
for c in (7, 14):
    d.text((X0 + STEP * (c - 1), 725), str(c), font=f_small, fill=LABEL, anchor="mm")
for r in [5, 9, 13, 17, 21, rows]:
    d.text((136, Y0 + STEP * (r - 1)), str(2 * r - 1),
           font=f_small, fill=LABEL, anchor="mm")

# "WEEK" vertical + flèche
t = Image.new("RGBA", (80, 24), (0, 0, 0, 0))
ImageDraw.Draw(t).text((40, 12), "WEEK", font=f_small, fill=LABEL, anchor="mm")
t = t.rotate(90, expand=True)
img.paste(t, (123, 732), t)
d.text((135, 808), "↓", font=f_small, fill=LABEL, anchor="mm")

# texte du bas
d.text((W / 2, 2085), f"{left} JOURS RESTANTS", font=f_big, fill=YELLOW, anchor="mm")

img.save("wallpaper.png")
