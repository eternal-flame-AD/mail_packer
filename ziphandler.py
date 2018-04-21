import zipfile


class ZipHandler():

    def __init__(self, fn, mode="w"):
        self.fn = fn
        self.mode = mode
        if self.mode == "w":
            self.zip = zipfile.ZipFile(fn, mode='w')
        elif self.mode == "r":
            self.zip = zipfile.ZipFile(fn, mode="r")
        else:
            raise ValueError("Invalid ZipFile mode")

    def append_file(self, fn):
        self.zip.write(fn)

    def list_file(self):
        return self.zip.filelist

    def close(self):
        self.zip.close()
