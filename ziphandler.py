import zipfile


class ZipHandler():

    def __init__(self, fn, mode="w"):
        self.fn = fn
        self.mode = mode
        if self.mode == "w":
            self.zip = zipfile.ZipFile(fn, mode='w',
                                       compression=zipfile.ZIP_DEFLATED)
        elif self.mode == "r":
            self.zip = zipfile.ZipFile(fn, mode="r")
        else:
            raise ValueError("Invalid ZipFile mode")

    def append_file(self, fn):
        self.zip.write(fn, arcname=fn[fn.rindex("/")+1:],
                       compress_type=zipfile.ZIP_DEFLATED)

    def list_file(self):
        return self.zip.infolist()

    def close(self):
        self.zip.close()
