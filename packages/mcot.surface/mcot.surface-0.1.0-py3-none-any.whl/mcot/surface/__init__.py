from . import grid
from ._write_gifti import write_gifti
from .cortex import Cortex, CorticalLayer, read_HCP
from .cortical_mesh import BrainStructure, CorticalMesh
from .mesh import Mesh2D

from mcot.utils.build import load_info
__doc__, __version__ = load_info(__name__) 
del load_info