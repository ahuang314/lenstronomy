class SIE_shear(object):

    def __init__(self,lens_model_list,kwargs_lens):

        assert lens_model_list[0] == 'SPEMD'
        assert lens_model_list[1] == 'SHEAR'
        self.Ntovary = 2
        self.k_start = 2
        self.tovary_indicies = [0,1]
        self.kwargs_lens = kwargs_lens

        self.to_vary_names = [['theta_E','center_x','center_y','e1','e2'], ['e1','e2']]

    def vary_model_fixed(self):

        return {'gamma': self.kwargs_lens[0]['gamma']}

    def get_param_ranges(self,reoptimize=False):

        if reoptimize:

            e1_e2 = 0.005
            e1_e2_shear = 0.005
            theta_E = 0.001
            center = 0.001

            low_e1 = self.kwargs_lens[0]['e1'] - e1_e2
            low_e2 = self.kwargs_lens[0]['e2'] - e1_e2
            hi_e1 = self.kwargs_lens[0]['e1'] + e1_e2
            hi_e2 = self.kwargs_lens[0]['e2'] + e1_e2

            low_shear_e1 = self.kwargs_lens[1]['e1'] - e1_e2_shear
            high_shear_e1 = self.kwargs_lens[1]['e1'] + e1_e2_shear
            low_shear_e2 = self.kwargs_lens[1]['e2'] - e1_e2_shear
            high_shear_e2 = self.kwargs_lens[1]['e2'] + e1_e2_shear

            low_Rein = self.kwargs_lens[0]['theta_E'] - theta_E
            hi_Rein = self.kwargs_lens[0]['theta_E'] + theta_E

            low_centerx = self.kwargs_lens[0]['center_x'] - center
            hi_centerx = self.kwargs_lens[0]['center_x'] + center
            low_centery = self.kwargs_lens[0]['center_y'] - center
            hi_centery = self.kwargs_lens[0]['center_y'] + center

        else:

            low_e1 = -0.1
            low_e2 = low_e1
            hi_e1 = 0.1
            hi_e2 = hi_e1

            low_shear_e1 = -0.05
            high_shear_e1 = 0.05
            low_shear_e2 = low_shear_e1
            high_shear_e2 = high_shear_e1

            low_Rein = 0.7
            hi_Rein = 1.4

            low_centerx = -0.01
            hi_centerx = 0.01
            low_centery = low_centerx
            hi_centery = hi_centerx

        sie_list_low = [low_Rein, low_centerx, low_centery, low_e1, low_e2]
        sie_list_high = [hi_Rein, hi_centerx, hi_centery, hi_e1, hi_e2]
        shear_list_low = [low_shear_e1, low_shear_e2]
        shear_list_high = [high_shear_e1, high_shear_e2]

        return sie_list_low+shear_list_low,sie_list_high+shear_list_high

class SPEP_shear(object):

    def __init__(self,lens_model_list,kwargs_lens):

        assert lens_model_list[0] == 'SPEP'
        assert lens_model_list[1] == 'SHEAR'
        self.Ntovary = 2
        self.k_start = 2
        self.tovary_indicies = [0, 1]
        self.kwargs_lens = kwargs_lens

        self.to_vary_names = [['theta_E', 'center_x', 'center_y', 'e1', 'e2'], ['e1', 'e2']]

    def vary_model_fixed(self):

        return {'gamma': self.kwargs_lens[0]['gamma']}

    def get_param_ranges(self,reoptimize=False):

        if reoptimize:

            e1_e2 = 0.005
            e1_e2_shear = 0.005
            theta_E = 0.001
            center = 0.001

            low_e1 = self.kwargs_lens[0]['e1'] - e1_e2
            low_e2 = self.kwargs_lens[0]['e2'] - e1_e2
            hi_e1 = self.kwargs_lens[0]['e1'] + e1_e2
            hi_e2 = self.kwargs_lens[0]['e2'] + e1_e2

            low_shear_e1 = self.kwargs_lens[1]['e1'] - e1_e2_shear
            high_shear_e1 = self.kwargs_lens[1]['e1'] + e1_e2_shear
            low_shear_e2 = self.kwargs_lens[1]['e2'] - e1_e2_shear
            high_shear_e2 = self.kwargs_lens[1]['e2'] + e1_e2_shear

            low_Rein = self.kwargs_lens[0]['theta_E'] - theta_E
            hi_Rein = self.kwargs_lens[0]['theta_E'] + theta_E

            low_centerx = self.kwargs_lens[0]['center_x'] - center
            hi_centerx = self.kwargs_lens[0]['center_x'] + center
            low_centery = self.kwargs_lens[0]['center_y'] - center
            hi_centery = self.kwargs_lens[0]['center_y'] + center

        else:

            low_e1 = -0.1
            low_e2 = low_e1
            hi_e1 = 0.1
            hi_e2 = hi_e1

            low_shear_e1 = -0.05
            high_shear_e1 = 0.05
            low_shear_e2 = low_shear_e1
            high_shear_e2 = high_shear_e1

            low_Rein = 0.7
            hi_Rein = 1.4

            low_centerx = -0.01
            hi_centerx = 0.01
            low_centery = low_centerx
            hi_centery = hi_centerx

        sie_list_low = [low_Rein, low_centerx, low_centery, low_e1, low_e2]
        sie_list_high = [hi_Rein, hi_centerx, hi_centery, hi_e1, hi_e2]
        shear_list_low = [low_shear_e1,low_shear_e2]
        shear_list_high = [high_shear_e1,high_shear_e2]

        return sie_list_low+shear_list_low,sie_list_high+shear_list_high




