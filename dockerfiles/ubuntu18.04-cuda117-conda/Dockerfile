# Start with the base image
FROM nvidia/cuda:11.7.1-base-ubuntu18.04

# Change source to Tsinghua
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# Install Git and curl
RUN apt-get update && apt-get install -y git && apt-get install -y curl

# Install Miniconda
RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda \
    && rm Miniconda3-latest-Linux-x86_64.sh

# Set up Conda in the environment
ENV PATH="/opt/miniconda/bin:$PATH"
RUN conda init bash

# Change source to Tsinghua
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

# Change pip source to Tsinghua
RUN mkdir ~/.pip && echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf

# docker build -t wgeng/ubuntu18.04-cuda117-conda .