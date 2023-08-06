import math
from typing import Type, Callable, Any, Union
from darkai import model_configs, backends
from darkai.supervised import supervised_model
from darkai.optimizer import optimizer
from darkai.observer import observer

if "perceptron" not in model_configs:
    model_configs["perceptron"] = {}


def perceptron(backend:str, *args, **kwargs) -> Type[supervised_model]:
    arch = "perceptron"
    model_arch = model_configs[arch]
    if backend in model_arch:
        model_config = model_arch[backend]
        model_ = perceptron_(*model_config)
        model_._backend = backend
        return model_
    else:
        raise Exception("Unsupported backend !")


class perceptron_(supervised_model):
    _model_name = "perceptron"
    _model_architecture = "perceptron"
    _backend = None

    def __init__(self, *arg):
        [
            fn_returns_array_with_ones_of_given_1d_shape,
            fn_returns_dot_product_of_two_1d_arrays,
            fn_returns_size_of_arrays_1st_dim,
            fn_returns_size_of_arrays_2nd_dim,
            fn_returns_dimension_count,
            fn_returns_dot_product_2d_array_with_1d_array,
            fn_apply_given_func_to_all_elements_of_given_1d_array
        ] = arg

        self.ones_1d = fn_returns_array_with_ones_of_given_1d_shape
        self.dot_1d_1d = fn_returns_dot_product_of_two_1d_arrays
        self.dot_2d_1d = fn_returns_dot_product_2d_array_with_1d_array
        self.size_of_1st_dim = fn_returns_size_of_arrays_1st_dim
        self.size_of_2nd_dim = fn_returns_size_of_arrays_2nd_dim
        self.dim_count = fn_returns_dimension_count
        self.map_1d = fn_apply_given_func_to_all_elements_of_given_1d_array
        self.activation_fn = None
        self.state = {
            "w": None,
            "b": None
        }
        self.optimizer = None
        self.common_activation_fns = {
            "sigmoid": lambda y: 1.0 / (1.0 + math.exp(-y)),
            "binary": lambda y: 0 if y<=0 else 1
        }
        self.observers = []
        self.tr_cache_predicted = None
        self.tr_cache_expected = None
        self.tr_cache_inputs = None


    def set_activation_fn(self, fn:Union[Callable, str]):
        if type(fn) is str:
            if fn in self.common_activation_fns:
                self.activation_fn = self.common_activation_fns[fn]
            else:
                raise Exception("Invalid Activation Function !")
        else:
            self.activation_fn = fn


    def add_observer(self, observer):
        observer.set_model(self)
        self.observers.append(observer)


    def predict(self, input_data):
        dim_count = self.dim_count(input_data)
        if dim_count == 2:
            return self.batch_predict(input_data)
        if dim_count != 1:
            raise Exception("Invalid dimensions for input_data !")
        size = self.size_of_1st_dim(input_data)
        self.prepare(size)
        out = self.dot_1d_1d(input_data, self.state["w"]) + self.state["b"]
        if self.activation_fn is None:
            return out
        return self.activation_fn(out)


    def batch_predict(self, input_data):
        dim_count = self.dim_count(input_data)
        if dim_count == 1:
            return self.predict(input_data)
        if dim_count != 2:
            raise Exception("Invalid dimensions for input_data !")
        size_2d = self.size_of_2nd_dim(input_data)
        self.prepare(size_2d)
        out = self.dot_2d_1d(input_data, self.state["w"]) + self.state["b"]
        if self.activation_fn is None:
            return out
        return self.map_1d(self.activation_fn , out)


    def prepare(self, new_size):
        w, b = self.state["w"], self.state["b"]
        if w is None or self.dim_count(w) != 1 or self.size_of_1st_dim(w) != new_size:
            self.state["w"] = self.ones_1d(new_size)
        if b is None or type(b) is not float:
            self.state["b"] = 1.0


    def set_optimizer(self, opt:Callable):
        self.optimizer = opt(self)


    def train(self, input_data, expected_output):
        dim_count = self.dim_count(input_data)
        if dim_count == 2:
            return self.batch_train(input_data, expected_output)
        if dim_count != 1 or True:
            raise Exception("Invalid dimensions for input_data !")
        # NYI - For simplicity
        # can only be trained in batches
        size = self.size_of_1st_dim(input_data)
        if type(expected_output) is int:
            expected_output = float(expected_output)
        if type(expected_output) is not float:
            raise Exception("Invalid type for expected_output !")
        self.prepare(size)


    def training_prediction(self):
        return self.tr_cache_predicted


    def training_expectation(self):
        return self.tr_cache_expected


    def training_inputs(self):
        return self.tr_cache_inputs


    def handle_observers(self, it):
        for observer in self.observers:
            observer.observe(self, it)


    def batch_train(self, input_data, expected_output):
        # training with 1 iteration
        return self.train_iters(1, input_data, expected_output)


    def train_iters(self, iters, input_data, expected_output, cb=None):
        if iters <= 0:
            return

        dim_count = self.dim_count(input_data)
        if dim_count == 1:
            return self.train(input_data, expected_output)
        if dim_count != 2:
            raise Exception("Invalid dimensions for input_data !")
        size_1d, size_2d = self.size_of_1st_dim(input_data), self.size_of_2nd_dim(input_data)
        if self.dim_count(expected_output) != 1 or self.size_of_1st_dim(expected_output) != size_1d:
            raise Exception("Invalid dimensions for expected_output !")
        self.prepare(size_2d)

        if self.optimizer is None:
            raise Exception("Optimizer not specified !")
        
        # Before training
        self.tr_cache_predicted = self.batch_predict(input_data)
        self.tr_cache_expected = expected_output
        self.tr_cache_inputs = input_data
        self.handle_observers(0)
        if cb is not None:
            cb(self, 0)

        for i in range(iters):
            self.state["w"], self.state["b"] = self.optimizer.optimize(self, self.state["w"], self.state["b"])
            self.tr_cache_predicted = self.batch_predict(input_data)
            self.handle_observers(i+1)
            if cb is not None:
                cb(self, i)



