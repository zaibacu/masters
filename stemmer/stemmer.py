from ctypes import *


class SN_env(Structure):
    _fields_ = (
        ("p", c_char_p),
        ("c", c_int),
        ("l", c_int),
        ("lb", c_int),
        ("bra", c_int),
        ("ket", c_int),
        ("S", POINTER(c_char_p)),
        ("I", POINTER(c_int)),
        ("B", c_char_p)
    )


class Stemmer(object):
    def __init__(self):
        self.lib = CDLL("stemmer/libltstemmer.so")
        self.env = self.create()

    def create(self):
        fn = self.lib.lt_create_env
        fn.restype = POINTER(SN_env)
        return fn()

    def close(self):
        import _ctypes
        fn = self.lib.lt_close_env
        fn.argtypes = [POINTER(SN_env)]
        fn(self.env)

        _ctypes.dlclose(self.lib._handle)

    def _set_current(self, text):
        fn = self.lib.SN_set_current
        fn.argtypes = [POINTER(SN_env), c_int, c_char_p]
        fn.restype = c_int
        fn(self.env, len(text), text)

    def stem(self, text):
        self._set_current(text.encode("UTF-8"))
        fn = self.lib.lt_stem
        fn.argtypes = [POINTER(SN_env)]
        fn.restype = c_int
        if fn(self.env) == 1:
            deref = self.env.contents
            data = deref.p[:deref.l]
            return data.decode("UTF-8")
        else:
            print("failed to stem")
            return text


if __name__ == "__main__":
    stemmer = Stemmer()
    print(stemmer.stem("balandžio"))
    stemmer.close()