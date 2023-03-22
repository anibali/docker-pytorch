# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 2023-03-23

### Added

- The following new Docker images have been added:
  - `2.0.0-cuda11.8-ubuntu22.04`
  - `2.0.0-nocuda-ubuntu22.04

### Changed

- New Dockerfiles have returned to using the `pytorch` and `nvidia` channels
  for PyTorch conda packages.

## 2022-12-12

### Added

- The following new Docker images have been added:
  - `1.13.0-cuda11.8-ubuntu22.04`
  - `1.13.0-nocuda-ubuntu22.04`
- New Docker images include [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).

### Changed

- New Dockerfiles use an explicit [Conda lock file](https://github.com/conda-incubator/conda-lock) for better reproducability of image builds instead of installing from `environment.yml` directly. This generally won't affect users of images, but it does make it easier to see exactly which Conda packages are included in each image (see [dockerfiles/1.13.0-nocuda-ubuntu22.04/conda-linux-64.lock](dockerfiles/1.13.0-nocuda-ubuntu22.04/conda-linux-64.lock), for example). It is still possible to install new packages in derived images/containers using an `environment.yml` file.

### Deprecated

- The following Docker images will remain available on Docker Hub but are no longer supported:
  - `1.7.0-cuda11.0-ubuntu20.04`
  - `1.8.1-cuda11.1-ubuntu20.04`
  - `1.10.0-nocuda-ubuntu20.04`
  - `1.10.0-cuda11.3-ubuntu20.04`
