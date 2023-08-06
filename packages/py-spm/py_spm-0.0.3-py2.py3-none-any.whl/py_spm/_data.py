import numpy as np
from py_spm.utils import empty_to_none


class Data:
    def __init__(
        self, fname, dim, dtype, be, offset, pos, scl_slope, scl_inter, permission
    ):
        self.fname = fname
        self.shape = np.array(dim)
        self.dtype = dtype
        self.be = be
        self.offset = offset
        self.pos = np.array(pos)
        self.scl_slope = empty_to_none(scl_slope)
        self.scl_inter = empty_to_none(scl_inter)
        self.permission = permission

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"fname='{self.fname}', "
            f"dim={self.shape.tolist()}, "
            f"dtype={self.dtype}, "
            f"be={self.be}, "
            f"offset={self.offset}, "
            f"pos={self.pos.tolist()}, "
            f"scl_slope={self.scl_slope}, "
            f"scl_inter={self.scl_inter}, "
            f"permission='{self.permission}')"
        )
