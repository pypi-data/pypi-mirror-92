***************
Release History
***************

v0.1.2 (2021-01-26)
===================
* fix the ``TwoButtonShutter`` class to be compatible with ophyd 1.6.0+

v0.1.1 (2020-10-26)
===================
* update manifest and license files
* make minimal traceback reporting optional
* changes to allow 'nslsii' to load without IPython
* update the status of the xspress3 detector on unstaging

v0.1.0 (2020-09-04)
===================
* synchronize xspress3 code with hxntools
* new TwoButtonShutter configuration
* change Signal.value to Signal.get()
* handle Kafka exceptions

v0.0.17 (2020-08-06)
====================
* update the function that subscribes a Kafka producer to the RunEngine

v0.0.16 (2020-06-26)
====================
* create the default logging directory if it does not exist

v0.0.15 (2020-06-16)
====================
* use appdirs to determine default logging directory
* add a function to subscribe a Kafka producer to the RunEngine

v0.0.10 (2019-06-06)
====================

Features
--------
* Add EPSTwoStateIOC class for simulation
