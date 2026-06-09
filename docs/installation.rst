Installation
============

Requirements
------------

- **Linux** with serial-port access (user in the ``dialout`` group, no ``sudo``).
- **Python 3.10+**.
- A graphical environment for live mode (matplotlib opens a GUI window).
  The screenshot mode (``--shot``) runs headless.
- A USB-UART bridge supporting **1 382 400 baud** (e.g. **Silicon Labs CP2104**,
  CP2102N, FTDI FT232H). Cheaper/slower adapters may fail to set this baud rate.

The module
----------

.. list-table::
   :widths: 33 33 33

   * - .. figure:: _static/adte2104_front.png
          :width: 100%

          Front — 2T2R patch antennas (Andar)
     - .. figure:: _static/adte2104_back.png
          :width: 100%

          Back — ADT6101P chip + flash
     - .. figure:: _static/adte2104_pinout.png
          :width: 100%

          Dimensions & pinout (25 × 23 mm)

Board marking: ``ADTM6101PJDM41P04`` (Andar). Images: © Shenzhen Hi-Link
Electronic — `product page <https://www.hlktech.net/index.php?id=1180>`_.

Hardware and wiring
-------------------

3.3 V module:

==========  ==================
Module      USB-UART bridge
==========  ==================
``TX``      ``RX``
``RX``      ``TX``
``GND``     ``GND``
``3V3``     ``3V3``
==========  ==================

.. warning::

   The **1 382 400** baud rate is high enough that ``stty`` / the CP2104 driver
   may fail to set it correctly (reading at 460800 yields seemingly stable but
   **bogus** frames — aliasing, because ``1382400 / 460800 = 3``).
   The application sets the baud rate via **pyserial**, which does it correctly
   (termios), so use it rather than ``cat`` / ``stty``.

Installing dependencies
-----------------------

.. code-block:: bash

   cd heartRate-adte2104-radar
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt

Dependencies (``requirements.txt``): ``pyserial``, ``matplotlib``, ``numpy``.

Building the documentation (optional)
-------------------------------------

.. code-block:: bash

   .venv/bin/pip install -r docs/requirements.txt
   .venv/bin/sphinx-build -b html docs docs/_build/html
   # result: docs/_build/html/index.html
