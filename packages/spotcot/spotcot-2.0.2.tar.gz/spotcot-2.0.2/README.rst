spotcot - Spot Cursor-on-Target Gateway.
****************************************

.. image:: docs/ScreenShot2021-01-08at4.18.37PM.png
   :alt: Screenshot of Spot CoT PLI Point in ATAK
   :target: docs/ScreenShot2021-01-08at4.18.37PM.png

The ``spotcot`` Spot Cursor-on-Target Gateway transforms Spot position messages
into Cursor on Target (CoT) Position Location Information (PLI) Points for
display on Situational Awareness (SA) applications such as the Android Team
Awareness Kit (ATAK), WinTAK, RaptorX, et al. This allows partner agencies to
track affiliated units without exposing existing networks, amongst other uses.

``spotcot`` can be run as a foreground command line application, or can be run
as a background service using a daemon like `supervisor <http://supervisord.org/>`_.

Usage of this gateway requires a `Spot <https://www.findmespot.com/en-us/>`_ device with service.

IF YOU HAVE AN URGENT OPERATIONAL NEED: Email ops@undef.net or call/sms +1-415-598-8226

Wildland Firefighting
=====================
``spotcot`` may also be of use in wildland firefighting, see Section 1114.d of the `Dingell Act <https://www.congress.gov/bill/116th-congress/senate-bill/47/text>`_::

    Location Systems for Wildland Firefighters.--
    (1) In general.--Not later than 2 years after the date of
        enactment of this Act, subject to the availability of
        appropriations, the Secretaries, in coordination with State
        wildland firefighting agencies, shall jointly develop and
        operate a tracking system (referred to in this subsection as the
        ``system'') to remotely locate the positions of fire resources
        for use by wildland firefighters, including, at a minimum, any
        fire resources assigned to Federal type 1 wildland fire incident
        management teams.


Installation
============

To install from this source tree::

    $ git checkout https://github.com/ampledata/spotcot.git
    $ cd spotcot/
    $ python setup.py install

To install from PyPI::

    $ pip install spotcot


Setup
=====

``spotcot`` uses the Spot **XML Feed** feature to retrieve Spot location
messages from the Spot API.

To enable the **XML Feed** feature:

1. Login to your Spot account at: https://login.findmespot.com/spot-main-web/auth/login.html
2. In the navigation bar, click **XML Feed**, then **Create XML Feed**.
3. Enter any value for **XML Feed Name**.
4. *[Optional]* If you select **Make XML page private**, chose and record a password.
5. Click **Create**, record the **XML Feed ID**.

Usage
=====

The `spotcot` daemon has several runtime arguments::

    $ spotcot -h
    usage: spotcot [-h] -U COT_URL [-S COT_STALE] -k API_KEY [-i INTERVAL]
                   [-p PASSWORD]

    optional arguments:
      -h, --help            show this help message and exit
      -U COT_URL, --cot_url COT_URL
                            URL to CoT Destination.
      -S COT_STALE, --cot_stale COT_STALE
                            CoT Stale period, in seconds.
      -k API_KEY, --api_key API_KEY
                            Spot API Key ("XML Feed Id").
      -i INTERVAL, --interval INTERVAL
                            Spot API Query Interval.
      -p PASSWORD, --password PASSWORD
                            Spot Feed Password for private feeds.

For minimum operation, `-k API_KEY` & `-U COT_HOST` are required.

Source
======
Github: https://github.com/ampledata/spotcot

Author
======
Greg Albrecht W2GMD oss@undef.net

http://ampledata.org/

Copyright
=========
Copyright 2021 Orion Labs, Inc.

License
=======
Apache License, Version 2.0. See LICENSE for details.
