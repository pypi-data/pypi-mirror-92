from PIL.Image import Image


class ConvertMode:
    mode: str

    def __init__(self, mode: str):
        self.mode = mode

    def __call__(self, x: Image) -> Image:
        return x.convert(self.mode)
