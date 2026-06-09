Usage
=====

Live mode (dashboard)
---------------------

.. code-block:: bash

   cd heartRate-adte2104-radar
   .venv/bin/python adte2104_dashboard.py

A window opens with a large **BPM** counter, breathing, distance, presence
status, and the heart/breathing phase waveforms. Close the window or press
``Ctrl-C`` to quit.

Selecting the port
------------------

The default port is ``/dev/ttyUSB1``. Provide another one as the first argument:

.. code-block:: bash

   .venv/bin/python adte2104_dashboard.py /dev/ttyUSB0

A **stable alias** that does not depend on USB plug order is recommended:

.. code-block:: bash

   .venv/bin/python adte2104_dashboard.py \
     /dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_XXXX-if00-port0

Find the identifier with ``ls /dev/serial/by-id/``.

Screenshot (headless)
---------------------

The ``--shot`` mode collects a few seconds of data and saves a render of the
dashboard to a PNG without opening a window (works e.g. on a server over SSH):

.. code-block:: bash

   .venv/bin/python adte2104_dashboard.py --shot docs/_static/dashboard.png

Identification banner
---------------------

At startup the application prints the module identification and detected data
streams::

   ============================================================
    Andar ADTE2104 v2.0  —  sensor identification
   ============================================================
     Chip / family  : Andar ADT6101P (HLK-LD6002-compatible)
     Technology     : 60 GHz FMCW, 2T2R, vital-signs
     Port / baud    : /dev/ttyUSB1 @ 1382400 8N1
     Protocol       : LD6002 TLV (float32 LE)
     Detected streams:
        0x0A13 Phase        x70
        0x0A14 Respiratory  x1
        0x0A15 Heartbeat    x2
        0x0A16 Distance     x70

.. note::

   The **firmware version** is not exposed in the data stream — the LD6002
   protocol has no such field, and the open-source libraries
   (:ghicewind:`<>`, ``phuongnamzz/HLK-LD6002``) expose no version command
   either. The application logs any unknown frames in case the module ever
   emits a version banner.

Tuning presence
---------------

Presence is computed from detected vital signs with a hold. Change the time
threshold via the constant in ``adte2104_dashboard.py``:

.. code-block:: python

   PRESENCE_HOLD = 4.0   # seconds — lower = drops faster, higher = more stable
