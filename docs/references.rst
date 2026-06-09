References
==========

Vendor documentation (Hi-Link / Andar)
---------------------------------------

- `HLK-LD6002 — 60 GHz breathing & heart-rate radar (Shenzhen Hi-Link)
  <https://www.hlktech.net/index.php?id=1180>`_ — product page of the module
  compatible with the ADTE2104; **ADT6101P** chip, UART default **1 382 400 baud**,
  no parity.
- `HLK-LD6002 — manual (manuals.plus)
  <https://manuals.plus/m/53b7125a37e085cd52122b49edfad57af10432b14394d39b45b61d427c80497b>`_
  — module and UART interface description.
- `LD6002 / LD6002B / LD6002C datasheet (manuals.plus)
  <https://manuals.plus/ae/1005005458549623>`_ — testboard variant and pinout.

Protocol implementations (open source)
--------------------------------------

- `icewind1991/hlk_ld6002 <https://github.com/icewind1991/hlk_ld6002>`_ — Rust
  library; source of the frame-type definitions (``Phase 0x0A13``,
  ``Respiratory 0x0A14``, ``Heartbeat 0x0A15``, ``Distance 0x0A16``) and the
  float32 decoding.
- `phuongnamzz/HLK-LD6002 <https://github.com/phuongnamzz/HLK-LD6002>`_ — Arduino
  library for the same module.

Further reading
---------------

- `Estimation of Human Body Vital Signs Based on 60 GHz Doppler Radar (PMC)
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6068558/>`_ — theoretical background
  for radar-based 60 GHz vital-signs measurement.
- `Seeed Studio MR60BHA2 — 60 GHz module based on Andar
  <https://wiki.seeedstudio.com/getting_started_with_mr60bha2_mmwave_kit/>`_ —
  a related module of the same family (a different, higher-level TLV protocol
  with SOF ``0x01``).

.. note::

   The name **ADTE2104** does not appear in the vendor's public documentation;
   the identification (ADT6101P / LD6002 family) was established from the UART
   protocol compatibility confirmed empirically and against the libraries above.
