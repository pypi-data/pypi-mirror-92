# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""A context manager to set a temporary working directory."""
from typing import Union
from pathlib import Path
from contextlib import contextmanager
import os

@contextmanager
def temporary_working_directory(directory: Union[str, Path]) -> Path:
    """Temporarily set the working directory.

    :param directory: The directory to set as the temporary working directory.
    :return: The temporary working directory.
    """
    old_working_directory = os.getcwd()
    os.chdir(directory)
    try:
        yield Path(directory)
    finally:
        os.chdir(old_working_directory)
