# File: Docker/ubuntu20.04.ufs_pyutils.dockerfile
# Author: Henry R. Winterbottom
# Date: 29 August 2023
# Version: 0.0.1
# License: LGPL v2.1

# This Docker recipe file builds a Docker image containing the
# following packages:

# - `ufs_pyutils` package.

# -------------------------
# * * * W A R N I N G * * *
# -------------------------

# It is STRONGLY urged that users do not make modifications below this
# point; changes below are not supported.

# ----

FROM ghcr.io/henrywinterbottom-wxdev/ubuntu20.04.miniconda:latest
ENV GIT_URL="https://www.github.com/henrywinterbottom-wxdev/ufs_pyutils.git"
ENV GIT_BRANCH="develop"

LABEL "author"="Henry R. Winterbottom (henry.winterbottom.wxdev@gmail.com"
LABEL "description"="Ubuntu 20.04 UFS Miniconda base image for the `ufs_pyutils` package."
LABEL "maintainer"="Henry R. Winterbottom"
LABEL "tag"="latest"
LABEL "version"="0.0.1"

RUN $(which git) clone ${GIT_URL} -b ${GIT_BRANCH} /opt/ufs_pyutils && \
    $(which pip) install -r /opt/ufs_pyutils/requirements.txt && \
    $(which conda) install -c conda-forge --file /opt/ufs_pyutils/requirements.conda && \
    $(which conda) clean --tarballs

ENV PATH="/opt/miniconda/bin:${PATH}"
ENV PYTHONPATH="/opt/ufs_pyutils:${PYTHONPATH}"
