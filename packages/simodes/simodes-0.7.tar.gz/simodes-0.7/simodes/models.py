from math import sqrt, atan2, pi

def normalizeDeltaAngle(delta):
    result = delta
    if (result > pi):
        result -= 2 * pi
    if (result < -pi):
        result += 2 * pi
    return result

def controllerPitchYawWithDestination(t, state, destination  = [0, 0, 0], maxYawA = 20, maxPitchA = 20, epsAngle = 0.001):
    currentVelocity = state[6]
    currentPitch = state[7]
    currentYaw = state[8]

    currentPosition = np.array(state[:3])
    destinationPoisition = np.array(destination[:3])
    radiusVector = destinationPoisition - currentPosition
    radiusVectorAbs = np.linalg.norm(radiusVector)
    radiusVector1 = radiusVector / radiusVectorAbs

    paramxy = sqrt(radiusVector1[0] * radiusVector1[0] + radiusVector1[1] * radiusVector1[1])
    yaw = atan2(radiusVector1[1], radiusVector1[0])
    pitch = atan2(radiusVector1[2], paramxy)#asin(paramxy)

    #https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
    deltaYaw = normalizeDeltaAngle(yaw - currentYaw)
    deltaPitch = normalizeDeltaAngle(pitch - currentPitch)

    #a = ω·v
    #v = ω·r
    epsV = 10
    if currentVelocity < epsV:
        # nizka rychlost, tedy bez manevru
        dYaw = 0
        dPitch = 0
    else:
        dYaw = maxYawA / currentVelocity # trust it is not zero
        if deltaYaw < -epsAngle:
            dYaw = -dYaw
        elif deltaYaw < epsAngle:
          #deltaYaw ∈ (-epsAngle, epsAngle)
          dYaw = 0

        dPitch = maxPitchA / currentVelocity # trust it is not zero
        if deltaPitch < -epsAngle:
            dPitch = -dPitch
        elif deltaPitch < epsAngle:
          #deltaPitch ∈ (-epsAngle, epsAngle)
          dPitch = 0

    dv = 0 # velocity WO change
    return dv, dPitch, dYaw

from math import sin, cos
import numpy as np

def computeState(px, py, pz, v, pitch, yaw):
    return [px, py, pz, v * cos(pitch) * cos(yaw), v * cos(pitch) * sin(yaw), v * sin(pitch), v, pitch, yaw]

def planePitchYawModel(t, state, controller):
    #state = [x, y, z, vx, vy, vz, v, pitch, yaw]

    dv, dPitch, dYaw = controller(t, state)

    currentVelocity = state[6]
    currentPitch = state[7]
    currentYaw = state[8]

    try:
        cospitch = cos(currentPitch)
        sinpitch = sin(currentPitch)
        cosyaw = cos(currentYaw)
        sinyaw = sin(currentYaw)
    except ValueError:

        cospitch = 0
        sinpitch = 0
        cosyaw = 0
        sinyaw = 0

    v = currentVelocity

    vx = v * cospitch * cosyaw
    vy = v * cospitch * sinyaw
    vz = v * sinpitch

    #dvx = dv * cospitch * cosyaw - v * sinpitch * cosyaw * dPitch - v * cospitch * sinyaw * dYaw
    #dvy = dv * cospitch * sinyaw - v * sinpitch * sinyaw * dPitch + v * cospitch * cosyaw * dYaw
    #dvz = dv * sinpitch + v * cospitch * dPitch
    
    vcospitch = v * cospitch
    vsinpitch = vz
    vsdPitch = vsinpitch * dPitch
    vcdYaw = vcospitch * dYaw
    dvx = dv * cospitch * cosyaw - cosyaw * vsdPitch - sinyaw * vcdYaw
    dvy = dv * cospitch * sinyaw - sinyaw * vsdPitch + cosyaw * vcdYaw
    dvz = dv * sinpitch + vcospitch * dPitch

    dx = vx
    dy = vy
    dz = vz

    return [dx, dy, dz, dvx, dvy, dvz, dv, dPitch, dYaw] 

def upgradeControlerFromDestinationToPath(controller, path, eps = 5):
    buffer = {
        'currentDestination': next(path),
        'outOfPoints': False
        }
    def compareDestinationWithState(state, destination):
        sumation = 0
        for index in range(3):
            delta = state[index] - destination[index]
            sumation = sumation + delta * delta
    
        result = sumation < eps
        return result

    def innerController(t, state):
        if buffer['outOfPoints']:
            return 0, 0, 0

        #decide about current destination
        if compareDestinationWithState(state, buffer['currentDestination']):
            try:
                nextDestination = next(path)
            except StopIteration:
                buffer['outOfPoints'] = True
            else:
                buffer['currentDestination'] = nextDestination
    
        #ask controller
        return controller(t, state, buffer['currentDestination'])
    return innerController

def definePlane(pitchYawModel=planePitchYawModel, destinationController=controllerPitchYawWithDestination, pathToFlyThrough=[], controllerParams=None):
    cFunc = destinationController
    if (not controllerParams is None):
        cFunc = lambda t, state, destination: destinationController(t, state, destination=destination, **controllerParams) 
    fullController = upgradeControlerFromDestinationToPath(cFunc, pathToFlyThrough)
    plane = lambda t, state: pitchYawModel(t, state, fullController)
    return plane

    
import numpy as np

def rocketModel(time, state, targetFunction, n=3):
    currentInput = targetFunction()

    currentPosition = np.array(state[:3])
    currentVelocity = np.array(state[3:6])

    targetPosition = np.array(currentInput[:3])
    targetVelocity  = np.array(currentInput[3:6])
    currentVelocityAbs = np.linalg.norm(currentVelocity) # abs of vector

    positionR = targetPosition - currentPosition
    positionRAbs = np.linalg.norm(positionR) # abs of vector
    velocityR = targetVelocity - currentVelocity
    velocityRAbs = np.linalg.norm(velocityR) # abs of vector

    omega = 1 / positionRAbs / positionRAbs * np.cross(positionR, velocityR)

    neededAcceleration = -n * velocityRAbs / currentVelocityAbs * \
      np.cross(currentVelocity, omega)
    result = [*currentVelocity, *neededAcceleration]

    return result

def defineRocket(targetFunction, rocketModel=rocketModel, **extraModelParams):
    fixedRocketModel = lambda t, state: rocketModel(t, state, targetFunction, **extraModelParams)
    return fixedRocketModel    