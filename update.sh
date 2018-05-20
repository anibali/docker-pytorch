#!/bin/bash -e
#
# Create Dockerfiles from template

# Template file
template="Dockerfile.template"
# List of environment variables which will be substituted into the template
shell_format='$BASE:$ADDITIONAL_STEPS'

# Creates a Dockerfile from the template.
# Arguments:
# 1. Output path to write the resulting Dockerfile to
# 2. The base image, substituted into $BASE in the template
# 3. Additional steps to insert into the Dockerfile,
#    substituted into $ADDITIONAL_STEPS in the template
function make_dockerfile {
  dest=$1
  export BASE=$2
  export ADDITIONAL_STEPS=$3

  # Make path to output file
  mkdir -p "$(dirname "$dest")"
  # Fill in the template and write the result to $dest
  envsubst $shell_format < $template > $dest
  # Copy additional files required by the Docker build
  if [ -d "common" ]; then
    cp -r common/. "$(dirname "$dest")"
  fi
}

# CUDA 7.5
make_dockerfile \
  'cuda-7.5/Dockerfile' \
  'nvidia/cuda:7.5-runtime-ubuntu14.04' \
  '# CUDA 7.5-specific steps
RUN conda install -y -c pytorch \
    cuda75=1.0 \
    magma-cuda75=2.2.0 \
    pytorch=0.3.0 \
    torchvision=0.2.0 \
 && conda clean -ya'

# CUDA 8.0
make_dockerfile \
  'cuda-8.0/Dockerfile' \
  'nvidia/cuda:8.0-runtime-ubuntu16.04' \
  '# CUDA 8.0-specific steps
RUN conda install -y -c pytorch \
    cuda80=1.0 \
    magma-cuda80=2.3.0 \
    pytorch=0.4.0 \
    torchvision=0.2.1 \
 && conda clean -ya'

# CUDA 9.1
make_dockerfile \
  'cuda-9.1/Dockerfile' \
  'nvidia/cuda:9.1-base-ubuntu16.04' \
  '# CUDA 9.1-specific steps
RUN conda install -y -c pytorch \
    cuda91=1.0 \
    magma-cuda91=2.3.0 \
    pytorch=0.4.0 \
    torchvision=0.2.1 \
 && conda clean -ya'

# No CUDA
make_dockerfile \
  'no-cuda/Dockerfile' \
  'ubuntu:16.04' \
  '# No CUDA-specific steps
ENV NO_CUDA=1
RUN conda install -y -c pytorch \
    pytorch=0.4.0 \
    torchvision=0.2.1 \
 && conda clean -ya'
