###############################
UFS Applications Python Toolbox
###############################

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

* Henry R. Winterbottom - henry.winterbottom.wxdev@gmail.com
  
^^^^^^^
Cloning
^^^^^^^

The ``ufs_pyutils`` repository may be obtained as follows.

.. code-block:: bash

   user@host:$ /path/to/git clone --recursive https://www.github.com/henrywinterbottom-wxdev/ufs_pyutils ./ufs_pyutils
   
^^^^^^^^^^^^^^^^^^^^^^
Container Environments
^^^^^^^^^^^^^^^^^^^^^^

A Docker container environment, supporting and within which the
``ufs_pyutils`` applications can be executed, may be obtained and
executed as follows.

.. code-block:: bash

   user@host:$ /path/to/docker ghcr.io/henrywinterbottom-wxdev/ubuntu20.04.ufs_pyutils:latest
   user@host:$ /path/to/docker container run -it ghcr.io/henrywinterbottom-wxdev/ubuntu20.04.ufs_pyutils:latest
   
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
