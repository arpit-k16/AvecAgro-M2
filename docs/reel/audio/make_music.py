"""Original background music for the AvecAgro reel (synthesised, no samples, no copyright).
Tanpura-style drone + soft chord pad + plucked arpeggio. 90 bpm, D major, length = reel length."""
import numpy as np, wave, sys
SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 127.0
OUT = sys.argv[2] if len(sys.argv) > 2 else 'music.wav'
N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(7)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def env_adsr(n, a, d, s, r):
    e = np.ones(n) * s; A, D, R = int(a*SR), int(d*SR), int(r*SR)
    e[:A] = np.linspace(0, 1, A); e[A:A+D] = np.linspace(1, s, D); e[-R:] *= np.linspace(1, 0, R); return e

# 1) tanpura drone: D2 / A2 / D3 with many harmonics and slow "jawari" shimmer, re-plucked every 2.67 s
drone = np.zeros(N); cycle = 60/90*4
for k, (m, off) in enumerate([(50, 0.0), (57, 0.67), (62, 1.33), (50, 2.0)]):
    f = hz(m - 12 if k in (0, 3) else m - 12)
    start = off
    while start < DUR:
        n = int(min(cycle * 1.6, DUR - start) * SR); s0 = int(start * SR)
        tt = np.arange(n) / SR; sig = np.zeros(n)
        for h in range(1, 14):
            shimmer = 1 + 0.35 * np.sin(2*np.pi*(0.3 + 0.07*h)*tt + h)
            sig += (0.9 ** h) * shimmer * np.sin(2*np.pi*f*h*tt + rng.random()*6.28)
        sig *= np.exp(-tt / 2.2) * np.minimum(1, tt / 0.02)
        drone[s0:s0+n] += sig[:N-s0]
        start += cycle
drone /= np.abs(drone).max()

# 2) chord pad: D - Bm - G - A, one chord per bar
chords = [[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]]
pad = np.zeros(N); bar = 60/90*4
for i in range(int(DUR // bar) + 1):
    s0 = int(i * bar * SR); n = min(int(bar * SR * 1.25), N - s0)
    if n <= 0: break
    tt = np.arange(n) / SR; sig = np.zeros(n)
    for m in chords[i % 4]:
        for det in (-0.12, 0.0, 0.13):
            ff = hz(m) * 2 ** (det / 12)
            sig += np.sin(2*np.pi*ff*tt) + 0.3*np.sin(2*np.pi*2*ff*tt)
    sig *= env_adsr(n, 0.9, 0.5, 0.8, 1.2)
    pad[s0:s0+n] += sig
pad /= np.abs(pad).max()

# 3) plucked arpeggio (Karplus-Strong), eighth notes, enters at 15 s, brighter in the demo section
def pluck(f, dur, bright):
    n = int(dur * SR); p = max(2, int(SR / f)); buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = bright * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out * np.minimum(1, np.arange(n) / 30)
arp = np.zeros(N); step = 60/90/2; pattern = [0, 1, 2, 1, 2, 3, 2, 1]
cache = {}
for i in range(int(DUR / step)):
    when = i * step
    if when < 15 or when > DUR - 4: continue
    ch = chords[int(when // bar) % 4]; notes = ch + [ch[0] + 12]
    m = notes[pattern[i % 8]] + 12
    bright = 0.996 if 55 <= when <= 106 else 0.99
    key = (m, bright)
    if key not in cache: cache[key] = pluck(hz(m), 1.4, bright)
    s0 = int(when * SR); seg = cache[key][:N - s0]
    vel = 0.75 + 0.25 * (i % 2 == 0)
    arp[s0:s0+len(seg)] += vel * seg
arp /= np.abs(arp).max()

# mix, gentle low-pass on pad, stereo widening with short delays, fades
mix = 0.42 * drone + 0.30 * pad + 0.38 * arp * np.clip((t - 15) / 4, 0, 1)
fade = np.minimum(1, t / 3) * np.minimum(1, (DUR - t) / 5)
mix *= fade
L = mix + 0.25 * np.roll(arp, int(0.011 * SR)) * fade * 0.4
R = mix + 0.25 * np.roll(arp, int(0.017 * SR)) * fade * 0.4
st = np.stack([L, R], 1); st /= np.abs(st).max(); st *= 0.6
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('wrote', OUT, DUR, 's')
