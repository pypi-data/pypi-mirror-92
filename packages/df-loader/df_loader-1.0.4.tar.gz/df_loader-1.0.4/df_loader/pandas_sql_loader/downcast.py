import numpy as np
from numpy import float32, float64, floating
from numpy import iinfo, finfo
from numpy import int8, int16, int32, int64
from numpy import object
from numpy import uint8, uint16, uint32, uint64, unsignedinteger


def get_dtype_rank(dtype):
    # Work with no more than two-digit ranks, else None
    dtype_name = str(np.dtype(dtype))

    num = None
    if dtype_name[-2].isdigit():
        num = int(dtype_name[-2:])
    elif dtype_name[-1].isdigit():
        num = int(dtype_name[-1])
    return num


def set_ranks(dtypes):
    ranks = {}
    for dtype in dtypes:
        rank = get_dtype_rank(dtype)
        if rank is None:
            raise ValueError(f'set_ranks: dtype {dtype} dont have no more than two-digit rank,'
                             f'why did you insert it into this func???')
        ranks[rank] = dtype
    return ranks


float_ranks = set_ranks([float32, float64])
int_ranks = set_ranks([int8, int16, int32, int64])
uint_ranks = set_ranks([uint8, uint16, uint32, uint64])


def downcast(arr, init_type):
    # Object is the uppermost cast, cannot downcast to this
    # And if the dtype of the arr is object that cannot downcast

    if init_type == object:
        arr = arr.astype(object)

    if arr.dtype == object:
        return arr

    init_type = np.dtype(init_type).type

    min_v = np.nanmin(arr)
    max_v = np.nanmax(arr)
    if issubclass(init_type, floating) or issubclass(arr.dtype.type, floating):
        float_rank = max(get_dtype_rank(init_type), 32)  # because np.float16 is half precision float
        init_type = try_downcast_minmax(min_v, max_v, float_rank, float_ranks, float64, finfo)
    else:
        type_rank = get_dtype_rank(init_type)
        if issubclass(init_type, unsignedinteger):
            if min_v >= 0:
                init_type = try_downcast_minmax(min_v, max_v, type_rank, uint_ranks, uint64, iinfo)
                return arr.astype(init_type)
        init_type = try_downcast_minmax(min_v, max_v, type_rank, int_ranks, int64, iinfo)
    return arr.astype(init_type)


def try_downcast_minmax(min_val, max_val, type_rank, ranks, max_rank, tinfo):
    init_type = ranks.get(type_rank, max_rank)
    while type_rank < 64:
        f_type_size = (tinfo(init_type).min, tinfo(init_type).max)
        if min_val >= f_type_size[0] and max_val <= f_type_size[1]:
            break
        else:
            type_rank = type_rank * 2
            init_type = ranks.get(type_rank, max_rank)
    return init_type
