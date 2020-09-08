import pickle
from numpy.random import randint
from utils import Color
import matplotlib.pyplot as plt
from visualize_test import visualize


class TFLMan:
    frame_number = 0

    def __init__(self, pkl_path):
        with open(pkl_path, 'rb') as pklfile:
            pkl_data = pickle.load(pklfile, encoding='latin1')

        self.__EMs = {k: v for k, v in pkl_data.items() if 'egomotion' in k}
        self.__pp = pkl_data['principle_point']
        self.__focal = pkl_data['flx']
        self.__prev_frame = None

    def on_frame(self, current_frame):
        candidates, auxilary = self.__get_candidates(current_frame)
        traffic_lights, traffic_auxiliary = self.__get_tfl_coordinates(current_frame, candidates, auxilary)

        current_frame = FrameContainer(current_frame)
        if self.__prev_frame:
            distance = self.__get_dists(self.__prev_frame, current_frame, self.__prev_frame.traffic_light, traffic_lights)
            self.__prev_frame = current_frame

        else:
            distance = None
            self.__prev_frame = current_frame

        TFLMan.frame_number += 1
        visualize(current_frame, candidates, auxilary, traffic_lights, traffic_auxiliary, distance)

        return traffic_lights, traffic_auxiliary, distance

    @staticmethod
    def __get_candidates(image):
        # get_tfl_light
        x_red = randint(0, 1024, 4)
        y_red = randint(0, 1024, 4)
        x_green = randint(0, 1024, 4)
        y_green = randint(0, 1024, 4)

        candidates = [[x_red[index], y_red[index]] for index in range(len(x_red))] + [[x_green[index], y_green[index]] for index in range(len(x_green))]
        auxilary = [Color.red for i in x_red] + [Color.green for i in x_green]

        return candidates, auxilary

    @staticmethod
    def __get_tfl_coordinates(image, candidates, auxilary):
        pass

    def __get_dists(self, prev_frame, current_frame, prev_traffic_lights, current_traffic_lights):
        pass


class FrameContainer(object):
    def __init__(self, img_path):
        self.img = plt.imread(img_path)
        self.traffic_light = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []
