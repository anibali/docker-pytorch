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

Firstly, ensure that you install the appropriate NVIDIA drivers. On Ubuntu,
I've found that the easiest way of ensuring that you have the right version
of the drivers set up is by installing a version of CUDA _at least as new as
the image you intend to use_ via
[the official NVIDIA CUDA download page](https://developer.nvidia.com/cuda-downloads).
As an example, if you intend on using the `cuda-10.1` image then setting up
CUDA 10.1 or CUDA 10.2 should ensure that you have the correct graphics drivers.

You will also need to install the NVIDIA Container Toolkit to enable GPU device
access within Docker containers. This can be found at
[NVIDIA/nvidia-docker](https://github.com/NVIDIA/nvidia-docker).


### Prebuilt images

Prebuilt images are available on Docker Hub under the name
[anibali/pytorch](https://hub.docker.com/r/anibali/pytorch/).

For example, you can pull an image with PyTorch 1.5.0 and CUDA 10.2 using:

```bash
$ docker pull anibali/pytorch:1.5.0-cuda10.2
```


### Usage

#### Running PyTorch scripts

It is possible to run PyTorch programs inside a container using the
`python3` command. For example, if you are within a directory containing
some PyTorch project with entrypoint `main.py`, you could run it with
the following command:

```sh
docker run --rm -it --init \
  --gpus=all \
  --ipc=host \
  --user="$(id -u):$(id -g)" \
  --volume="$PWD:/app" \
  anibali/pytorch python3 main.py
```

Here's a description of the Docker command-line options shown above:

* `--gpus=all`: Required if using CUDA, optional otherwise. Passes the
  graphics cards from the host to the container. You can also more precisely
  control which graphics cards are exposed using this option (see documentation
  at https://github.com/NVIDIA/nvidia-docker).
* `--ipc=host`: Required if using multiprocessing, as explained at
  https://github.com/pytorch/pytorch#docker-image.
* `--user="$(id -u):$(id -g)"`: Sets the user inside the container to match your
  user and group ID. Optional, but is useful for writing files with correct
  ownership.
* `--volume="$PWD:/app"`: Mounts the current working directory into the container.
  The default working directory inside the container is `/app`. Optional.

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
  --gpus=all \
  -e "DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  anibali/pytorch python3 -c "import tkinter; tkinter.Tk().mainloop()"
```
