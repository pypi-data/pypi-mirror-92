#!/usr/bin/env python
# coding: utf-8

# # Simulace s využitím konceptu Redux

# ## Koncept stavového automatu (Redux)

# In[214]:


# ### Logs

# In[215]:


def addLog(state, action):
    if 'data' in action:
        result = [*state, {'msg': action['msg'], **action['data']}]
    else:
        result = [*state, {'msg': action['msg']}]
    return result

def limitLog(state, action):
    result = list(state[len(state)-action['lenght']:])
    return result

logDescription = {
    'addLog': addLog,
    'limitLog': limitLog
}


# In[216]:





# ### Events

# In[217]:


def addEvent(state, action):
    eventList = [*state['events'], 
        {'time': action['time'], 'executor': action['executor'], 'kwargs': action['kwargs']}
             ]
    eventList.sort(key = lambda item: item['time'])
    result = {'events': eventList, 'activeEvent': state['activeEvent']}
    return result

def popEvent(state, action):
    eventList = [*state['events']]
    if len(eventList) > 0:
        oldestEvent = eventList.pop(0)
    else:
        oldestEvent = None
    result = {'events': eventList, 'activeEvent': oldestEvent}
    return result

eventDescription = {
    'addEvent': addEvent,
    'popEvent': popEvent
}


# ### ODEModels

# In[218]:


defaultModelAttributes = {'destroyed': False, 'state': None}

def setModelAttributes(allModels, id, **attributes):
    modelRow = allModels[id]
    result = {**allModels, id: {**modelRow, **attributes}}
    return result

def destroyODEModel(state, action):
    id = action['modelId']
    return setModelAttributes(state, id, destroyed=True)

def setODEModelState(state, action):
    id = action['modelId']
    return {**state, id: {**defaultModelAttributes, 'state': action['modelState']}}

def changeODEModelState(state, action):
    result = state
    id = action['modelId']
    if id in state:
        result = setModelAttributes(allModels=state, id=id, state=action['modelState'])
    return result

def changeODEModelAttribute(state, action):
    result = state
    id = action['modelId']
    if id in state:
        result = setModelAttributes(allModels=state, id=id, **{action['attributeName']: action['attributeValue']})
    return result
    
odeDescription = {
    'destroyODEModel': destroyODEModel,
    'setODEModelState': setODEModelState,
    'changeODEModelState': changeODEModelState,
    'changeODEModelAttribute': changeODEModelAttribute
}    


# ### Custom class

# In[219]:


def createCustomClass(className, superClass, attributeDict):
    """
    more descriptive
    """
    return type(className, superClass, attributeDict)


# ### All Together

# In[220]:


def wrapReducer(reducer, pre = None, post = None):
    def wrappedReducer(state, action):
        innerState = pre(state)
        newState = reducer(innerState, action)
        result = post(state, newState)
        return result
    return wrappedReducer

def createPre(key1):
    return lambda state: state[key1]

def createPost(key1):
    return lambda state, subState: {**state, key1: subState}

def createActionCreator(typeValue):
    def createAction(self, **kwargs):
        return {'type': typeValue, **kwargs}
    return createAction

def compoundReducers(description):
    def reducer(state, action):
        actionType = action['type']
        if actionType in description:
            selectedReducer = description[actionType]
            newState = selectedReducer(state, action)
            return newState
        else:
            return state
    return reducer

def twoLayerReducer(description):
    result = {}
    actionsMaster = {}
    for key1, value1 in description.items():
        actionsSlaver = {}
        for key2, func in value1.items():
            fullIndex = key1 + '.' + key2
            result[fullIndex] = wrapReducer(func, pre=createPre(key1), post=createPost(key1))
            actionsSlaver[key2] = createActionCreator(fullIndex)
        
        actionsMaster[key1] = createCustomClass('SlaveActions_' + key1, (), actionsSlaver)()
        
    fullReducer = compoundReducers(result)
    
    actions = createCustomClass('Actions', (), actionsMaster)()
    return fullReducer, actions
    
allDescription = {
    'odeModels': {
        'destroyODEModel': destroyODEModel,
        'setODEModelState': setODEModelState,
        'changeODEModelState': changeODEModelState,
        'changeODEModelAttribute': changeODEModelAttribute
    },
    'eventList': {
        'addEvent': addEvent,
        'popEvent': popEvent
    },
    'logs': {
        'addLog': addLog,
        'limitLog': limitLog
    }
}


# ## Koncept centrálního uložení (Store)

# In[221]:


class Store():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
    pass            

def createStore(reducer, initialState=None, enhancer=None):
    currentReducer = reducer
    currentState = initialState
    dispatching = False
    
    def dispatch(action):
        nonlocal dispatching
        nonlocal currentState
        if callable(action):
            raise Exception("Use special middleware for callable actions")
        if dispatching:
            raise Exception("Detected dispatch call while dispatching")
        try:
            dispatching = True
            currentState = currentReducer(currentState, action)
        finally:
            dispatching = False
        
        return action
    
    def getState():
        if dispatching:
            raise Exception("You shouldn't ask for new instance of state while dispatching")
        return currentState
        
    def replaceReducer(reducer):
        if callable(reducer):
            currentReducer = reducer
        else:
            raise Exception("Reducer must be callable")
        pass

    if (not enhancer is None) & callable(enhancer):
        return enhancer(createStore)(reducer, initialState)
    else:
        # return Store(dispatch=dispatch, getState=getState, replaceReducer=replaceReducer)
        return createCustomClass('Store', (), {'dispatch': dispatch, 'getState': getState, 'replaceReducer': replaceReducer})


# ### Middlewares

# In[222]:


def compose(*F):
    def inner(*args, **kwargs):
        result = None
        firstCall = True
        funcs = list(F)
        #funcs.reverse()
        for f in funcs:
            if firstCall:
                result = f(*args, **kwargs)
                firstCall = False
            else:
                result = f(result)
        return result
            
    if len(F) == 0:
        return lambda arg: arg
    else:
        return inner


# In[223]:


def applyMiddleware(*middlewares):
    def result(createStore):
        def inner(reducer, preloadedState):
            store = createStore(reducer, preloadedState)
            def dispatch():
                raise Exception("Do not use dispatch during store creation")

            middlewareAPI = {
                'getState': store.getState,
                'dispatch': lambda action, *args: dispatch(action, *args)
            }    

            chain = map(lambda middleware: middleware(**middlewareAPI), middlewares)
            
            dispatch = compose(*chain)(store.dispatch)
            
            storeParams = {**store.__dict__, 'dispatch': dispatch}
            return Store(**storeParams)
        return inner
    return result
# original can be found at https://github.com/reduxjs/redux/blob/master/src/applyMiddleware.ts


# In[224]:


def createThunkMiddleware(**kwargs):
    def inner(dispatch, getState):
        def nextWrapper(next):
            def actionWrapper(action):
                if callable(action):
                    return action(dispatch, getState, **kwargs)
                return next(action)
            return actionWrapper
        return nextWrapper
    return inner

# original can be found at https://github.com/reduxjs/redux-thunk/blob/master/src/index.js
#function createThunkMiddleware(extraArgument) {
#  return ({ dispatch, getState }) => (next) => (action) => {
#    if (typeof action === 'function') {
#      return action(dispatch, getState, extraArgument);
#    }
#    return next(action);
#  };
#}


# In[225]:


def actionCreator(dispatch, description):
    def innerActionCreator(lowDesc):
        result = {}
        for key, func in lowDesc.items():
            result[key] = lambda **kwargs: dispatch({'type': key, **kwargs})
        pass
    return innerActionCreator


# ## Final Platform

# In[ ]:





# In[226]:


def simInit():
    simStoreDescription = {
        'odeModels': {
            'destroyODEModel': destroyODEModel,
            'setODEModelState': setODEModelState,
            'changeODEModelState': changeODEModelState,
            'changeODEModelAttribute': changeODEModelAttribute
        },
        'eventList': {
            'addEvent': addEvent,
            'popEvent': popEvent
        },
        'logs': {
            'addLog': addLog,
            'limitLog': limitLog
        }
    }

    simStateZero = {
        'odeModels': {},
        'eventList':  {'events': [], 'activeEvent': None},
        'logs': []}

    simReducer, simActions = twoLayerReducer(simStoreDescription)
    thunk = createThunkMiddleware()
    simStore = createStore(simReducer, simStateZero, applyMiddleware(thunk))
    
    return simStore, simActions


# In[227]:

simStore, simActions = simInit()
def stepAction(addEventCreator=simActions.eventList.addEvent, popEventCreator=simActions.eventList.popEvent):
    def action(dispatch, getState):
        dispatch(popEventCreator())
        eventToExecute = getState()['eventList']['activeEvent']
        
        if not eventToExecute is None:

            func = eventToExecute['executor']
            time = eventToExecute['time']
            kwargs = {}
            if 'kwargs' in eventToExecute:
                kwargs = eventToExecute['kwargs']
            func(time, **kwargs)

        return eventToExecute
    return action

def createSimStep(simStore):
    def simStep():
        return simStore.dispatch(stepAction())
    return simStep
    
def simInit2():
    simStore, simActions = simInit()
    simStep = createSimStep(simStore)
    def simAddEvent(time, executor, **kwargs):
        simStore.dispatch(simActions.eventList.addEvent(time=time, executor=executor, kwargs=kwargs))
    
    def simRun():
        while True:
            if simStep() is None:
                break
            yield simStore, simActions, simStep, simAddEvent
    
    return simStore, simActions, simStep, simAddEvent, simRun

simStore, simActions, simStep, simAddEvent, simRun = simInit2()


# ## ODE Solver

# In[229]:


import scipy.integrate as integrate # for numerical solution od differential equations

def simpleODESolver(model, t0, state0, t_bound, max_step):
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


# In[230]:


def createOnItem(func, *aparams, **nparams):
    def onItem(sequence):
        for item in sequence:
            func(item, *aparams, **nparams)
            yield item
    return onItem


# In[231]:


import random
import string

def rndg():
    #symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    symbols = string.ascii_lowercase
    result = ''.join(random.choice(symbols) for i in range(10))
    return result

def attachODESolver(solver, simStore, simActions, simAddEvent, onStep=lambda modelId, getState: None, **attributes):
    modelId = rndg()
    changeODEModelState = simActions.odeModels.changeODEModelState
    dispatch = simStore.dispatch
    getState = simStore.getState
    
    def stepper(time, state):
        modelDatabaseRow = getState()['odeModels'][modelId]
        if not modelDatabaseRow['destroyed']:
            dispatch(changeODEModelState(modelId=modelId, modelState=state))
            modelDatabaseRow = getState()['odeModels'][modelId]
            onStep(modelId, getState)
            newState = next(solver)
            simAddEvent(newState['time'], stepper, state=newState)
            
        return state
    
    firstModelState = next(solver)
    dispatch(simActions.odeModels.setODEModelState(modelId=modelId, modelState=firstModelState))
    for key, value in attributes.items():
        dispatch(simActions.odeModels.changeODEModelAttribute(modelId=modelId, attributeName=key, attributeValue=value))
        
    simAddEvent(firstModelState['time'], stepper, state=firstModelState)
    return modelId


# In[232]:


def model2D(time, state):
    return [state[2], state[3], 0, -9.81]


# ## Data Reader

# In[233]:


def createDataSelector(masterMaps, maps):
    def extractor(dataItem):
        result = {}
        for masterName, masterFunc in masterMaps.items():
            row = masterFunc(dataItem)
            for name, func in maps.items():
                result[masterName + name] = func(row)
        return result
    return extractor

dataDescriptor = {
    't': lambda item: item['state']['time'],
    'x': lambda item: item['state']['y'][0],
    'y': lambda item: item['state']['y'][1],
    'd': lambda item: item['destroyed']
}


# ## Final Platform as a Class

# In[235]:


class SimulatorActions_():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
    pass            

    
class Simulator():
    def __init__(self):
        simStore, simActions, simStep, simAddEvent, simRun = simInit2()  
        self._simStore = simStore
        self._simActions = simActions

        self._dispatch = simStore.dispatch
        self._simStep = simStep
        self._simRun = simRun
        self._simActions = simActions
        self._simAddEvent = simAddEvent
        pass
    
    def Dispatch(self, action):
        self._simStore.dispatch(action)
        return self
    
    def GetState(self):
        return self._simStore.getState()
    
    def Step(self):
        return self._simStep()
    
    def Run(self, mapFunc=lambda item: item['odeModels']):
        if not mapFunc is None:
            for i in self._simRun():
                yield mapFunc(self.GetState())
        else:
            for i in self._simRun():
                yield self
    
    
    simStoreDescription = {
        'odeModels': {
            'destroyODEModel': destroyODEModel,
            'setODEModelState': setODEModelState,
            'changeODEModelState': changeODEModelState,
            'changeODEModelAttribute': changeODEModelAttribute
        },
        'eventList': {
            'addEvent': addEvent,
            'popEvent': popEvent
        },
        'logs': {
            'addLog': addLog,
            'limitLog': limitLog
        }
    }
    
    def DestroyODEModel(self, modelId):
        return self.Dispatch(self._simActions.odeModels.destroyODEModel(modelId=modelId))
    
    def SetODEModelState(self, modelId, modelState):
        return self.Dispatch(self._simActions.odeModels.setODEModelState(modelId=modelId, modelState=modelState))
    
    def ChangeODEModelState(self, modelId, modelState):
        return self.Dispatch(self._simActions.odeModels.changeODEModelState(modelId=modelId, modelState=modelState))
    
    def ChangeODEModelAttributes(self, modelId, **attributes):
        result = self
        for key, value in attributes.items():
            result = self.Dispatch(self._simActions.odeModels.changeODEModelAttribute(modelId=modelId, attributeName=key, attributeValue=value))
        return result
    
    def AddEvent(self, time, func, **kwargs):
        return self.Dispatch(self._simActions.eventList.addEvent(time=time, executor=func, kwargs=kwargs))
    
    def PopEvent(self):
        return self.Dispatch(self._simActions.eventList.popEvent())
    
    def AddLog(self, msg, **data):
        return self.Dispatch(self._simActions.logs.addLog(msg=msg, data=data))
    
    def LimitLog(self, lenght):
        return self.Dispatch(self._simActions.logs.limitLog(lenght=lenght))
        
    def AttachODESolver(self, solver, onStep=lambda time, modelId, getState: None, **odeModelAttributes):
        #attachODESolver(solver, simStore, simActions, simAddEvent, onStep=lambda modelId, getState: None, **attributes):
        modelId = rndg()
        changeODEModelState = self._simActions.odeModels.changeODEModelState
        dispatch = self.Dispatch
        getState = self.GetState
        addEvent = self.AddEvent

        def stepper(time, state):
            modelDatabaseRow = getState()['odeModels'][modelId]
            if not modelDatabaseRow['destroyed']:
                dispatch(changeODEModelState(modelId=modelId, modelState=state))
                modelDatabaseRow = getState()['odeModels'][modelId]
                onStep(time, modelId, dispatch)
                newState = next(solver)
                addEvent(newState['time'], stepper, state=newState)

            return state

        firstModelState = next(solver)
        dispatch(simActions.odeModels.setODEModelState(modelId=modelId, modelState=firstModelState))
        for key, value in odeModelAttributes.items():
            dispatch(simActions.odeModels.changeODEModelAttribute(modelId=modelId, attributeName=key, attributeValue=value))

        self.AddEvent(firstModelState['time'], stepper, state=firstModelState)
        return modelId    

