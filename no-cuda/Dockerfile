FROM ubuntu:16.04

# Install curl and sudo
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
 && rm -rf /var/lib/apt/lists/*

# Use Tini as the init process with PID 1
RUN curl -Lso /tini https://github.com/krallin/tini/releases/download/v0.14.0/tini \
 && chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# Install Git, bzip2, and X11 client
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    git \
    bzip2 \
    libx11-6 \
 && sudo rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN curl -so ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.3.14-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh

# Create a Python 3.6 environment
RUN /home/user/miniconda/bin/conda install conda-build \
 && /home/user/miniconda/bin/conda create -y --name pytorch-py36 \
    python=3.6.0 numpy pyyaml scipy ipython mkl \
 && /home/user/miniconda/bin/conda clean -ya
ENV PATH=/home/user/miniconda/envs/pytorch-py36/bin:$PATH \
    CONDA_DEFAULT_ENV=pytorch-py36 \
    CONDA_PREFIX=/home/user/miniconda/envs/pytorch-py36

# No CUDA-specific steps
ENV NO_CUDA=1

# Install PyTorch and Torchvision
RUN conda install -y --name pytorch-py36 -c soumith \
    pytorch=0.2.0 torchvision=0.1.9 \
 && conda clean -ya

# Install HDF5 Python bindings
RUN conda install -y --name pytorch-py36 \
    h5py \
 && conda clean -ya
RUN pip install h5py-cache

# Install Torchnet, a high-level framework for PyTorch
RUN pip install git+https://github.com/pytorch/tnt.git@master

# Install Requests, a Python library for making HTTP requests
RUN conda install -y --name pytorch-py36 requests && conda clean -ya

# Install Graphviz
RUN conda install -y --name pytorch-py36 graphviz=2.38.0 \
 && conda clean -ya
RUN pip install graphviz

# Install OpenCV3 Python bindings
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    libgtk2.0-0 \
    libcanberra-gtk-module \
 && sudo rm -rf /var/lib/apt/lists/*
RUN conda install -y --name pytorch-py36 -c menpo opencv3 \
 && conda clean -ya

# Set the default command to python3
CMD ["python3"]
