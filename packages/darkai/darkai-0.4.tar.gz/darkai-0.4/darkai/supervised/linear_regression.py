import json

class linear_regression:

    # the constructor accepts
    # one of the several backends
    def __init__(self, backend):
        self.backend = backend
        self.state = {
            "trainings": 0
        }
    
    def train(self, x, y, inplace=False):
        M = self.backend
        if x is None or y is None:
            raise ValueError("Invalid data types provided, expected " + str(backend.array_type))
        size_x, size_y = backend.len(x), backend.len(y)
        if size_x != size_y:
            raise ValueError("Invalid parameters, x and y should be of same size")

        if(self.state["trainings"] > 0) :
            return self.continue_training(x, y, inplace)
        
        state = self.state

        sum_x, sum_y = backend.sum(x), backend.sum(y)
        mean_x, mean_y = sum_x / size_x, sum_y / size_y

        # x1 = x - mean_x
        x1 = backend.subtract(x, mean_x, inplace)
        # y1 = y - mean_y
        y1 = backend.subtract(y, mean_y, inplace)

        # x2 = x1 ^ 2
        x2 = backend.square(x1, True)

        # z = x1 * y1
        # z refers to x1 from now, since, we don't need x1 anymore
        z = backend.multiply(x1, y1, True, modify_right=True)

        m = backend.sum(z) / backend.sum(x2)
        c = mean_y - (m * mean_x)

        state["m"], state["c"] = m, c
        state["trainings"] += 1

    def predict(self, x):
        state = self.state
        return state["m"] * x + state["c"]


    def test(self, x):
        pass

    def save_state_to_file(self, filepath):
        with open(filepath, "wb") as f:
            json.dump(self.state, f)
    
    def resume_state_from_file(self, filepath=None):
        with open(filepath, "rb") as f:
            self.state = json.load(f)
    
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state