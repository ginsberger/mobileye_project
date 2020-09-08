from tfl_manager import TFLMan


class Controler:
    def __init__(self, pls_path):
        self.__pkl = None
        self.__frame = []

        with open(pls_path) as f:
            for i, j in enumerate(f):
                if i == 0:
                    self.__pkl = j[:-1]
                else:
                    self.__frame.append(j[:-1])

        self.__tfl_manager = TFLMan(self.__pkl)

    def run(self):
        for frame in self.__frame:
            self.__tfl_manager.on_frame(frame)


control = Controler(r"C:\Users\Lenovo\Documents\mobileye_project\data\frames.pls")
control.run()
