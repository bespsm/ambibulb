# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>

import os
from cffi import FFI

THIS_DIR = os.path.abspath(os.getcwd())
ROOT_DIR = "/opt/vc"
LIB_DIR = os.path.join(ROOT_DIR, "lib")
INC_DIR = os.path.join(ROOT_DIR, "include")

ffi = FFI()

f = open(os.path.join(THIS_DIR, "snapshot_bcm/snapshot_bcm.h"))
defs = f.read()
f.close()

ffi.cdef(defs)

f = open(os.path.join(THIS_DIR, "snapshot_bcm/snapshot_bcm.c"))
src = f.read()
f.close()

ffi.set_source(
    "ambibulb.snapshot_bcm",
    src,
    include_dirs=[
        THIS_DIR,
        INC_DIR,
        os.path.join(INC_DIR, "interface/vcos/pthreads"),
        os.path.join(INC_DIR, "interface/vmcs_host/linux"),
    ],
    library_dirs=[LIB_DIR],
    libraries=["bcm_host", "vcos", "vchiq_arm", "pthread", "rt"],
    define_macros=[
        ("HAVE_LIBBCM_HOST", None),
        ("USE_EXTERNAL_LIBBCM_HOST", None),
        ("USE_VCHIQ_ARM", None),
    ],
)

if __name__ == "__main__":
    ffi.compile(verbose=True)