import warnings as _warnings
from time import time as _time

import numpy as _np

from triangler.color import ColorMethod
from triangler.edges import EdgeMethod
from triangler.mod import Triangler
from triangler.sampling import SampleMethod

_np.random.seed(int(_time()))
_warnings.filterwarnings("ignore")
