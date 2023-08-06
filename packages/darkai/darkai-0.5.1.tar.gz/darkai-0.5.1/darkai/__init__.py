
# model_configs, example -
#   model_configs["perceptron"]["numpy"] = [
#        #*functions_list
#   ]
model_configs = {}

# optimizer_configs, example -
# optimizer_configs["gradient_descent"] = {
#       "perceptron" : {
#           "_optimizer_class": #optimizer_class
#           "numpy" : [
#                   #*functions_list
#              ]
#       }
#  }
optimizer_configs = {}

# observer_configs, example -
# observer_configs["accuracy_observer"] = {
#       "numpy": [
#              #*functions_list
#       ]
# }
observer_configs = {}


backends = {
    "numpy": "numpy",
    "pytorch": "pytorch",
    "arrayfire_cpu": "arrayfire_cpu",
    "arrayfire_opencl": "arrayfire_opencl",
    "arrayfire_cuda": "arrayfire_cuda"
}


def apply_model_config(md_configs):
    for model in md_configs:
        if model in model_configs:
            d_model_config = model_configs[model]
            md_config = md_configs[model]
            for backend in md_config:
                if backend not in d_model_config:
                    d_model_config[backend] = md_config[backend]
        else:
            model_configs[model] = md_configs[model]


def apply_optimizer_config(opt_configs):
    for opt in opt_configs:
        if opt in optimizer_configs:
            d_opt_config = optimizer_configs[opt]
            opt_config = opt_configs[opt]
            for arch in opt_config:
                if arch in d_opt_config:
                    d_arch_config = d_opt_config[arch]
                    arch_config = opt_config[arch]
                    for backend in arch_config:
                        if backend not in d_arch_config:
                            d_arch_config[backend] = arch_config[backend]
                else:
                    d_opt_config[arch] = opt_config[arch]
        else:
            optimizer_configs[opt] = opt_configs[opt]

def apply_observer_config(obs_configs):
    for obs in obs_configs:
        if obs in observer_configs:
            d_obs_config = observer_configs[obs]
            obs_config = obs_configs[obs]
            for backend in obs_config:
                if backend not in d_obs_config:
                    d_obs_config[backend] = obs_config[backend]
        else:
            observer_configs[obs] = obs_configs[obs]
