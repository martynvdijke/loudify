# loudify

> Running a GNU Radio flowgraph as a ZMQ worker.

<!-- ![dev build status](https://github.com/martynvdijke/gr-lora_sdr/workflows/dev%20build%20status/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ad9f936d2d674635b927fd83e57abec1)](https://app.codacy.com/gh/martynvdijke/loudify?utm_source=github.com&utm_medium=referral&utm_content=martynvdijke/loudify&utm_campaign=Badge_Grade_Settings)
[![docs-dev](https://github.com/martynvdijke/gr-lora_sdr/workflows/docs-dev/badge.svg)](https://martynvdijke.github.io/gr-lora_sdr/html/index.html)
![dev test status](https://github.com/martynvdijke/gr-lora_sdr/workflows/dev%20test%20status/badge.svg) -->
[![GitHub license](https://img.shields.io/github/license/martynvdijke/loudify-worker)](https://github.com/martynvdijke/loudify/blob/dev/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/loudfiy_worker)](https://pypi.org/project/loudify_worker)
[![Downloads](https://pepy.tech/badge/loudfiy_worker)](https://pepy.tech/project/loudfiy_worker)
[![PyPI](https://img.shields.io/pypi/v/loudfiy_broker)](https://pypi.org/project/loudify_broker)
[![Downloads](https://pepy.tech/badge/loudfiy_broker)](https://pepy.tech/project/loudfiy_broker)


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/martynvdijke/loudify/settings">
    <img src="pictures/broker.png" alt="Logo">
  </a>

  <h3 align="center">Loudify</h3>

  <p align="center">
    Loudify
    <br />
    <a href="https://martynvdijke.github.io/loudify-worker/html/index.html"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/martynvdijke/loudify-worker/issues">Report a bug</a>
    <a href="https://github.com/martynvdijke/loudify-worker/issues">Request a feature</a>
  </p>
</p>

## Summary
This project consist of three different parts namely the client that is running a GNU Radio flowgraph, 
the worker doing the actual demodulation process and the broker connecting the two together.
This repo holds the code for the worker and broker, but be sure to look at the other repo's to see how everything is tide together.
- [broker](https://github.com/martynvdijke/loudify-broker)
- [worker](https://github.com/martynvdijke/loudify-worker)
- [client](https://github.com/martynvdijke/gr-lora_sdr)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Make sure to add or update tests as appropriate.

## [Changelog](CHANGELOG.md)
