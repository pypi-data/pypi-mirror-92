from . import observer
from darkai import observer_configs

class mean_squared_error_observer(observer):
    _backend = None

    def __init__(self):
        self.data = []
        self.loaded_config = False
        self.skip_n = 0
    
    def skip(self, n):
        self.skip_n = n

    def set_model(self, model):
        if "mean_squared_error_observer" not in observer_configs:
            raise Exception("Observer not supported, possibly broken config")
        obs_config = observer_configs["mean_squared_error_observer"]
        self._backend = model._backend
        if self._backend not in obs_config:
            raise Exception("Backend of model not supported by observer!")
        self.load_config(*obs_config[self._backend])
    
    def load_config(self, *arg):
        [
            fn_returns_size_of_arrays_1st_dim,
            fn_subtract_two_array_into_new_array,
            fn_inplace_square_array_elements,
            fn_sum_of_1d_array
        ] = arg
        self.size_1d = fn_returns_size_of_arrays_1st_dim
        self.cp_sub = fn_subtract_two_array_into_new_array
        self.sq_arr = fn_inplace_square_array_elements
        self.sum_1d = fn_sum_of_1d_array
        self.loaded_config = True
    
    def observe(self, model, it):
        if not self.loaded_config:
            raise Exception("Observer config not loaded!")
        if it == 0:
            self.data = []

        if self.skip_n > 0:
            self.skip_n -= 1
            return

        actual_output = model.training_expectation()
        predicted_output = model.training_prediction()
        batch_size = self.size_1d(actual_output)

        current_mse = self.sum_1d(self.sq_arr(self.cp_sub(actual_output, predicted_output))) / float(batch_size)

        self.data.append(current_mse)


