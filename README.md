## PyTorch Docker image

[![Docker Automated build](https://img.shields.io/docker/automated/anibali/pytorch.svg)](https://hub.docker.com/r/anibali/pytorch/)

Ubuntu + PyTorch + CUDA (optional)


### Requirements

In order to use this image you must have Docker Engine installed. Instructions
for setting up Docker Engine are
[available on the Docker website](https://docs.docker.com/engine/installation/).

#### CUDA requirements

If you have a CUDA-compatible NVIDIA graphics card, you can use a CUDA-enabled
version of the PyTorch image to enable hardware acceleration. I have only
tested this in Ubuntu Linux.

Firstly, ensure that you install the appropriate NVIDIA drivers and libraries.
If you are running Ubuntu, you can install proprietary NVIDIA drivers
[from the PPA](https://launchpad.net/~graphics-drivers/+archive/ubuntu/ppa)
and CUDA [from the NVIDIA website](https://developer.nvidia.com/cuda-downloads).

You will also need to install `nvidia-docker2` to enable GPU device access
within Docker containers. This can be found at
[NVIDIA/nvidia-docker](https://github.com/NVIDIA/nvidia-docker).


### Prebuilt images

Pre-built images are available on Docker Hub under the name
[anibali/pytorch](https://hub.docker.com/r/anibali/pytorch/). For example,
you can pull the CUDA 10.0 version with:

```bash
$ docker pull anibali/pytorch:cuda-10.0
```

The table below lists software versions for each of the currently supported
Docker image tags available for `anibali/pytorch`.

| Image tag   | CUDA  | PyTorch |
|-------------|-------|---------|
| `no-cuda`   | None  | 1.0.0   |
| `cuda-10.0` | 10.0  | 1.0.0   |
| `cuda-9.0`  | 9.0   | 1.0.0   |
| `cuda-8.0`  | 8.0   | 1.0.0   |

The following images are also available, but are deprecated.

| Image tag  | CUDA | PyTorch |
|------------|------|---------|
| `cuda-9.2` | 9.2  | 0.4.1   |
| `cuda-9.1` | 9.1  | 0.4.0   |
| `cuda-7.5` | 7.5  | 0.3.0   |


### Usage

#### Running PyTorch scripts

It is possible to run PyTorch programs inside a container using the
`python3` command. For example, if you are within a directory containing
some PyTorch project with entrypoint `main.py`, you could run it with
the following command:

```sh
docker run --rm -it --init \
  --runtime=nvidia \
  --ipc=host \
  --user="$(id -u):$(id -g)" \
  --volume="$PWD:/app" \
  -e NVIDIA_VISIBLE_DEVICES=0 \
  anibali/pytorch python3 main.py
```

Here's a description of the Docker command-line options shown above:

* `--runtime=nvidia`: Required if using CUDA, optional otherwise. Passes the
  graphics card from the host to the container.
* `--ipc=host`: Required if using multiprocessing, as explained at
  https://github.com/pytorch/pytorch#docker-image.
* `--user="$(id -u):$(id -g)"`: Sets the user inside the container to match your
  user and group ID. Optional, but is useful for writing files with correct
  ownership.
* `--volume="$PWD:/app"`: Mounts the current working directory into the container.
  The default working directory inside the container is `/app`. Optional.
* `-e NVIDIA_VISIBLE_DEVICES=0`: Sets an environment variable to restrict which
  graphics cards are seen by programs running inside the container. Set to `all`
  to enable all cards. Optional, defaults to all.

You may wish to consider using [Docker Compose](https://docs.docker.com/compose/)
to make running containers with many options easier. At the time of writing,
only version 2.3 of Docker Compose configuration files supports the `runtime`
option.

#### Running graphical applications

If you are running on a Linux host, you can get code running inside the Docker
container to display graphics using the host X server (this allows you to use
OpenCV's imshow, for example). Here we describe a quick-and-dirty (but INSECURE)
way of doing this. For a more comprehensive guide on GUIs and Docker check out
http://wiki.ros.org/docker/Tutorials/GUI.

On the host run:

```sh
sudo xhost +local:root
```

You can revoke these access permissions later with `sudo xhost -local:root`.
Now when you run a container make sure you add the options `-e "DISPLAY"` and
`--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"`. This will provide the container
with your X11 socket for communication and your display ID. Here's an
example:

```sh
docker run --rm -it --init \
  --runtime=nvidia \
  -e "DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  anibali/pytorch python3 -c "import tkinter; tkinter.Tk().mainloop()"
```
