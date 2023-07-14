# =========================================================================

# Module: fsutils/local_interface.py

# Author: Henry R. Winterbottom

# Email: henry.winterbottom@noaa.gov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the respective public license published by the
# Free Software Foundation and included with the repository within
# which this application is contained.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# =========================================================================

"""
Module
------

    local_interface.py

Description
-----------

    This module contains the base-class object for all local
    file-system tasks.

Classes
-------

    LocalFileSystem(fscopy=False, fsmove=False)

        This is the base-class module for local file system
        asynchronous interfacing.

Author(s)
---------

    Henry R. Winterbottom; 13 July 2023

History
-------

    2023-07-13: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import asyncio
from typing import Dict, Generic

import fsspec
from utils.logger_interface import Logger

# ----


class LocalFileSystem:
    """
    Description
    -----------

    This is the base-class module for local file system asynchronous
    interfacing.

    Keywords
    --------

    fscopy: bool, optional

        A Python boolean valued variable; if `True`, the specified
        files will be copied from a specified source path to a
        specified destination path.

    fsmove: bool, optional

        A Python boolean valued variable; if `True`, the specified
        files will be moved from a specified source path to a
        specified destination path.

    """

    def __init__(self: Generic, fscopy: bool = False, fsmove: bool = False):
        """
        Description
        -----------

        Creates a new LocalFileSystem object.

        """

        # Define the base-class attributes.
        self.logger = Logger(caller_name=f"{__name__}.{self.__class__.__name__}")
        self.fsys = fsspec.filesystem("file")
        (self.fscopy, self.fsmove) = [fscopy, fsmove]

    async def copy(self: Generic, srcfile: str, dstfile: str) -> None:
        """
        Description
        -----------

        Copies a specified source file path to the specified
        destination file path.

        Parameters
        ----------

        srcfile: str

            A Python string specifying the source file path.

        dstfile: str

            A Python string specifying the destination file path.

        """

        # Copy the respective source file path to the respective
        # destination file path.
        try:
            msg = f"Copying file {srcfile} to {dstfile}."
            self.logger.info(msg=msg)
            await self.fsys.copy(srcfile, dstfile)
        except TypeError:
            pass

    async def move(self: Generic, srcfile: str, dstfile: str) -> None:
        """
        Description
        -----------

        Moves a specified source file path to the specified
        destination file path.

        Parameters
        ----------

        srcfile: str

            A Python string specifying the source file path.

        dstfile: str

            A Python string specifying the destination file path.

        """

        # Move the respective source file path to the respective
        # destination file path.
        try:
            msg = f"Moving file {srcfile} to {dstfile}."
            self.logger.info(msg=msg)
            await self.fsys.move(srcfile, dstfile)
        except TypeError:
            pass

    async def run(self: Generic, filedict: Dict[str, str]) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Moves or copies, asynchronously, the specified source file
            paths to the respective destination file paths.

        """

        # Perform the file handling accordingly.
        if self.fscopy:
            tasks = [
                self.copy(srcfile=srcfile, dstfile=dstfile)
                for (srcfile, dstfile) in filedict.items()
            ]
        if self.fsmove:
            tasks = [
                self.move(srcfile=srcfile, dstfile=dstfile)
                for (srcfile, dstfile) in filedict.items()
            ]
        await asyncio.gather(*tasks)
