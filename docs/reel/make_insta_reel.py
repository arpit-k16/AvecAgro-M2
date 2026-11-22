"""Vertical (9:16) Instagram-style reel for AvecAgro Milestone 2.
Frames are drawn with PIL and piped to ffmpeg. All screens of the app come from real runs:
frames_live/ = public Render site (gpt-oss-120b), frames/ = prompt lab (Claude). Music: audio/make_music.py (UPBEAT=1)."""
import subprocess, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
GF = '/usr/share/fonts/truetype/google-fonts/ofl/'
ANTON = GF + 'anton/Anton-Regular.ttf'
FBLK = GF + 'firasans/FiraSans-Black.ttf'
FBOLD = GF + 'firasans/FiraSans-Bold.ttf'
FSEMI = GF + 'firasans/FiraSans-SemiBold.ttf'
FREG = GF + 'firasans/FiraSans-Regular.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
INK = (22, 36, 27); LEAF = (30, 122, 71); LEAF_L = (95, 203, 138); TURM = (217, 154, 23)
RUST = (178, 58, 38); PAPER = (238, 243, 236); WHITE = (255, 255, 255); MIST = (190, 211, 197)
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
def ease_out(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def ease_back(x):
    x = max(0, min(1, x)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def caption(img, text, t, y=1590, size=58, color=WHITE, box=INK, hl=None):
    """Word-by-word reveal caption in a rounded box; words in hl get the turmeric colour."""
    d = ImageDraw.Draw(img); fnt = font(FBLK, size)
    lines = wrap(d, text, fnt, 900)
    lh = int(size * 1.22); bh = lh * len(lines) + 56
    top = y - bh // 2
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    a = int(235 * ease_out(t / 0.25))
    od.rounded_rectangle([60, top, W - 60, top + bh], radius=34, fill=box + (a,))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    nwords = sum(len(l.split()) for l in lines); shown = int(nwords * ease_out(t / 0.7)) + (1 if t > 0 else 0)
    k = 0
    for i, line in enumerate(lines):
        x = (W - d.textlength(line, font=fnt)) / 2; yy = top + 28 + i * lh
        for w in line.split():
            if k < shown:
                c = TURM if hl and w.strip('.,:!?').lower() in hl else color
                d.text((x, yy), w, font=fnt, fill=c)
            x += d.textlength(w + ' ', font=fnt); k += 1

def chip(img, text, color=TURM):
    d = ImageDraw.Draw(img); fnt = font(FBOLD, 40)
    w = d.textlength(text, font=fnt)
    d.rounded_rectangle([60, 120, 60 + w + 56, 120 + 72], radius=36, fill=color)
    d.text((88, 132), text, font=fnt, fill=INK)

def bg(color=INK):
    img = Image.new('RGBA', (W, H), color + (255,))
    return img

_shot = {}
def shot(img, path, t, dur, zoom=(1.0, 1.08), pan=(0.0, 0.0), top=250, width=960):
    """App screenshot as a rounded 'phone card' with slide-up entrance and a slow Ken Burns zoom/pan."""
    if path not in _shot:
        s = Image.open(path).convert('RGB'); r = width / s.width
        _shot[path] = s.resize((width, int(s.height * r)), Image.LANCZOS)
    s = _shot[path]
    p = t / dur; z = zoom[0] + (zoom[1] - zoom[0]) * p
    cw, ch = int(width / z), int(min(s.height, 1280) / z)
    ox = int((s.width - cw) * (0.5 + pan[0] * p)); oy = int((s.height - ch) * (0.0 + max(0, pan[1]) * p))
    ox = max(0, min(s.width - cw, ox)); oy = max(0, min(s.height - ch, oy))
    crop = s.crop((ox, oy, ox + cw, oy + ch)).resize((width, int(ch * z)), Image.BILINEAR)
    slide = int(140 * (1 - ease_out(t / 0.45)))
    mask = Image.new('L', crop.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, crop.width, crop.height], radius=36, fill=255)
    shadow = Image.new('RGBA', (crop.width + 80, crop.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([40, 50, crop.width + 40, crop.height + 40], radius=40, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    x = (W - width) // 2; y = top + slide
    img.alpha_composite(shadow, (x - 40, y - 40))
    img.paste(crop, (x, y), mask)

def big(img, lines, t, y0=560, size=150, colors=None, gap=1.05, font_path=ANTON):
    d = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        lt = t - i * 0.18
        if lt <= 0: continue
        sc = 0.6 + 0.4 * ease_back(lt / 0.35)
        f = font(font_path, max(10, int(size * sc)))
        c = (colors[i] if colors else WHITE)
        w = d.textlength(line, font=f)
        yy = y0 + i * int(size * gap) + int(size * (1 - sc) / 2)
        d.text(((W - w) / 2, yy), line, font=f, fill=c)

def progress(img, gt, total):
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 10], fill=(40, 60, 46)); d.rectangle([0, 0, int(W * gt / total), 10], fill=TURM)

def brand(img):
    d = ImageDraw.Draw(img); f = font(FBOLD, 36)
    d.text((W - 60 - d.textlength('AvecAgro', font=f), 1850), 'AvecAgro', font=f, fill=MIST)

def codecard(img, t, title, body, accent, y=330, h=860, mark=None):
    d = ImageDraw.Draw(img)
    slide = int(120 * (1 - ease_out(t / 0.4)))
    x0, y0 = 60, y + slide
    d.rounded_rectangle([x0, y0, W - 60, y0 + h], radius=36, fill=(250, 251, 248), outline=accent, width=6)
    d.text((x0 + 40, y0 + 34), title, font=font(FBOLD, 40), fill=accent)
    fm = font(MONO, 30); yy = y0 + 110
    for para in body.split('\n'):
        for line in (wrap(d, para, fm, W - 220) or ['']):
            col = RUST if mark and any(m in line for m in mark) else INK
            if mark and any(m in line for m in mark):
                d.rectangle([x0 + 34, yy - 4, W - 94, yy + 38], fill=(247, 223, 218))
            d.text((x0 + 44, yy), line, font=fm, fill=col); yy += 42
            if yy > y0 + h - 60: return

def stat_rows(img, t, rows, y=520):
    d = ImageDraw.Draw(img)
    for i, (label, a, b, good) in enumerate(rows):
        lt = t - i * 0.5
        if lt <= 0: continue
        yy = y + i * 300; sl = int(80 * (1 - ease_out(lt / 0.4)))
        d.text((90 + sl, yy), label, font=font(FBOLD, 48), fill=MIST)
        fa = font(ANTON, 130)
        d.text((90 + sl, yy + 70), a, font=fa, fill=(200, 120, 110))
        aw = d.textlength(a, font=fa)
        if lt > 0.35:
            d.text((90 + sl + aw + 40, yy + 90), '→', font=font(FBOLD, 100), fill=MIST)
            d.text((90 + sl + aw + 170, yy + 70), b, font=fa, fill=LEAF_L if good else TURM)

def checklist(img, t, title, items, color, y=420):
    d = ImageDraw.Draw(img)
    d.text((80, y - 150), title, font=font(ANTON, 110), fill=color)
    for i, it in enumerate(items):
        lt = t - 0.4 - i * 0.45
        if lt <= 0: continue
        yy = y + i * 190; sl = int(60 * (1 - ease_out(lt / 0.35)))
        d.ellipse([80 + sl, yy + 8, 140 + sl, yy + 68], fill=color)
        cx, cy = 110 + sl, yy + 38
        if color == LEAF_L: d.line([(cx - 14, cy), (cx - 3, cy + 12), (cx + 16, cy - 12)], fill=INK, width=8)
        else: d.line([(cx - 14, cy), (cx + 12, cy)], fill=INK, width=8); d.line([(cx + 2, cy - 12), (cx + 14, cy), (cx + 2, cy + 12)], fill=INK, width=8)
        for j, line in enumerate(wrap(d, it, font(FSEMI, 54), 820)):
            d.text((170 + sl, yy + j * 64), line, font=font(FSEMI, 54), fill=WHITE)

LV = lambda n: P('frames_live', n)
V1 = ('Prompt: "You are AVECAGRO… recommend suitable crops… Never invent sensor readings…"\n\nInput: Bhopal, MP. Wheat planned. Sensor: pH 15, 90 °C.\n\nOutput (real, excerpt):\n'
      '…the commonly cited recommendation for irrigated timely-sown wheat is about 120:60:40 kg N:P2O5:K2O per hectare…\n'
      '…varieties (e.g., MP 1202, HI 1544, HI 8498)…\n\nFree text · no sources · not machine-readable')
V3 = ('Prompt v3: role + retrieved passages + JSON schema + 1 example + rules\n"Never cite an id not in the passages. NEVER write a soil value not in the profile."\n\nOutput (real, excerpt):\n'
      '{"crop":"Wheat","kb_refs":["KB-05","KB-03"]}\n{"crop":"Chickpea","kb_refs":["KB-04","KB-03"]}\n{"crop":"Lentil","kb_refs":["KB-27","KB-03"]}\n'
      '"soil_assessment":{"status":"unknown", "summary":"pH and temperature readings were impossible and were discarded… get a Soil Health Card test"}')

S = [  # (duration, drawer)
 (3.5, lambda im, t: (big(im, ['FARMING', 'ADVICE THAT', "DOESN'T GUESS."], t, 560, 170, [WHITE, WHITE, TURM]))),
 (6.5, lambda im, t: (big(im, ['86%'], t, 360, 330, [TURM]), caption(im, 'of Indian farm holdings are small or marginal', max(0, t - 0.4), 900, 64, box=(30, 52, 38)),
                      caption(im, 'Weather. Pests. Unknown soil. No expert nearby.', max(0, t - 2.0), 1250, 60, hl={'weather', 'pests', 'soil'}))),
 (3.0, lambda im, t: (big(im, ['AVECAGRO'], t, 650, 200, [LEAF_L]), caption(im, 'An AI advisor for crops, season plans and pest alerts', max(0, t - 0.3), 1100, 56, box=(30, 52, 38)))),
 (3.0, lambda im, t: (chip(im, 'Prompt experiment'), big(im, ['SAME FARMER.', 'SAME MODEL.', 'TWO PROMPTS.'], t, 600, 150, [WHITE, WHITE, TURM]))),
 (11.0, lambda im, t: (chip(im, 'Before · v1 (Milestone 1)', (247, 160, 140)), codecard(im, t, 'v1 · one free-text prompt', V1, RUST, mark=['120:60:40', 'MP 1202']),
                       caption(im, 'It invented a fertiliser dose and seed varieties', max(0, t - 1.2), 1420, 56, hl={'invented'}))),
 (11.0, lambda im, t: (chip(im, 'After · v3 (final)', LEAF_L), codecard(im, t, 'v3 · grounded, cited, structured', V3, LEAF),
                       caption(im, 'Only facts from our knowledge base, with sources', max(0, t - 1.2), 1420, 56, hl={'sources'}))),
 (8.0, lambda im, t: (chip(im, 'Measured on 7 runs'), stat_rows(im, t, [('Valid JSON', '0/7', '7/7', True), ('Valid sources', '0/7', '7/7', True), ('Answer length vs v2', '4.7k', '2.7k', True)]))),
 (4.0, lambda im, t: (chip(im, 'Real prompt-lab run'), shot(im, P('frames', 'lab_summary.jpg'), t, 4.0, (1.0, 1.1)),
                      caption(im, 'Every number comes from a real run', max(0, t - 0.5), 1620, 54))),
 (2.5, lambda im, t: (chip(im, 'Live demo'), big(im, ['NO LOGIN.', 'REAL RUN.'], t, 620, 170, [WHITE, TURM]),
                      caption(im, 'avecagro.onrender.com', max(0, t - 0.6), 1150, 60, color=LEAF_L, box=(30, 52, 38)))),
 (5.0, lambda im, t: (chip(im, 'Live demo'), shot(im, LV('r02_input.jpg'), t, 5.0, (1.0, 1.12), (0.0, 0.3)), caption(im, 'A farmer types in Hinglish', max(0, t - 0.4), 1640, 60, hl={'hinglish'}))),
 (3.5, lambda im, t: (chip(im, 'Live demo'), shot(im, LV('r03_furrow2.jpg'), t, 3.5, (1.05, 1.15), (0.0, 1.0)), caption(im, 'Each AI step sprouts a seed', max(0, t - 0.3), 1640, 60))),
 (3.5, lambda im, t: (chip(im, 'Live demo'), shot(im, LV('r04_furrow4.jpg'), t, 3.5, (1.15, 1.25), (0.0, 1.0)), caption(im, 'Check · facts · crops · plan · pests', max(0, t - 0.3), 1640, 56))),
 (6.0, lambda im, t: (chip(im, 'Live demo'), shot(im, LV('r05_profile.jpg'), t, 6.0, (1.0, 1.1), (0.0, 0.4)), caption(im, 'It reads the farm and asks back in Hindi', max(0, t - 0.4), 1640, 56, hl={'hindi'}))),
 (7.0, lambda im, t: (chip(im, 'Live demo'), shot(im, LV('r06_crops.jpg'), t, 7.0, (1.0, 1.1), (0.0, 0.5)), caption(im, 'Crops picked from trusted sources, with citations', max(0, t - 0.4), 1640, 54, hl={'citations'}))),
 (6.0, lambda im, t: (chip(im, 'Live demo'), shot(im, LV('r07_plan.jpg'), t, 6.0, (1.0, 1.1), (0.0, 0.6)), caption(im, 'A week-by-week plan that waits for rain', max(0, t - 0.4), 1640, 56, hl={'rain'}))),
 (5.0, lambda im, t: (chip(im, 'Live demo'), shot(im, LV('r08_pests.jpg'), t, 5.0, (1.0, 1.08), (0.0, 0.4)), caption(im, 'Pest watch with safe IPM steps', max(0, t - 0.4), 1640, 58))),
 (7.0, lambda im, t: (chip(im, 'Live demo · edge case', (247, 160, 140)), shot(im, LV('r09_dose.jpg'), t, 7.0, (1.0, 1.1), (0.0, 0.3)),
                      caption(im, 'Asked for a pesticide dose. It refused, and still helped.', max(0, t - 0.4), 1640, 54, hl={'refused'}))),
 (6.0, lambda im, t: (chip(im, 'Testing'), shot(im, P('frames', 'tests.jpg'), t, 6.0, (1.0, 1.1), (0.0, 0.5)), caption(im, '14 tests: 13 pass, 1 honest fail', max(0, t - 0.4), 1640, 60, hl={'13', 'pass'}))),
 (9.0, lambda im, t: (chip(im, 'Milestone 2 · done'), checklist(im, t, 'DONE', ['4 prompts + retrieval with sources', 'Live web app, no login needed', '14 tests and a v1 → v3 prompt lab', 'Answers in Hindi, Hinglish, English'], LEAF_L))),
 (9.0, lambda im, t: (chip(im, 'Next · Milestone 3'), checklist(im, t, 'NEXT', ['Expert-checked knowledge base for more states', 'Live soil-sensor and weather feeds', 'Hindi voice input for farmers', 'Field trials with real farmers'], TURM))),
 (7.5, lambda im, t: (big(im, ['AVECAGRO'], t, 640, 210, [LEAF_L]), caption(im, 'Try it: avecagro.onrender.com', max(0, t - 0.4), 1040, 60, color=WHITE, box=LEAF, hl={'avecagro.onrender.com'}),
                      caption(im, 'Team PE-B49-23 · SCSE4041 Milestone 2', max(0, t - 0.9), 1300, 44, color=MIST, box=(30, 52, 38)))),
]
TOTAL = sum(d for d, _ in S)

def main():
    music = P('audio', 'music_upbeat.wav')
    subprocess.run(['python3', P('audio', 'make_music.py'), str(TOTAL), music], check=True, env=dict(os.environ, UPBEAT='1'))
    out = P('AvecAgro_M2_Reel.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', music, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p',
                           '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    gt = 0.0
    for i, (dur, draw) in enumerate(S):
        n = int(round(dur * FPS))
        for f in range(n):
            t = f / FPS
            im = bg(); draw(im, t); progress(im, gt + t, TOTAL); brand(im)
            if t < 0.12 and i > 0:  # quick flash cut on the beat
                fl = Image.new('RGBA', (W, H), (255, 255, 255, int(110 * (1 - t / 0.12)))); im.alpha_composite(fl)
            ff.stdin.write(im.convert('RGB').tobytes())
        gt += dur
    ff.stdin.close(); ff.wait()
    print('reel', out, TOTAL, 's')

if __name__ == '__main__':
    main()
