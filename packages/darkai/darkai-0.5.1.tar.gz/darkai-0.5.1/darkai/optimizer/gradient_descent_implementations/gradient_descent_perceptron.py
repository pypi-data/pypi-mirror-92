from darkai import backends
from ..optimizer import optimizer

class gradient_descent_perceptron(optimizer):
    # specifies name of optimizer
    _optimizer_name = "gradient_descent"
    # specifies which model architecture it can train
    _optimizer_architecture = "perceptron"
    # this gives the hint of current backend(math library) being used
    _backend = None

    def __init__(self, *arg):
        [
            fn_returns_size_of_arrays_1st_dim,
            fn_sum_of_1d_array,
            fn_summations_of_all_sub_arrays_into_new_array,
            fn_subtract_two_array_into_new_array,
            fn_copy_and_transpose_array,
            fn_inplace_multiply_1st_array_with_2nd_array,
            fn_inplace_multiply_1st_array_with_float,
            fn_inplace_subtract_1st_array_with_2nd_array
        ] = arg
        self.size_of_1st_dim = fn_returns_size_of_arrays_1st_dim
        self.sum_1d = fn_sum_of_1d_array
        self.sum_2d = fn_summations_of_all_sub_arrays_into_new_array
        self.cp_transpose = fn_copy_and_transpose_array
        self.inplace_mult = fn_inplace_multiply_1st_array_with_2nd_array
        self.cp_sub = fn_subtract_two_array_into_new_array
        self.learning_rate = 0.01
        self.mult_n = fn_inplace_multiply_1st_array_with_float
        self.inplace_sub = fn_inplace_subtract_1st_array_with_2nd_array

    def set_learning_rate(self, lr:float):
        self.learning_rate = lr

    def optimize(self, model, w, b):
        expected_output = model.training_expectation()
        input_data = model.training_inputs()
        batch_size = self.size_of_1st_dim(expected_output)

        y_predicted = model.training_prediction()

        Db = (2.0 / batch_size) * self.sum_1d(self.cp_sub(y_predicted, expected_output))
        b -= self.learning_rate * Db

        input_data_T = self.cp_transpose(input_data)
        mult = self.inplace_mult(input_data_T, self.cp_sub(y_predicted, expected_output))
        Dw = self.mult_n( self.sum_2d(mult), (2.0 / batch_size) * self.learning_rate )
        w = self.inplace_sub(w, Dw)

        return w, b
