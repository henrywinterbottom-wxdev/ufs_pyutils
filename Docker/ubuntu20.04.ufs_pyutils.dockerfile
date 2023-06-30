# =========================================================================

# Docker: Docker/ubuntu20.04.ufs_pyutils.dockerfile

# Email: henry.winterbottom@noaa.gov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the respective public license published by the
# Free Software Foundation and included with the repository within
# which this application is contained.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# =========================================================================

# Description
# -----------

#    This Docker recipe file builds a Docker image containing the
#    following packages.

#    - Ubuntu 20.04 base Linux image;

#    - Miniconda Python 3.9+ stack;

#    - `ufs_pyutils` package.

# Author(s)
# ---------

#    Henry R. Winterbottom; 17 January 2023 

# History
# -------

#    2023-01-17: Henry R. Winterbottom -- Initial implementation.

# ----

# -------------------------
# * * * W A R N I N G * * *
# -------------------------

# It is STRONGLY urged that users do not make modifications below this
# point.

# ----

FROM noaaufsrnr/ubuntu20.04.miniconda
ENV GIT_URL="https://www.github.com/HenryWinterbottom-NOAA/ufs_pyutils.git"
ENV GIT_BRANCH="feature/subprocess_logger"

LABEL "author"="Henry R. Winterbottom (henry.winterbottom@noaa.gov)"
LABEL "description"="Ubuntu 20.04 UFS Miniconda base image for the `ufs_pyutils` package."
LABEL "maintainer"="Henry R. Winterbottom"
LABEL "tag"="latest"
LABEL "version"="0.0.1"

RUN $(which git) clone ${GIT_URL} -b ${GIT_BRANCH} /ufs_pyutils && \
    $(which pip) install -r /ufs_pyutils/requirements.txt && \
    $(which conda) install -c conda-forge --file /ufs_pyutils/requirements.conda && \
    $(which conda) clean --tarballs

ENV PATH="/miniconda/bin:${PATH}"
ENV PYTHONPATH="/ufs_pyutils:${PYTHONPATH}"