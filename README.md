# ADTE2104 v2.0 — heart-rate & presence radar (60 GHz)

[![Docs](https://github.com/jakub-michalik/heartRate-adte2104-radar/actions/workflows/docs.yml/badge.svg)](https://github.com/jakub-michalik/heartRate-adte2104-radar/actions/workflows/docs.yml)
[![Docs online](https://img.shields.io/badge/docs-online-brightgreen)](https://jakub-michalik.github.io/heartRate-adte2104-radar/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Live readout and visualization from the **Andar ADTE2104 v2.0** radar (**ADT6101P**
chip, protocol-compatible with **HLK-LD6002**) over UART (CP2104 bridge).

The dashboard shows: **heart rate [BPM]**, breathing [/min], distance [cm], presence,
and the heart/breathing phase waveforms.

![ADTE2104 dashboard — heart rate, breathing, distance, presence](docs/_static/dashboard.png)

## Documentation

📖 **Online:** https://jakub-michalik.github.io/heartRate-adte2104-radar/
(built and published automatically from `main` by GitHub Actions →
[`.github/workflows/docs.yml`](.github/workflows/docs.yml))

Sources live in [`docs/`](docs/) — protocol description, installation, usage,
API and references. Build locally:

```bash
.venv/bin/pip install -r docs/requirements.txt
.venv/bin/sphinx-build -b html docs docs/_build/html
# open docs/_build/html/index.html
```

## Protocol (verified live)

- **UART 1382400 baud, 8N1, no parity.**
  ⚠️ `stty` / CP2104 cannot set such a high baud — you must use **pyserial**
  (`serial.Serial(port, 1382400)`), which sets it via termios. Reading at
  460800 yields seemingly stable but **bogus** frames (aliasing, 1382400 ÷ 3).
- TLV frame: `01 | ID(2 BE) | LEN(2 BE) | TYPE(2 BE) | HCK(1) | DATA[LEN] | DCK(1)`
  - `HCK = ~XOR(bytes 0..6) & 0xFF`, `DCK = ~XOR(DATA) & 0xFF`
  - values: **float32 little-endian**

| TYPE   | Meaning      | Payload                                  |
|--------|--------------|------------------------------------------|
| 0x0A13 | Phase        | 3× f32 (total / breath / heart phase)    |
| 0x0A14 | Respiratory  | f32 — breaths/min                        |
| 0x0A15 | **Heartbeat**| f32 — **BPM**                            |
| 0x0A16 | Distance     | u32 flag + f32 [cm]; flag==1 → present   |

Firmware version is **not** exposed in the stream — the app identifies the module
and logs any unknown frames.

## Installation

```bash
cd ~/repos/heartRate-adte2104-radar
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Usage

```bash
cd ~/repos/heartRate-adte2104-radar
.venv/bin/python adte2104_dashboard.py
```

Default port is `/dev/ttyUSB1`. Use a different one as an argument:

```bash
.venv/bin/python adte2104_dashboard.py /dev/ttyUSB0
```

A stable, plug-order-independent port is recommended:

```bash
.venv/bin/python adte2104_dashboard.py \
  /dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_XXXX-if00-port0
```

Headless screenshot (no GUI window):

```bash
.venv/bin/python adte2104_dashboard.py --shot docs/_static/dashboard.png
```

Close the window or press `Ctrl-C` to quit.

## Requirements

- Linux, serial-port access (be in the `dialout` group, no `sudo`).
- A graphical environment (matplotlib opens a GUI window) — except `--shot`.
- USB-UART bridge supporting **1 382 400 baud** (e.g. Silicon Labs CP2104).

## Wiring

3.3 V module: `TX → RX` (bridge), `RX → TX`, `GND → GND`.

## Protocol references

- HLK-LD6002 (ADT6101P chip): <https://www.hlktech.net/index.php?id=1180>
- icewind1991/hlk_ld6002 (Rust): <https://github.com/icewind1991/hlk_ld6002>
- phuongnamzz/HLK-LD6002 (Arduino): <https://github.com/phuongnamzz/HLK-LD6002>

## License

[MIT](LICENSE) © 2026 Jakub Michalik
