from .simulationwithredux2 import Simulator
from .simulationwithredux2 import simpleODESolver
from .simulationwithredux2 import createDataSelector

import scipy.integrate as integrate

def CreateDataSelector(masterMaps, maps):
    def extractor(dataItem):
        result = {}
        for masterName, masterFunc in masterMaps.items():
            row = masterFunc(dataItem)
            for name, func in maps.items():
                result[masterName + name] = func(row)
        return result
    return extractor

def SimpleODESolver(model, t0, state0, t_bound, max_step):
    if not callable(model):
        raise ValueError('Model must be callable')

    solver = integrate.RK45(fun = model, t0 = t0, y0 = state0, t_bound = t_bound, max_step = max_step)
    currentItem = {'time': solver.t, 'y': [*state0], 'yd': [*model(t0, state0)]}
    while True:
        yield currentItem # send signal, inform about current result
        message = solver.step()
        currentItem = {'time': solver.t, 'y': [*solver.y], 'yd': [*model(solver.t, solver.y)]}
        if (not(solver.status == 'running')):
            break    