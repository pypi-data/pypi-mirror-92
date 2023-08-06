import numpy as np

def enable(d):
    md_configs = {
        "perceptron": {
            "numpy": [
                np.ones,
                lambda a, b: float(np.dot(a, b)),
                lambda a: a.shape[0],
                lambda a: a.shape[1],
                lambda a: len(a.shape),
                np.dot,
                lambda fn, arr: np.vectorize(lambda n: fn(float(n)))(arr)
            ]
        }
    }

    def np_inplace_mult(a, b):
        a *= b
        return a
    
    def np_inplace_subt(a, b):
        a -= b
        return a

    opt_configs = {
        "gradient_descent": {
            "perceptron": {
                "numpy": [
                    lambda a: a.shape[0],
                    lambda a: float(np.sum(a)),
                    lambda a: np.sum(a, axis=1),
                    lambda a,b: a - b,
                    lambda a: np.transpose(a).copy(),
                    np_inplace_mult,
                    np_inplace_mult,
                    np_inplace_subt,
                ]
            }
        }
    }

    obs_configs = {
        "accuracy_observer": {
            "numpy": [
                lambda a: a.shape[0],
                lambda a, i: float(a[i])
            ]
        },
        "mean_squared_error_observer": {
            "numpy": [
                lambda a: a.shape[0],
                lambda a, b: a - b,
                lambda a: np.square(a, a),
                lambda a: float(np.sum(a))
            ]
        }
    }

    
    
    d.apply_model_config(md_configs)
    d.apply_optimizer_config(opt_configs)
    d.apply_observer_config(obs_configs)
