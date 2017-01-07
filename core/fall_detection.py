import numpy as np
import statistics

class FallDetector():
    def calculate_values(self, mean_vec, delta_pca, vector_angles):
        self.__update_values(mean_vec, delta_pca, vector_angles)
        self.__calculate_mean_values()
        # print("dmean_vec: %s delta_pca: %s pcas: %s" % (self.mean_direction_diff_vec, self.mean_delta_pca, self.mean_anlge_pcas))
        return self.mean_direction_diff_vec, self.mean_delta_pca, self.mean_anlge_pcas
    
    def is_fall(self):
        is_falling, is_fall = False, False
        dcenter_x, dcenter_y = self.mean_direction_diff_vec[0], self.mean_direction_diff_vec[1]
        
        # check if centrum is making fall movement
        if dcenter_y > 50 and (dcenter_x > 50 or dcenter_x < -50):
            # check if pca_angles are moving
            is_falling = True

        return is_falling, is_fall

    '''' CORE PRIVATE HELPERS '''
    def __calculate_mean_values(self):
        # python mean difference of list items
        def calculate_differences(seq):
            return [j-i for i,j in zip(seq[:-1], seq[1:])]
        
        def calculate_mean_vec(self):
            v1, v2 = calculate_differences(self._mean_vecs[0]), calculate_differences(self._mean_vecs[1])
            self.mean_direction_diff_vec = [sum(v1), sum(v2)]

        def calculate_delta_pca(self):
            self.mean_delta_pca = statistics.median(self._delta_pcas)

        def calculate_pca(self):
            v1, v2 = calculate_differences(self._angle_pcas[0]), calculate_differences(self._angle_pcas[1])
            self.mean_anlge_pcas = [sum(v1), sum(v2)]

        calculate_mean_vec(self)
        calculate_delta_pca(self)
        calculate_pca(self)

    def __update_values(self, mean_vec, delta_pca, vector_angles):
        # append
        self.__push_propval(self._mean_vecs, mean_vec[0], True) # mean_vec is arr in arr
        self.__push_propval(self._delta_pcas, delta_pca)
        self.__push_propval(self._angle_pcas, vector_angles, True)

        # pop if neceserry
        self.__pop_propval(self._mean_vecs, True)
        self.__pop_propval(self._delta_pcas)
        self.__pop_propval(self._angle_pcas, True)


    '''' EXTRA PRIVATE HELPERS '''
    def __pop_propval(self, prop, is_pair=False):
        if not is_pair:
            if len(prop) > self.var_length:
                prop.pop(0)
        else:
            if len(prop[0]) > self.var_length:
                prop[0].pop(0)
                prop[1].pop(0)

    def __push_propval(self, prop, val, is_pair=False):
        if not is_pair:
            prop.append(val)
        else:
            prop[0].append(val[0])
            prop[1].append(val[1])

    def __init__(self):
        self._mean_vecs = []
        self._mean_vecs.append([]), self._mean_vecs.append([])        

        self._delta_pcas = []

        self._angle_pcas = []
        self._angle_pcas.append([]), self._angle_pcas.append([])

        self.var_length = 30


fall_detection = FallDetector()
