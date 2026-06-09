Protokół UART
=============

Moduł **Andar ADTE2104 v2.0** to radar 60 GHz FMCW oparty na chipie
**Andar ADT6101P**, protokołowo zgodny z modułem **HLK-LD6002** firmy
`Shenzhen Hi-Link Electronic <https://www.hlktech.net/index.php?id=1180>`_.
Poniższy opis odtworzono na żywo z urządzenia i potwierdzono względem
otwartej biblioteki `icewind1991/hlk_ld6002
<https://github.com/icewind1991/hlk_ld6002>`_.

Parametry portu
---------------

============  ==============================================================
Parametr      Wartość
============  ==============================================================
Baud          **1 382 400**
Format        8N1 (8 bitów danych, bez parzystości, 1 bit stopu)
Kodowanie     liczby zmiennoprzecinkowe **float32 little-endian**
============  ==============================================================

.. warning::

   ``stty`` / sterownik CP2104 może nie ustawić 1 382 400 baud. Odczyt na
   460800 daje **fałszywe** 19-bajtowe ramki (aliasing ``1382400 / 460800 = 3``).
   Otwieraj port przez :class:`serial.Serial` (pyserial), które ustawia baud
   przez termios.

Struktura ramki (TLV)
---------------------

.. code-block:: text

   +------+--------+--------+--------+------+------------+------+
   | SOF  |  ID    |  LEN   |  TYPE  | HCK  |   DATA      | DCK  |
   | 0x01 | 2 B BE | 2 B BE | 2 B BE | 1 B  |  LEN bajtów | 1 B  |
   +------+--------+--------+--------+------+------------+------+

- **SOF** — bajt startu, zawsze ``0x01``
- **ID** — identyfikator (uint16, big-endian)
- **LEN** — długość pola ``DATA`` (uint16, big-endian)
- **TYPE** — typ wiadomości (uint16, big-endian; tabela niżej)
- **HCK** — suma kontrolna nagłówka: ``~XOR(bajty 0..6) & 0xFF``
- **DATA** — ładunek o długości ``LEN``
- **DCK** — suma kontrolna danych: ``~XOR(DATA) & 0xFF``

Typy wiadomości
---------------

.. list-table::
   :header-rows: 1
   :widths: 12 18 10 60

   * - TYPE
     - Znaczenie
     - LEN
     - Dekodowanie ``DATA``
   * - ``0x0A13``
     - Phase
     - 12 B
     - 3× float32 LE: faza całkowita / oddechowa / sercowa
   * - ``0x0A14``
     - Respiratory
     - 4 B
     - float32 LE — oddechy na minutę
   * - ``0x0A15``
     - **Heartbeat**
     - 4 B
     - float32 LE — **tętno w BPM**
   * - ``0x0A16``
     - Distance
     - 8 B
     - uint32 ``flaga`` + float32 LE ``dystans`` [cm]
   * - ``0x0A16``
     - Distance
     - 4 B
     - brak celu (sam ``flaga`` ≠ 1)

Dla ramki **Distance** ``flaga == 1`` oznacza ważny pomiar (cel wykryty);
inna wartość lub krótszy (4 B) wariant oznacza brak celu.

Przykład dekodowania
--------------------

Ramka tętna (``TYPE = 0x0A15``, ``LEN = 4``), ``DATA = 00 00 92 42``:

.. code-block:: python

   import struct
   struct.unpack("<f", bytes.fromhex("00009242"))[0]   # -> 73.0  (BPM)

Weryfikacja sum kontrolnych:

.. code-block:: python

   def cksum(data: bytes) -> int:
       x = 0
       for b in data:
           x ^= b
       return (~x) & 0xFF

Detekcja obecności
------------------

Flaga w ramce ``Distance`` reaguje też na nieruchome odbicia (ściany, meble),
dlatego aplikacja wyznacza **obecność człowieka** na podstawie wykrytych
parametrów życiowych (tętno/oddech > 0) z podtrzymaniem ``PRESENCE_HOLD``
sekund — patrz :meth:`adte2104_dashboard.Reader.is_present`.
