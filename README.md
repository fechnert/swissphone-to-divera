# Swissphone to Divera

Read and parse (POCSAG) messages of any [Swissphone] pager with a serial port and forward these to [Divera 24/7].


## About

Swissphone has various pager models which can output the received (and decrypted) message via RS232 / USB interface.
Just to mention a few, here are some of these models with their main drawback:

- [MS POCSAG], not available in Germany
- [DiCal-RED], rather expensive, focused on vehicle communication
- BOSS 925, discontinued but possible to buy from other vendors

For commercial use the [DiCal-RED] is mainly used.

For individual use, the BOSS 925 is often recommended due to its low cost. It's the only "normal" (mobile, handheld)
model which has the IDEA decryption module built-in and can output the decrypted message via a serial port. It is also
still widely available on different reseller sites and can be repaired or even improved or extended with spare parts of
the same Series.


## Why another implementation?

Current solutions are either totally outdated, only built for a specific  operating system like Windows (see [BosMon])
or hard to configure and maintain for a longer period of time without checking every day if everything is still running
smoothly.

I used different solutions and products which are great, but lacked at least some of the following features. So i simply
built my own, which fits perfectly for me, but may also be interesting to others.


## Features

- **Works on Linux** - Can be deployed on small computers like NUCs or even single board computers like the
  [Raspberry Pi] or any other kind of non-windows machine.

- **Easy to setup** - Simply pull the code and adjust one easy to read and easy to change yaml file which contains all
  important configurations.

- **Easy to adjust** - Its python, simply switch out the `Parser` class with your own implementation to match your
  message style or edge cases.


## To Do's

- **Provide your own parsers** - Provide the possibility to easily add (or configure) and use your own parser implementation without having to adjust the `lib/parser.py` file.

- **Extendable via plugins** - Provide the option to add plugins for more specific use cases
  like alert triggering on power disruption, built-in geocoding or even printer communication or speaker support.

- **Built in monitoring** - Trigger an alert if the pager seems to be turned off or this tool isn't even running.


## Usage

_Coming soon!_


[Swissphone]: https://www.swissphone.com/
[Divera 24/7]: https://www.divera247.com
[MS POCSAG]: https://www.swissphone.com/product/ms-pocsag/
[DiCal-RED]: https://www.swissphone.com/product/dical-red/
[BosMon]: https://www.bosmon.de/
[Raspberry Pi]: https://www.raspberrypi.org/products/
