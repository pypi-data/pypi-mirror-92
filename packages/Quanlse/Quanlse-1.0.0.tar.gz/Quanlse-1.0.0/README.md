English | [简体中文](README_CN.md)

![](https://release-data.cdn.bcebos.com/Quanlse_title_en.png)

[![](https://img.shields.io/badge/license-Apache%202.0-green)](./LICENSE) [![](https://img.shields.io/badge/build-passing-green)]() ![](https://img.shields.io/badge/Python-3.6--3.8-blue) ![](https://img.shields.io/badge/release-v1.0.0-blue)

[Quanlse (量脉)](https://quanlse.baidu.com) is a cloud-based platform for quantum control developed by the [Institute for Quantum Computing at Baidu Research](https://quantum.baidu.com). Quanlse aims to bridge the gap between quantum software and hardware. It provides efficient and professional quantum control solutions via an open-source SDK strengthened by the Quanlse Could Service.

Quanlse supports the pulse generation and scheduling of arbitrary single-qubit and two-qubit gates. With the help of toolkits in Quanlse, one can also use Quanlse for modeling physical devices, simulating dynamical evolution, and visualizing error analysis. More interestingly, users can achieve pulse-level control of quantum algorithms using the tools in Quanlse. Furthermore, Quanlse also supports advanced research and development (R&D) in the field of quantum control.

## Install

We highly recommend using [Anaconda](https://www.anaconda.com/) for your R&D environment for the best experience.

### Install via pip

We recommend the following way of installing Quanlse with `pip`,

```bash
pip install Quanlse
```

### Download and install via Github

You can also download all the files and install Quanlse locally,

```bash
git clone http://github.com/baidu/Quanlse
cd Quanlse
pip install -e .
```

### Run programs

Now, you can try to run a program to verify whether Quanlse has been installed successfully.

```bash
cd Example
python 1-Example-Pi-Pulse.py
```

## Introduction and developments

### Overview

To get start with Quanlse, users are recommended to go through the [Overview](https://quanlse.baidu.com/#/doc/overview) firstly to acquire the whole picture of this platform. Then, Quick Start could be a good place to guide you on how to use Quanlse Cloud Service step by step and how to construct your first program using Quanlse. Next, users are encouraged to learn more functions and applications from the [Turorials](https://quanlse.baidu.com/#/doc/tutorial-overview) Quanlse provided. Finally, it would be great if users could solve their own problems using Quanlse. For a complete and detailed documentation of the Quanlse Python SDK API, please refer to our [API documentation page](https://quanlse.baidu.com/api/).

### Tutorials

Quanlse provides detailed and comprehensive tutorials from fundamental to advanced topics. Each tutorial currently supports reading on our [website](https://quanlse.baidu.com/#/doc/tutorial-overview). For interested developers, we recommend them to download [Jupyter Notebooks](https://github.com/baidu/Quanlse/tree/master/Tutorial) and play around with it. The tutorial list is as follows:

- **Single Qubit Control**
    1. [Single-Qubit Gate](https://quanlse.baidu.com/#/doc/tutorial-single-qubit)
    2. [Calibrate Pi Pulse](https://quanlse.baidu.com/#/doc/tutorial-pi-pulse)
- **Two Qubits Control**
    1. [iSWAP Gate](https://quanlse.baidu.com/#/doc/tutorial-iswap)
    2. [Controlled-Z Gate](https://quanlse.baidu.com/#/doc/tutorial-cz)
    3. [Cross-Resonance Gate](https://quanlse.baidu.com/#/doc/tutorial-cr)
- **Advanced Content**
    2. [Derivative Removal by Adiabatic Gate](https://quanlse.baidu.com/#/doc/tutorial-drag)
    2. [Error Analysis](https://quanlse.baidu.com/#/doc/tutorial-error-analysis)
    3. [Quanlse Scheduler](https://quanlse.baidu.com/#/doc/tutorial-scheduler)
    4. [Pulse-based Variational Quantum Eigensolver Algorithm](https://quanlse.baidu.com/#/doc/tutorial-pbvqe)

In addition, Quanlse also supports quantum control for nuclear magnetic resonance (NMR) quantum computing. For more information about [QuanlseNMR](https://nmr.baidu.com/en/), please refer to [Tutorial: QuanlseNMR](https://quanlse.baidu.com/#/doc/nmr).


## Feedbacks

Users are encouraged to contact us through [Github Issues](https://github.com/baidu/Quanlse/issues) or quanlse@baidu.com with general questions, bugs, and potential improvements. We hope to make Quanlse better together with the community!

## Frequently Asked Questions

**Q: How can I learn to use Quanlse?**

**A:** Quanlse provides detailed learning materials, please visit our [website](https://quanlse.baidu.com/#/doc/tutorial-overview).

**Q: What should I do when I run out of my credit points?**  

**A:** Please contact us on [Quantum Hub](https://quantum-hub.baidu.com). First, you should log into Quantum Hub, then enter the "User Management -> Feedback" page, and input the necessary information (choose "Get More Credit Points"). Finally submit your feedback and wait for a reply.

**Q: How should I cite Quanlse in my research?**  

**A:** We highly encourage developers to use Quanlse as a research tool to do research & development in the field of quantum control. Please cite us by including [BibTeX file](Quanlse.bib).

## Changelog

The changelog of this project can be found in [CHANGELOG.md](CHANGELOG.md).

## Copyright and License

Quanlse uses [Apache-2.0 license](LICENSE).

## References

[1] [Quantum Computing - Wikipedia](https://en.wikipedia.org/wiki/Quantum_computing).

[2] Nielsen, M. A. & Chuang, I. L. Quantum computation and quantum information. (Cambridge University Press, 2010).

[3] [Werschnik, J. & Gross, E. K. U. Quantum optimal control theory. J. Phys. B At. Mol. Opt. Phys. 40, R175 (2007)](https://doi.org/10.1088/0953-4075/40/18/R01).

[4] [Wendin, G. Quantum information processing with superconducting circuits: A review. Reports Prog. Phys. 80, (2017)](https://doi.org/10.1088/1361-6633/aa7e1a).

[5] [Krantz, P. et al. A quantum engineer’s guide to superconducting qubits. Appl. Phys. Rev. 6, (2019)](https://doi.org/10.1063/1.5089550).

