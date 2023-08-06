# DarkAI

Example code -

```
import darkai
from darkai import backends

from darkai.observer import accuracy_observer, mean_squared_error_observer
from darkai.optimizer import gradient_descent
from darkai.supervised import perceptron
from darkai.plugins import numpy_support

import numpy as np

# Enable Numpt support before using numpy as backend
numpy_support.enable(darkai)

# Training data
training_data = np.array([[0, 1], [1, 0], [0, 0], [1, 1]], np.float32)

# Expected Output
expected_output = np.array([0, 0, 0, 1], np.float32)

# create a perceptron with backend "numpy" (this library will be used for math)
p = perceptron(backends["numpy"])

# activation function can be changed
# eg - p.set_activation_fn("sigmoid")
p.set_activation_fn(lambda a: a)

# use gradient descent as optimizer
p.set_optimizer(gradient_descent)

# we will observe the accuracy and MSE
accuracy = accuracy_observer()
accuracy.set_threshold(0.5)
mse = mean_squared_error_observer()

# add the observers to the model
p.add_observer(accuracy)
p.add_observer(mse)

# set learning rate
p.optimizer.set_learning_rate(0.1)

# train with 100 iterations
p.train_iters(10000, training_data, expected_output)


# print training accuracy
print("Accuracy: ")
print(accuracy.data)
print()


# print training MSE
print("MSE: ")
print(mse.data)
print()


# predict
out = p.predict(training_data)
print("Predicted: ", out)
```