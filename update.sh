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
  'nvidia/cuda:7.5-cudnn5-devel' \
  '# CUDA 7.5-specific steps
RUN conda install -y --name pytorch-py36 -c soumith \
    magma-cuda75 \
 && conda clean -ya'

# CUDA 8.0
make_dockerfile \
  'cuda-8.0/Dockerfile' \
  'nvidia/cuda:8.0-cudnn5-devel' \
  '# CUDA 8.0-specific steps
RUN conda install -y --name pytorch-py36 -c soumith \
    magma-cuda80 \
 && conda clean -ya'

# No CUDA
make_dockerfile \
  'no-cuda/Dockerfile' \
  'ubuntu:16.04' \
  '# No CUDA-specific steps
ENV NO_CUDA=1'
