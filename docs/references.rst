Źródła i materiały
==================

Dokumentacja producenta (Hi-Link / Andar)
-----------------------------------------

- `HLK-LD6002 — 60 GHz radar oddechu i tętna (Shenzhen Hi-Link)
  <https://www.hlktech.net/index.php?id=1180>`_ — strona produktu modułu
  zgodnego z ADTE2104; chip **ADT6101P**, UART domyślnie **1 382 400 baud**,
  bez parzystości.
- `HLK-LD6002 — instrukcja (manuals.plus)
  <https://manuals.plus/m/53b7125a37e085cd52122b49edfad57af10432b14394d39b45b61d427c80497b>`_
  — opis modułu i interfejsu UART.
- `Karta produktu LD6002 / LD6002B / LD6002C (manuals.plus)
  <https://manuals.plus/ae/1005005458549623>`_ — wariant testboardu i piny.

Implementacje protokołu (open source)
-------------------------------------

- `icewind1991/hlk_ld6002 <https://github.com/icewind1991/hlk_ld6002>`_ — biblioteka
  Rust; źródło definicji typów ramek (``Phase 0x0A13``, ``Respiratory 0x0A14``,
  ``Heartbeat 0x0A15``, ``Distance 0x0A16``) i sposobu dekodowania float32.
- `phuongnamzz/HLK-LD6002 <https://github.com/phuongnamzz/HLK-LD6002>`_ — biblioteka
  Arduino dla tego samego modułu.

Materiały dodatkowe
-------------------

- `Estimation of Human Body Vital Signs Based on 60 GHz Doppler Radar (PMC)
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6068558/>`_ — tło teoretyczne pomiaru
  vital-signs radarem 60 GHz.
- `Seeed Studio MR60BHA2 — moduł 60 GHz oparty na Andar
  <https://wiki.seeedstudio.com/getting_started_with_mr60bha2_mmwave_kit/>`_ —
  pokrewny moduł tej samej rodziny (inny, wyższy protokół TLV z SOF ``0x01``).

.. note::

   Nazwa **ADTE2104** nie występuje w publicznej dokumentacji producenta;
   identyfikację (ADT6101P / rodzina LD6002) ustalono na podstawie zgodności
   protokołu UART potwierdzonej empirycznie oraz względem powyższych bibliotek.
