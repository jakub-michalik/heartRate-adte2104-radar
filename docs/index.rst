heartRate-adte2104-radar
========================

Odczyt i wizualizacja na żywo z radaru 60 GHz **Andar ADTE2104 v2.0**
(chip **ADT6101P**, protokołowo zgodny z **HLK-LD6002**) podłączonego przez UART.
Aplikacja dekoduje firmowy protokół vital-signs i pokazuje **tętno (BPM)**,
**oddech**, **dystans** oraz **obecność**, wraz z przebiegami fazy sercowej
i oddechowej.

.. image:: _static/dashboard.png
   :alt: Dashboard ADTE2104 — tętno, oddech, dystans, obecność
   :width: 100%

.. note::

   Protokół tego modułu **nie** jest publicznie udokumentowany pod nazwą
   ADTE2104 — został odtworzony (reverse-engineering) na żywo i potwierdzony
   względem otwartych bibliotek dla zgodnego modułu HLK-LD6002.
   Szczegóły: :doc:`protocol`.

Najważniejsze cechy
-------------------

- 🫀 **Tętno w BPM** w czasie rzeczywistym (typ ramki ``0x0A15``)
- 🌬️ **Częstość oddechu** [/min] (``0x0A14``)
- 📏 **Dystans do celu** [cm] + flaga obecności (``0x0A16``)
- 📈 **Przebiegi fazy** sercowej i oddechowej (``0x0A13``)
- 🟢 **Detekcja obecności** na podstawie wykrytych parametrów życiowych
- 🖥️ Dashboard **matplotlib** + tryb zrzutu ekranu (``--shot``)

Szybki start
------------

.. code-block:: bash

   git clone git@github.com:jakub-michalik/heartRate-adte2104-radar.git
   cd heartRate-adte2104-radar
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   .venv/bin/python adte2104_dashboard.py

Spis treści
-----------

.. toctree::
   :maxdepth: 2

   installation
   usage
   protocol
   api
   references
