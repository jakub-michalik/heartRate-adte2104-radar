heartRate-adte2104-radar
========================

Live readout and visualization from the 60 GHz **Andar ADTE2104 v2.0** radar
(**ADT6101P** chip, protocol-compatible with **HLK-LD6002**) over UART.
The application decodes the vendor vital-signs protocol and shows
**heart rate (BPM)**, **breathing**, **distance** and **presence**, together
with the heart and breathing phase waveforms.

.. image:: _static/dashboard.png
   :alt: ADTE2104 dashboard — heart rate, breathing, distance, presence
   :width: 100%

.. note::

   This module's protocol is **not** publicly documented under the name
   ADTE2104 — it was reverse-engineered live and confirmed against open-source
   libraries for the compatible HLK-LD6002 module. Details: :doc:`protocol`.

Key features
------------

- 🫀 **Heart rate in BPM** in real time (frame type ``0x0A15``)
- 🌬️ **Breathing rate** [/min] (``0x0A14``)
- 📏 **Distance to target** [cm] + presence flag (``0x0A16``)
- 📈 **Phase waveforms** for heart and breathing (``0x0A13``)
- 🟢 **Presence detection** based on detected vital signs
- 🖥️ **matplotlib** dashboard + screenshot mode (``--shot``)

Quick start
-----------

.. code-block:: bash

   git clone git@github.com:jakub-michalik/heartRate-adte2104-radar.git
   cd heartRate-adte2104-radar
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   .venv/bin/python adte2104_dashboard.py

Table of contents
-----------------

.. toctree::
   :maxdepth: 2

   installation
   usage
   protocol
   api
   references
