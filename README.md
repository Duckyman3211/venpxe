# VenPXE

**VenPXE** is an open-source network boot system built on python with the iPXE. It acts as a boot USB without USB over standard HTTP/TFTP networks.

## Core Features

* **Web Interface** - Easily change configuration and upload ISO's from a webui.
* **ISO Booting** – Easily manage OS installations directly over the network without complex modifications.
* **Diagnostic Tools** – Comes with different tools to test memory, screens and disks, and tools like live recovery boot images, disk partition manager, hdd eraser and ssd trimmer.
* **Automated Installation Scripts** – Allows you to add different scripts like autounatted.yml, answer files or cloud-init through the webui per ISO.

## Design choices

The entire system is designed to be completely open-source, easy to understand, and lightweight enough to run smoothly on low-power hardware:

* **iPXE Core Layer** – Managing UEFI/Legacy hardware handshakes.
* **Network Layer** – Uses lightweight proxy engines to safely guide clients without altering existing home network router configurations.
* **JSON config files** – Portable config-mapped storage system designed to scale cleanly across systems while being easy to read.

## Getting Started

*Info to be made. Is in active development.*