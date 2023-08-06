"""Package for PFx Brick"""

import os

# fmt: off
__project__ = 'pfxbrick'
__version__ = '0.7.0'
# fmt: on

VERSION = __project__ + "-" + __version__

script_dir = os.path.dirname(__file__)

from .pfxbrick import PFxBrick, find_bricks
from .pfxaction import PFxAction
from .pfxconfig import PFxConfig
from .pfxfiles import PFxFile, PFxDir
