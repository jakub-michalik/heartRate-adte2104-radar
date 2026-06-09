Uruchomienie
============

Tryb live (dashboard)
---------------------

.. code-block:: bash

   cd heartRate-adte2104-radar
   .venv/bin/python adte2104_dashboard.py

Otworzy się okno z dużym licznikiem **BPM**, oddechem, dystansem, statusem
obecności oraz przebiegami fazy sercowej i oddechowej. Zamknięcie okna lub
``Ctrl-C`` kończy program.

Wybór portu
-----------

Domyślny port to ``/dev/ttyUSB1``. Inny podajesz jako pierwszy argument:

.. code-block:: bash

   .venv/bin/python adte2104_dashboard.py /dev/ttyUSB0

Zalecany jest **stały alias** niezależny od kolejności podłączania USB:

.. code-block:: bash

   .venv/bin/python adte2104_dashboard.py \
     /dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_XXXX-if00-port0

Identyfikator znajdziesz przez ``ls /dev/serial/by-id/``.

Zrzut ekranu (headless)
-----------------------

Tryb ``--shot`` zbiera kilka sekund danych i zapisuje render dashboardu do PNG
bez otwierania okna (działa np. na serwerze przez SSH):

.. code-block:: bash

   .venv/bin/python adte2104_dashboard.py --shot docs/_static/dashboard.png

Banner identyfikacji
--------------------

Na starcie aplikacja wypisuje identyfikację modułu i wykryte strumienie danych::

   ============================================================
    Andar ADTE2104 v2.0  —  identyfikacja czujnika
   ============================================================
     Chip / rodzina : Andar ADT6101P (HLK-LD6002-compatible)
     Technologia    : 60 GHz FMCW, 2T2R, vital-signs
     Port / baud    : /dev/ttyUSB1 @ 1382400 8N1
     Protokol       : LD6002 TLV (float32 LE)
     Wykryte strumienie:
        0x0A13 Phase        x70
        0x0A14 Respiratory  x1
        0x0A15 Heartbeat    x2
        0x0A16 Distance     x70

.. note::

   **Wersja firmware** nie jest wystawiana w strumieniu danych — protokół
   LD6002 nie ma takiego pola, a otwarte biblioteki (:ghicewind:`<>`,
   ``phuongnamzz/HLK-LD6002``) również nie udostępniają komendy odczytu wersji.
   Aplikacja loguje wszelkie nieznane ramki, gdyby moduł kiedyś wysłał banner.

Strojenie obecności
-------------------

Obecność wyliczana jest z wykrytych parametrów życiowych z podtrzymaniem.
Próg czasowy zmienisz stałą w ``adte2104_dashboard.py``:

.. code-block:: python

   PRESENCE_HOLD = 4.0   # sekundy — mniej = szybciej gasi, więcej = stabilniej
