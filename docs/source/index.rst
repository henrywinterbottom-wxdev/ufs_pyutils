###########
ufs_pyutils
###########

^^^^^^^^^^^
Description
^^^^^^^^^^^

An Python toolbox for UFS-based applications.

- **confs**: Configuration-type file (e.g., JSON, YAML, XML, etc.,) interfaces.
- **execute**: Application execution (e.g., containers, executables, scripts, etc.,) interfaces.
- **ioapps**: File format read and writing and file staging and archiving interfaces.
- **tools**: Generic-type tools for all application interfaces.
- **utils**: Utility interfaces.

^^^^^^^^^^
Developers
^^^^^^^^^^

* Henry R. Winterbottom - henry.winterbottom@noaa.gov
  
^^^^^^^
Cloning
^^^^^^^

The ``ufs_pyutils`` repository may be obtained as follows.

.. code-block:: bash

   user@host:$ /path/to/git clone --recursive https://www.github.com/HenryWinterbottom-NOAA/ufs_pyutils ./ufs_pyutils
   
^^^^^^^^^^^^^^^^^^^^^^
Container Environments
^^^^^^^^^^^^^^^^^^^^^^

A Docker container environments, supporting and within which the
``ufs_pyutils`` applications can be executed, may be obtained and
executed as follows.

.. code-block:: bash

   user@host:$ /path/to/docker ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest
   user@host:$ /path/to/docker container run -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest

To build and to excute within a Singularity version of the above
latest container image, do as follows.

.. code-block:: bash

   user@host:$ /path/to/singularity build /path/to/ufs_pyutils.sif docker://ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest
   user@host:$ /path/to/singularity shell /path/to/ufs_pyutils.sif

^^^^^^^^^^^^^
API Reference
^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   confs
   execute
   ioapps
   tools
   utils
