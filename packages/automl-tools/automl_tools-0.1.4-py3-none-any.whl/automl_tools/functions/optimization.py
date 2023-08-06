import numpy as np
from hyperopt import STATUS_OK, hp, Trials, fmin, tpe, space_eval
from hyperopt.pyll import scope
from sklearn.model_selection import cross_val_score

from automl_tools.functions.selection import search_model
from automl_tools.functions.utils import target_count_class


def search_space(model):
    space = dict()
    if model == 'LR':
        space = dict(warm_start=hp.choice('warm_start', [True, False]),
                     fit_intercept=hp.choice('fit_intercept', [True, False]),
                     tol=hp.uniform('tol', 0.00001, 0.0001),
                     C=hp.uniform('C', 0.05, 3),
                     max_iter=hp.choice('max_iter', range(100, 1000))
                     )

    elif model == 'RF':
        space = dict(criterion='gini',
                     max_depth=6,
                     max_features=hp.choice('max_features', ['auto', 'sqrt', 'log2', None]),
                     min_samples_leaf=hp.uniform('min_samples_leaf', 0, 0.5),
                     min_samples_split=hp.uniform('min_samples_split', 0, 1),
                     n_estimators=100,
                     )

    elif model == 'SVM':
        space = dict(C=hp.uniform('C', 0.1, 2.0),
                     kernel=hp.choice('kernel', ['linear', 'poly', 'rbf', 'sigmoid']),
                     degree=scope.int(hp.quniform('degree', 2, 5, 1)),
                     gamma=hp.choice('gamma', ['auto', 'scale']),
                     probability=hp.choice('probability', [True]),
                     tol=hp.loguniform('tol', np.log(1e-5), np.log(1e-2))
                     )

    elif model == 'LS':
        space = dict(alpha=hp.uniform('alpha', 1, 10),
                     max_iter=hp.choice('max_iter', range(100, 1000)),
                     loss=hp.choice('loss', ['log', 'modified_huber', 'squared_loss',
                                             'huber', 'epsilon_insensitive']),
                     penalty=hp.choice('penalty', ['l1']),
                     learning_rate=hp.choice('learning_rate', ['optimal'])
                     )
    elif model == 'RD':
        space = dict(alpha=hp.uniform('alpha', 1, 10),
                     max_iter=hp.choice('max_iter', range(100, 1000)),
                     loss=hp.choice('loss', ['log', 'modified_huber', 'squared_loss',
                                             'huber', 'epsilon_insensitive']),
                     penalty=hp.choice('penalty', ['l2']),
                     learning_rate=hp.choice('learning_rate', ['optimal'])
                     )
    elif model == 'NET':
        space = dict(alpha=hp.uniform('alpha', 1, 10),
                     max_iter=hp.choice('max_iter', range(100, 1000)),
                     loss=hp.choice('loss', ['log', 'modified_huber', 'squared_loss',
                                             'huber', 'epsilon_insensitive']),
                     penalty=hp.choice('penalty', ['elasticnet']),
                     learning_rate=hp.choice('learning_rate', ['optimal'])
                     )

    elif model == "DT":
        space = dict(criterion=hp.choice('criterion', ['gini', 'entropy']),
                     splitter=hp.choice('splitter', ['best', 'random']),
                     max_depth=scope.int(hp.quniform('max_depth', 3, 10, 1)),
                     min_samples_split=scope.int(hp.quniform('min_samples_split', 2, 50, 1)),
                     min_samples_leaf=scope.int(hp.quniform('min_samples_leaf', 1, 50, 1)),
                     max_features=hp.choice('max_features', ['auto', 'log2', None])
                     )

    elif model == 'ET':
        space = dict(criterion=hp.choice('criterion', ['entropy', 'gini']),
                     max_depth=hp.choice('max_depth', np.arange(3, 12, dtype=int)),
                     max_features=hp.choice('max_features', ['auto', 'sqrt', 'log2', None]),
                     min_samples_leaf=hp.uniform('min_samples_leaf', 0, 0.5),
                     min_samples_split=hp.uniform('min_samples_split', 0, 1),
                     n_estimators=hp.choice('n_estimators', [10, 50]))

    elif model == 'GB':
        space = dict(learning_rate=hp.lognormal('learning_rate', 0.05, 0.3),
                     max_depth=hp.quniform('max_depth', 10, 12, 10),
                     max_features=hp.choice('max_features', ['auto', 'sqrt', 'log2', None]),
                     min_samples_leaf=hp.uniform('min_samples_leaf', 0, 0.5),
                     min_samples_split=hp.uniform('min_samples_split', 0, 1),
                     n_estimators=hp.choice('n_estimators', [10, 50])
                     )
    elif model == 'AB':
        space = dict(n_estimators=hp.choice('n_estimators', range(50, 100)),
                     learning_rate=hp.quniform('learning_rate', 0, 0.05, 0.0001)
                     )

    elif model == 'XGB':
        space = dict(learning_rate=hp.quniform('learning_rate', 0, 0.05, 0.0001),
                     n_estimators=hp.choice('n_estimators', range(100, 1000)),
                     eta=hp.quniform('eta', 0.025, 0.5, 0.005),
                     max_depth=hp.choice('max_depth', np.arange(2, 12, dtype=int)),
                     min_child_weight=hp.quniform('min_child_weight', 1, 9, 0.025),
                     subsample=hp.quniform('subsample', 0.5, 1, 0.005),
                     gamma=hp.quniform('gamma', 0.5, 1, 0.005),
                     colsample_bytree=hp.quniform('colsample_bytree', 0.5, 1, 0.005)
                     )
    elif model == 'LGB':
        space = dict(learning_rate=hp.quniform('learning_rate', 0, 0.05, 0.0001),
                     n_estimators=hp.choice('n_estimators', range(100, 1000)),
                     max_depth=hp.choice('max_depth', np.arange(2, 12, dtype=int)),
                     num_leaves=hp.choice('num_leaves', 2 * np.arange(2, 2 ** 11, dtype=int)),
                     min_child_weight=hp.quniform('min_child_weight', 1, 9, 0.025),
                     colsample_bytree=hp.quniform('colsample_bytree', 0.5, 1, 0.005)
                     )

    elif model == 'CTB':
        space = dict(n_estimators=hp.choice('n_estimators', np.arange(50, 250, 25)),
                     max_depth=hp.choice('max_depth', np.arange(2, 12, dtype=int)),
                     learning_rate=hp.quniform('learning_rate', 0, 0.05, 0.0001),
                     reg_lambda=hp.uniform('reg_lambda', 1, 10)
                     )

    elif model == 'NGB':
        space = dict(n_estimators=hp.choice('n_estimators', np.arange(50, 250, 25)),
                     learning_rate=hp.quniform('learning_rate', 0, 0.05, 0.0001),
                     minibatch_frac=hp.choice('minibatch_frac', [1.0, 0.5]),
                     tol=hp.uniform('tol', 0.00001, 0.0001),
                     )
    return space


def get_acc_status(clf, X, y):
    acc = cross_val_score(clf, X, y, cv=5).mean()
    return {'loss': -acc, 'status': STATUS_OK}


def best_search_tuning(model_name, X, y):
    model_type, _num_class,_ = target_count_class(y)

    trials = Trials()

    space = search_space(model_name)
    if model_type == "regression":
        if model_name == "LR":
            space = dict(fit_intercept=hp.choice('fit_intercept', [True, False]),
                         normalizebool=hp.choice('normalizebool', [True, False]),
                         positivebool=hp.choice('positivebool', [True, False])
                         )

    def obj_fnc(params):
        clf = search_model(model_name, model_type, _num_class)
        clf.set_params(**params)
        return get_acc_status(clf, X, y)

    best = fmin(
        fn=obj_fnc,
        space=space,
        algo=tpe.suggest,
        max_evals=50,
        trials=trials
    )
    best = space_eval(space, best)
    return best


def get_dataset_parameter_baseline(train, target, feature_name, model_name):
    X = train[feature_name]
    y = target
    best_parameter_tuning = best_search_tuning(model_name, X, y)
    return best_parameter_tuning
