#!/usr/bin/env python3
"""
Andar ADTE2104 v2.0 / HLK-LD6002 (chip ADT6101P) — 60 GHz radar vital-signs.
Live dashboard: tetno (BPM), oddech, dystans, obecnosc + przebiegi fazy.

Protokol (zweryfikowany na zywo + biblioteka icewind1991/hlk_ld6002)::

  UART 1382400 8N1 (CP2104 wymaga ustawienia przez pyserial, nie stty).
  Ramka TLV:  01 | ID(2 BE) | LEN(2 BE) | TYPE(2 BE) | HCK(1) | DATA[LEN] | DCK(1)
    HCK = ~XOR(bajty 0..6) & 0xFF ;  DCK = ~XOR(DATA) & 0xFF
  TYPE: 0x0A13 Phase (3x float32 LE: total/breath/heart)
        0x0A14 Respiratory  (float32 LE, oddechy/min)
        0x0A15 Heartbeat     (float32 LE, BPM)
        0x0A16 Distance      (u32 flag + float32 LE [cm]; flag==1 => obecnosc)
  Wartosci: float32 little-endian.
"""
import sys, time, struct, threading, collections
import serial

PORT = "/dev/ttyUSB1"   # domyslny; mozna nadpisac argumentem CLI
BAUD = 1382400

PHASE, RESP, HEART, DIST = 0x0A13, 0x0A14, 0x0A15, 0x0A16
TYPE_NAME = {PHASE: "Phase", RESP: "Respiratory", HEART: "Heartbeat", DIST: "Distance"}

PRESENCE_HOLD = 4.0   # s — jak dlugo trzymac "obecnosc" po ostatnich zywych parametrach


def cksum(b):
    x = 0
    for v in b:
        x ^= v
    return (~x) & 0xFF


class Reader(threading.Thread):
    """Watek czytajacy UART i parsujacy ramki TLV."""
    def __init__(self, port, baud):
        super().__init__(daemon=True)
        self.ser = serial.Serial(port, baud, timeout=0.2)
        self.lock = threading.Lock()
        self.hr = self.br = self.dist = None
        self.last_vital = -1e9   # czas ostatnich niezerowych vital-signs (monotonic)
        self.dist_valid = False  # flaga targetu z ramki dystansu
        self.heart_phase = collections.deque(maxlen=600)   # ~12 s @50Hz
        self.breath_phase = collections.deque(maxlen=600)
        self.hr_hist = collections.deque(maxlen=300)
        self.seen_types = collections.Counter()
        self.unknown = []
        self.running = True

    def run(self):
        buf = bytearray()
        ser = self.ser
        while self.running:
            buf += ser.read(4096) or b""
            i = 0
            while i < len(buf) - 8:
                if buf[i] != 0x01:
                    i += 1
                    continue
                dlen = (buf[i+3] << 8) | buf[i+4]
                typ = (buf[i+5] << 8) | buf[i+6]
                if dlen > 64 or cksum(buf[i:i+7]) != buf[i+7]:
                    i += 1
                    continue
                if i + 8 + dlen > len(buf):
                    break  # niekompletna ramka — doczytaj
                data = bytes(buf[i+8:i+8+dlen])
                if cksum(data) != buf[i+8+dlen]:
                    i += 1
                    continue
                self._handle(typ, data)
                i += 8 + dlen + 1
            del buf[:i]

    def _handle(self, typ, d):
        with self.lock:
            self.seen_types[typ] += 1
            if typ == HEART and len(d) == 4:
                self.hr = struct.unpack("<f", d)[0]
                if self.hr > 0:
                    self.hr_hist.append(self.hr)
                    self.last_vital = time.monotonic()
            elif typ == RESP and len(d) == 4:
                self.br = struct.unpack("<f", d)[0]
                if self.br > 0:
                    self.last_vital = time.monotonic()
            elif typ == DIST and len(d) >= 4:
                # 8 B = [flaga targetu (u32), dystans (f32 cm)]; 4 B = brak targetu
                flag = struct.unpack("<I", d[0:4])[0]
                if flag == 1 and len(d) >= 8:
                    self.dist_valid = True
                    self.dist = struct.unpack("<f", d[4:8])[0]
                else:
                    self.dist_valid = False
                    self.dist = None
            elif typ == PHASE and len(d) == 12:
                tot, br_ph, hr_ph = struct.unpack("<fff", d)
                self.breath_phase.append(br_ph)
                self.heart_phase.append(hr_ph)
            elif typ not in TYPE_NAME:
                if len(self.unknown) < 20:
                    self.unknown.append((typ, d.hex(" ")))

    def is_present(self):
        """Obecnosc = wykryto zywe parametry (tetno/oddech) w ostatnich PRESENCE_HOLD s."""
        return (time.monotonic() - self.last_vital) < PRESENCE_HOLD


def print_banner(rd):
    print("=" * 60)
    print(" Andar ADTE2104 v2.0  —  identyfikacja czujnika")
    print("=" * 60)
    print(f"  Chip / rodzina : Andar ADT6101P (HLK-LD6002-compatible)")
    print(f"  Technologia    : 60 GHz FMCW, 2T2R, vital-signs")
    print(f"  Port / baud    : {PORT} @ {BAUD} 8N1")
    print(f"  Protokol       : LD6002 TLV (float32 LE)")
    time.sleep(1.5)  # zbierz strumienie
    with rd.lock:
        seen = dict(rd.seen_types)
        unknown = list(rd.unknown)
    print(f"  Wykryte strumienie:")
    for t, n in sorted(seen.items()):
        print(f"     0x{t:04X} {TYPE_NAME.get(t,'?'):12s} x{n}")
    if unknown:
        print("  Nieznane ramki (mozliwy banner/wersja firmware):")
        for t, h in unknown:
            print(f"     0x{t:04X}: {h}")
    else:
        print("  Wersja firmware: NIE wystawiana w strumieniu danych "
              "(protokol LD6002 nie ma pola wersji).")
    print("=" * 60)


def build_dashboard(rd):
    """Buduje figure dashboardu i zwraca (fig, update) — wspolne dla trybu live i zrzutu."""
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(11, 7))
    try:
        fig.canvas.manager.set_window_title("ADTE2104 — Vital Signs")
    except Exception:
        pass  # brak managera (backend Agg / zrzut)
    gs = fig.add_gridspec(3, 3, height_ratios=[1, 1.3, 1.3], hspace=0.45, wspace=0.3)

    ax_txt = fig.add_subplot(gs[0, :]); ax_txt.axis("off")
    t_hr = ax_txt.text(0.02, 0.5, "", fontsize=42, fontweight="bold", color="#d6336c", va="center")
    t_br = ax_txt.text(0.40, 0.7, "", fontsize=20, va="center")
    t_di = ax_txt.text(0.40, 0.25, "", fontsize=20, va="center")
    t_pr = ax_txt.text(0.72, 0.5, "", fontsize=24, fontweight="bold", va="center")

    ax_hp = fig.add_subplot(gs[1, :]); ax_hp.set_title("Faza sercowa (przebieg)")
    ax_hp.set_ylabel("faza"); l_hp, = ax_hp.plot([], [], color="#d6336c", lw=1.4)
    ax_bp = fig.add_subplot(gs[2, :]); ax_bp.set_title("Faza oddechowa (przebieg)")
    ax_bp.set_ylabel("faza"); ax_bp.set_xlabel("probki"); l_bp, = ax_bp.plot([], [], color="#1c7ed6", lw=1.4)

    def update(_):
        with rd.lock:
            hr, br, dist = rd.hr, rd.br, rd.dist
            present = rd.is_present()
            hp = list(rd.heart_phase); bp = list(rd.breath_phase)
        t_hr.set_text(f"{hr:.0f} BPM" if hr else "-- BPM")
        t_br.set_text(f"Oddech: {br:.1f} /min" if br else "Oddech: --")
        t_di.set_text(f"Dystans: {dist:.0f} cm" if dist else "Dystans: --")
        t_pr.set_text("● OBECNOSC" if present else "○ brak")
        t_pr.set_color("#2f9e44" if present else "#adb5bd")
        if hp:
            l_hp.set_data(range(len(hp)), hp); ax_hp.relim(); ax_hp.autoscale_view()
        if bp:
            l_bp.set_data(range(len(bp)), bp); ax_bp.relim(); ax_bp.autoscale_view()
        return l_hp, l_bp

    return fig, update


def run_live(rd):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    fig, update = build_dashboard(rd)
    ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
    try:
        plt.show()
    finally:
        rd.running = False


def run_shot(rd, path, secs=8.0):
    """Headless zrzut dashboardu do PNG po zebraniu 'secs' sekund danych."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    print(f"Zbieram dane {secs:.0f} s do zrzutu…")
    time.sleep(secs)
    fig, update = build_dashboard(rd)
    update(0)
    fig.savefig(path, dpi=110, bbox_inches="tight")
    rd.running = False
    print(f"Zapisano zrzut: {path}")


def main():
    args = sys.argv[1:]
    shot = None
    if "--shot" in args:
        idx = args.index("--shot")
        shot = args[idx + 1] if idx + 1 < len(args) else "dashboard.png"
        del args[idx:idx + 2]
    global PORT
    if args:
        PORT = args[0]
    try:
        rd = Reader(PORT, BAUD)
    except serial.SerialException as e:
        print(f"Blad otwarcia {PORT} @ {BAUD}: {e}")
        return
    rd.start()
    print_banner(rd)
    if shot:
        run_shot(rd, shot)
    else:
        run_live(rd)


if __name__ == "__main__":
    main()
