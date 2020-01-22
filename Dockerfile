# Version 1.0 template-transformer-simple 

FROM agpipeline/gantry-base-image:latest
LABEL maintainer="Chris Schnaufer <schnaufer@email.arizona.edu>"

# Build environment values
ARG arg_terrautil_url=https://github.com/terraref/terrautils.git
ENV terrautil_url=$arg_terrautil_url

ARG arg_terrautil_branch=master
ENV terrautil_branch=$arg_terrautil_branch

COPY requirements.txt packages.txt /home/extractor/

USER root

RUN [ -s /home/extractor/packages.txt ] && \
    (echo 'Installing packages' && \
        apt-get update && \
        cat /home/extractor/packages.txt | xargs apt-get install -y --no-install-recommends && \
        rm /home/extractor/packages.txt && \
        apt-get autoremove -y && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*) || \
    (echo 'No packages to install' && \
        rm /home/extractor/packages.txt)

RUN [ -s /home/extractor/requirements.txt ] && \
    (echo "Install python modules" && \
    python -m pip install -U --no-cache-dir pip && \
    python -m pip install --no-cache-dir setuptools && \
    python -m pip install --no-cache-dir -r /home/extractor/requirements.txt && \
    rm /home/extractor/requirements.txt) || \
    (echo "No python modules to install" && \
    rm /home/extractor/requirements.txt)

# Install from source
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git && \
    git clone $terrautil_url --branch $terrautil_branch --single-branch "/home/extractor/terrautil" && \
    python3 -m pip install "/home/extractor/terrautil/" && \
    rm -rf /home/extractor/terrautil && \
    apt-get remove -y \
        git && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.cache/pip

USER extractor

COPY configuration.py transformer.py transformer_class.py /home/extractor/
