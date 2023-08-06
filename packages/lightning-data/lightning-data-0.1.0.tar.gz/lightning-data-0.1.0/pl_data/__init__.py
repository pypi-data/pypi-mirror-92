"""Root package info."""

import os

__version__ = '0.1.0'
__author__ = 'PyTorchLightning et al.'
__author_email__ = 'name@pytorchlightning.ai'
__license__ = 'TBD'
__copyright__ = f'Copyright (c) 2020-2021, {__author__}.'
__homepage__ = 'https://github.com/PyTorchLightning/lightning-data'
__docs__ = "PyTorch Lightning Sample project."
__long_doc__ = """
What is it?
-----------
PL dats oriented package mainly focusing on datasets and datamodules...
"""

_PACKAGE_ROOT = os.path.dirname(__file__)
_PROJECT_ROOT = os.path.dirname(_PACKAGE_ROOT)
