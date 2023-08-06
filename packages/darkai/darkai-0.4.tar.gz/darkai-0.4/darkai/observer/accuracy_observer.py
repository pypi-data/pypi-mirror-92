from . import observer
from darkai import observer_configs

class accuracy_observer(observer):
    _backend = None

    def __init__(self):
        self.data = []
        self.loaded_config = False
        self.threshold = 0
        self.skip_n = 0
    
    def set_threshold(self, n):
        self.threshold = n
    
    def skip(self, n):
        self.skip_n = n

    def set_model(self, model):
        if "accuracy_observer" not in observer_configs:
            raise Exception("Observer not supported, possibly broken config")
        obs_config = observer_configs["accuracy_observer"]
        self._backend = model._backend
        if self._backend not in obs_config:
            raise Exception("Backend of model not supported by observer!")
        self.load_config(*obs_config[self._backend])
    
    def load_config(self, *arg):
        [
            fn_returns_size_of_arrays_1st_dim,
            fn_returns_element_of_given_array_at_given_location
        ] = arg
        self.size_1d = fn_returns_size_of_arrays_1st_dim
        self.loc = fn_returns_element_of_given_array_at_given_location
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

        correct = 0
        for i in range(batch_size):
            actual = self.loc(actual_output, i)
            predicted = self.loc(predicted_output, i)
            diff = abs(actual - predicted)
            if diff <= self.threshold:
                correct += 1

        current_accuracy = float(correct) / float(batch_size)

        self.data.append(current_accuracy)


