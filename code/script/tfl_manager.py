import pickle
from numpy.random import randint
from utils import Color
import matplotlib.pyplot as plt
from visualize_test import visualize
import find_tfl_lights
import cv2
from frame_container import FrameContainer


class TFLMan:

    def __init__(self, pkl_path):
        with open(pkl_path, 'rb') as pklfile:
            pkl_data = pickle.load(pklfile, encoding='latin1')

        self.__EMs = {k: v for k, v in pkl_data.items() if 'egomotion' in k}
        self.__pp = pkl_data['principle_point']
        self.__focal = pkl_data['flx']
        self.__prev_frame = None

    def on_frame(self, current_frame, frame_index):
        candidates, auxilary = self.__get_candidates(current_frame)
        traffic_lights, traffic_auxiliary = self.__get_tfl_coordinates(current_frame, candidates, auxilary)

        current_frame = FrameContainer(current_frame)
        if self.__prev_frame:
            distance = self.__get_dists(self.__prev_frame, current_frame, self.__prev_frame.traffic_light, traffic_lights)
            self.__prev_frame = current_frame

        else:
            distance = None
            self.__prev_frame = current_frame

        visualize(current_frame, candidates, auxilary, traffic_lights, traffic_auxiliary, distance)

        return traffic_lights, traffic_auxiliary, distance

    @staticmethod
    def __get_candidates(image):
        x_red, y_red, x_green, y_green = find_tfl_lights.find_tfl_lights(cv2.imread(image))

        candidates = [[x_red[index], y_red[index]] for index in range(len(x_red))] + [[x_green[index], y_green[index]] for index in range(len(x_green))]
        auxilary = [Color.red for i in x_red] + [Color.green for i in x_green]

        return candidates, auxilary

    @staticmethod
    def __get_tfl_coordinates(image, candidates, auxilary):
        traffic_lights_ind = randint(0, len(candidates), len(candidates)//2)
        traffic_lights = [candidates[index] for index in range(len(candidates)) if index in traffic_lights_ind]
        auxilary = [auxilary[index] for index in range(len(auxilary)) if index in traffic_lights_ind]

        return traffic_lights, auxilary

    def __get_dists(self, prev_frame, current_frame, prev_traffic_lights, current_traffic_lights):
        # current_frame.traffic_light = current_traffic_lights
        # current_frame.EM = self.__EMs[TFLMan.frame_number]

        dist = [10.0 for traffic_light in current_traffic_lights]
        print(dist)
        return dist
