from sklearn import impute, linear_model, preprocessing
_allowed_steps = {
    'SimpleImputer': impute.SimpleImputer,
    'LinearRegression': linear_model.LinearRegression,
    'StandardScaler': preprocessing.StandardScaler
}


def get_step_class(name):
    try:
        return _allowed_steps[name]
    except KeyError:
        raise Exception(f'Step names {name} is not allowed!\nThe following steps are allowed: {get_allowed_steps()}')


def get_allowed_steps():
    return _allowed_steps.keys()
