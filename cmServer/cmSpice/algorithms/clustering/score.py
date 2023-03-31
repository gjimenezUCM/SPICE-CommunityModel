from sklearn.metrics import davies_bouldin_score

def make_generator(parameters):
    # https://stackoverflow.com/a/55151423
    if not parameters:
        yield dict()
    else:
        key_to_iterate = list(parameters.keys())[0]
        next_round_parameters = {p : parameters[p]
                    for p in parameters if p != key_to_iterate}
        for val in parameters[key_to_iterate]:
            for pars in make_generator(next_round_parameters):
                temp_res = pars
                temp_res[key_to_iterate] = val
                yield temp_res



# def tuning(model, data, fixed_params, param_grid):
#     # add fix parameters - here - it's just a random one
#     # fixed_params = {"max_iter":300 } 
#     # param_grid = {"n_clusters": range(2, 11)}

#     score = 9223372036854775807
#     bestParams = {}
#     for params in make_generator(param_grid):
#         params.update(fixed_params)
#         ca = model( **params )
#         ca.fit(data)
#         labels = ca.labels_
#         nScore = davies_bouldin_score(data, labels)
#         if nScore < score:
#             score = nScore
#             bestParams = params
#     return bestParams, score
