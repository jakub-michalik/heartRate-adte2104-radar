UART protocol
=============

The **Andar ADTE2104 v2.0** module is a 60 GHz FMCW radar based on the
**Andar ADT6101P** chip, protocol-compatible with the **HLK-LD6002** module by
`Shenzhen Hi-Link Electronic <https://www.hlktech.net/index.php?id=1180>`_.
The description below was reverse-engineered live from the device and confirmed
against the open-source library `icewind1991/hlk_ld6002
<https://github.com/icewind1991/hlk_ld6002>`_.

Serial parameters
-----------------

============  ==============================================================
Parameter     Value
============  ==============================================================
Baud          **1 382 400**
Format        8N1 (8 data bits, no parity, 1 stop bit)
Encoding      **float32 little-endian** values
============  ==============================================================

.. warning::

   ``stty`` / the CP2104 driver may fail to set 1 382 400 baud. Reading at
   460800 yields **bogus** 19-byte frames (aliasing ``1382400 / 460800 = 3``).
   Open the port via :class:`serial.Serial` (pyserial), which sets the baud
   rate through termios.

Frame structure (TLV)
---------------------

.. code-block:: text

   +------+--------+--------+--------+------+-------------+------+
   | SOF  |  ID    |  LEN   |  TYPE  | HCK  |   DATA       | DCK  |
   | 0x01 | 2 B BE | 2 B BE | 2 B BE | 1 B  |  LEN bytes   | 1 B  |
   +------+--------+--------+--------+------+-------------+------+

- **SOF** — start-of-frame byte, always ``0x01``
- **ID** — identifier (uint16, big-endian)
- **LEN** — length of the ``DATA`` field (uint16, big-endian)
- **TYPE** — message type (uint16, big-endian; see table below)
- **HCK** — header checksum: ``~XOR(bytes 0..6) & 0xFF``
- **DATA** — payload of length ``LEN``
- **DCK** — data checksum: ``~XOR(DATA) & 0xFF``

Message types
-------------

.. list-table::
   :header-rows: 1
   :widths: 12 18 10 60

   * - TYPE
     - Meaning
     - LEN
     - ``DATA`` decoding
   * - ``0x0A13``
     - Phase
     - 12 B
     - 3× float32 LE: total / breathing / heart phase
   * - ``0x0A14``
     - Respiratory
     - 4 B
     - float32 LE — breaths per minute
   * - ``0x0A15``
     - **Heartbeat**
     - 4 B
     - float32 LE — **heart rate in BPM**
   * - ``0x0A16``
     - Distance
     - 8 B
     - uint32 ``flag`` + float32 LE ``distance`` [cm]
   * - ``0x0A16``
     - Distance
     - 4 B
     - no target (``flag`` ≠ 1)

For the **Distance** frame, ``flag == 1`` means a valid measurement (target
detected); any other value or the shorter (4 B) variant means no target.

Decoding example
----------------

Heart-rate frame (``TYPE = 0x0A15``, ``LEN = 4``), ``DATA = 00 00 92 42``:

.. code-block:: python

   import struct
   struct.unpack("<f", bytes.fromhex("00009242"))[0]   # -> 73.0  (BPM)

Checksum verification:

.. code-block:: python

   def cksum(data: bytes) -> int:
       x = 0
       for b in data:
           x ^= b
       return (~x) & 0xFF

Presence detection
------------------

The flag in the ``Distance`` frame also reacts to static reflections (walls,
furniture), so the application derives **human presence** from detected vital
signs (heart/breath > 0) with a hold of ``PRESENCE_HOLD`` seconds — see
:meth:`adte2104_dashboard.Reader.is_present`.
