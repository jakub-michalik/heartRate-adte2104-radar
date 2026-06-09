Instalacja
==========

Wymagania
---------

- **Linux** z dostępem do portu szeregowego (użytkownik w grupie ``dialout``,
  bez ``sudo``).
- **Python 3.10+**.
- Środowisko graficzne dla trybu live (matplotlib otwiera okno GUI).
  Tryb zrzutu ekranu (``--shot``) działa headless.
- Mostek USB-UART obsługujący **1 382 400 baud** (np. **Silicon Labs CP2104**,
  CP2102N, FTDI FT232H). Tańsze/wolniejsze adaptery mogą nie ustawić tego baudu.

Sprzęt i okablowanie
--------------------

Moduł zasilany **3.3 V**:

==========  ==================
Moduł       Mostek USB-UART
==========  ==================
``TX``      ``RX``
``RX``      ``TX``
``GND``     ``GND``
``3V3``     ``3V3``
==========  ==================

.. warning::

   Baud **1 382 400** jest na tyle wysoki, że ``stty`` / sterownik CP2104 może
   go nie ustawić poprawnie (odczyt na 460800 daje pozornie stabilne, lecz
   **fałszywe** ramki — aliasing, ponieważ ``1382400 / 460800 = 3``).
   Aplikacja ustawia baud przez **pyserial**, które robi to poprawnie
   (termios), więc używaj jej, a nie ``cat``/``stty``.

Instalacja zależności
---------------------

.. code-block:: bash

   cd heartRate-adte2104-radar
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt

Zależności (``requirements.txt``): ``pyserial``, ``matplotlib``, ``numpy``.

Budowanie dokumentacji (opcjonalnie)
------------------------------------

.. code-block:: bash

   .venv/bin/pip install -r docs/requirements.txt
   .venv/bin/sphinx-build -b html docs docs/_build/html
   # wynik: docs/_build/html/index.html
