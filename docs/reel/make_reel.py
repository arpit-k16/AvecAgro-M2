from PIL import Image, ImageDraw, ImageFont
import subprocess, os
os.makedirs('out',exist_ok=True)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
def fit(d,t,size=30):
    while size>16:
        f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',size)
        if d.textlength(t,font=f)<=1230: return f
        size-=1
    return f
def frame(src, caption, label, out):
    if src.startswith('cards/'):
        im=Image.open(src).convert('RGB').resize((1280,720))
        if caption:
            d=ImageDraw.Draw(im); d.rectangle([0,650,1280,720],fill=(20,30,20)); d.text((640,685),caption,font=fit(d,caption),fill='white',anchor='mm')
    else:
        im=Image.new('RGB',(1280,720),(31,42,28))
        s=Image.open(src).convert('RGB'); s=s.resize((int(s.width*600/s.height),600), Image.LANCZOS)
        im.paste(s,((1280-s.width)//2,8))
        d=ImageDraw.Draw(im)
        d.rectangle([0,612,1280,720],fill=(20,30,20))
        d.text((640,655),caption,font=fit(d,caption),fill='white',anchor='mm')
        d.text((640,698),label,font=Fs,fill=(190,210,180),anchor='mm')
    im.save(out)
L='Real run · AvecAgro web app (Claude) · 22 Nov 2026'
seq=[
('cards/01_problem.png','',10,''),
('cards/02_experiment.png','',5,''),
('cards/03_before.png','v1: free text, invents a fertiliser dose — no sources',13,''),
('frames/lab_rows_v1.jpg','Prompt lab: v1 row for test 14 → "Invented soil numbers: YES"',6,L),
('cards/05_after.png','v3: grounded, cited, valid JSON — impossible readings discarded',13,''),
('frames/lab_summary.jpg','v1 → v3 on 7 runs: JSON 0/7 → 7/7 · citations 0/7 → 7/7 · 43% shorter than v2',8,L),
('frames/h01.jpg','Demo: farmer types in Hinglish (Gorakhpur, UP, after paddy, low budget)',5,L),
('frames/h02.jpg','P1 builds the farm profile: rabi, canal water, low budget, flags "2 bigha"',6,L),
('frames/h03.jpg','P2 + RAG: wheat & chana, answered in Hinglish, sources KB-05 / KB-15 / KB-04',7,L),
('frames/h04.jpg','Soil unknown → no invented values, asks for a Soil Health Card test',5,L),
('frames/h05.jpg','P3: week-by-week calendar with irrigation and nutrient notes',6,L),
('frames/h07.jpg','P4: pest watch-list, IPM steps, Kisan Call Centre 1800-180-1551',6,L),
('frames/d01_running.jpg','Edge case: asks for an exact chlorpyrifos dose + a yield guarantee',4,L),
('frames/d02_running.jpg','Router skips P2/P3: crop already standing with a problem → P4 only',4,L),
('frames/p01.jpg','P4: likely brown planthopper — declines the dose and the guarantee',8,L),
('frames/tests.jpg','14 tests (normal, edge, invalid): 13 pass, 1 fail (retrieval miss) — reported honestly',6,L),
('cards/04_progress.png','',15,''),
]
lst=[]
for i,(src,cap,dur,lab) in enumerate(seq):
    out=f'out/f{i:02d}.png'; frame(src,cap,lab,out); lst.append((out,dur))
with open('out/list.txt','w') as f:
    for o,d in lst: f.write(f"file '{os.path.basename(o)}'\nduration {d}\n")
    f.write(f"file '{os.path.basename(lst[-1][0])}'\n")
total=sum(d for _,d in lst); print('total seconds',total)
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','out/list.txt','-f','lavfi','-i','anullsrc=r=44100:cl=stereo',
 '-vf','fps=25,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-shortest','-t',str(total),'AvecAgro_M2_Reel.mp4'],check=True)
