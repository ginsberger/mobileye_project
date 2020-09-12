import pickle
from numpy.random import randint
from utils import Color
import matplotlib.pyplot as plt
from visualize_test import visualize
import find_tfl_lights
import cv2
from frame_container import FrameContainer
from create_sample import crop_image
from tensorflow.keras.models import load_model


class TFLMan:

    def __init__(self, pkl_path):
        with open(pkl_path, 'rb') as pklfile:
            pkl_data = pickle.load(pklfile, encoding='latin1')

        self.__EMs = {k: v for k, v in pkl_data.items() if 'egomotion' in k}
        self.__pp = pkl_data['principle_point']
        self.__focal = pkl_data['flx']
        self.__prev_frame = None
        self.__model = load_model("../../data/model.h5")

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

    def __get_tfl_coordinates(self, image, candidates, auxliary):

        crop_shape = (81, 81)
        l_predicted_label = []

        for candidate in candidates:
            crop_img = crop_image(cv2.imread(image), candidate[0], candidate[1])
            predictions = self.__model.predict(crop_img.reshape([-1]+list(crop_shape) +[3]))
            l_predicted_label.append(1 if predictions[0][1] > 0.98 else 0)

        traffic_lights = [candidates[index] for index in range(len(candidates)) if l_predicted_label[index] == 1]
        auxliary =  [auxliary[index] for index in range(len(auxliary)) if l_predicted_label[index] == 1]

        return traffic_lights, auxliary

    def __get_dists(self, prev_frame, current_frame, prev_traffic_lights, current_traffic_lights):
        # current_frame.traffic_light = current_traffic_lights
        # current_frame.EM = self.__EMs[TFLMan.frame_number]

        dist = [10.0 for traffic_light in current_traffic_lights]
        print(dist)
        return dist
