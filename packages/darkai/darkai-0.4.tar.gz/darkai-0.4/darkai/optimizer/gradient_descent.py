from typing import Union, Type
from .optimizer import optimizer
from darkai import optimizer_configs
from darkai.supervised import supervised_model
from darkai.unsupervised import unsupervised_model
from .gradient_descent_implementations.gradient_descent_perceptron import gradient_descent_perceptron


gd_impls = {
    "perceptron": gradient_descent_perceptron
}

if "gradient_descent" not in optimizer_configs:
    optimizer_configs["gradient_descent"] = {}

gd = optimizer_configs["gradient_descent"]
for gd_impl in gd_impls:
    if gd_impl in gd:
        gd_impl_dt = gd[gd_impl]
        if "_optimizer_class" not in gd_impl_dt:
            gd_impl_dt["_optimizer_class"] = gd_impls[gd_impl]
    else:
        gd[gd_impl] = {
            "_optimizer_class": gd_impls[gd_impl]
        }


def gradient_descent(model: Union[Type[supervised_model], Type[unsupervised_model]]) -> Type[optimizer]:
    if "gradient_descent" not in optimizer_configs:
        raise Exception("Gradient Descent Not Supported!, Possibly broken config")
    opt_configs = optimizer_configs["gradient_descent"]
    model_backend = model._backend
    model_arch = model._model_architecture
    
    if model_arch not in opt_configs:
        raise Exception("Model Not Supported!")
    gd_arch = opt_configs[model_arch]
    gd = gd_arch["_optimizer_class"]
    if model_backend not in gd_arch:
        raise Exception("Backend Not Supported!")
    backend_config = gd_arch[model_backend]
    gd_ = gd(*backend_config)
    gd_._backend = model_backend
    return gd_
