import platform
import pkg_resources

from cffi import FFI

LIB_NAME = None

if platform.system() == 'Linux' and platform.architecture()[0] == '64bit':
    LIB_NAME = 'libdenis.linux.x86_64.so'
elif platform.system() == 'Darwin':
    if platform.machine() == 'arm64':
        LIB_NAME = 'libdenis.darwin.arm64.dylib'
    elif platform.machine() == 'x86_64':
        LIB_NAME = 'libdenis.darwin.x86_64.dylib'

if LIB_NAME is None:
    raise Exception('Unsuported system')


ffi = FFI()
ffi.cdef("""
    double haversine(double, double, double, double);
""")

LIB_PATH = pkg_resources.resource_filename('denis', LIB_NAME)

lib = ffi.dlopen(LIB_PATH)

def haversine(lat_lng1, lat_lng2):
    return lib.haversine(
        lat_lng1[0],
        lat_lng1[1],
        lat_lng2[0],
        lat_lng2[1],
    )
