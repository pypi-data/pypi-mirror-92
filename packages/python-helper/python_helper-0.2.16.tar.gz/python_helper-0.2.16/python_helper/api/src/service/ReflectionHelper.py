from python_helper.api.src.domain  import Constant as c
from python_helper.api.src.service import LogHelper, ObjectHelper, StringHelper, RandomHelper

MAXIMUN_ARGUMENTS = 20

CLASS_TYPE_NAME = 'class'
METHOD_TYPE_NAME = 'method'
BUILTIN_FUNCTION_OR_METHOD_TYPE_NAME = 'builtin_function_or_method'
FUNCTION_TYPE_NAME = 'function'

UNKNOWN_TYPE_NAME = f'{c.UNKNOWN.lower()} type'
NAME_NOT_PRESENT = 'name not present'

METHOD_TYPE_NAME_LIST = [
    METHOD_TYPE_NAME,
    BUILTIN_FUNCTION_OR_METHOD_TYPE_NAME
]

def getAttributeOrMethod(instance, name) :
    attributeOrMethodInstance = None
    try :
        attributeOrMethodInstance = None if ObjectHelper.isNone(instance) or ObjectHelper.isNone(name) else getattr(instance, name)
    except Exception as exception :
        LogHelper.warning(getAttributeOrMethod, f'Not possible to get "{name}" from "{getName(instance.__class__, typeName=CLASS_TYPE_NAME) if ObjectHelper.isNotNone(instance) else instance}" instance', exception=exception)
    return attributeOrMethodInstance

def getAttributeAndMethodNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        attributeOrMethodName
        for attributeOrMethodName in dir(objectNullArgsInstance)
        if isNotPrivate(attributeOrMethodName)
    ]

def isAttributeName(attributeName, objectNullArgsInstance) :
    return isNotPrivate(attributeName) and isNotMethod(objectNullArgsInstance, attributeName)

def getAttributeNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        attributeName
        for attributeName in dir(objectNullArgsInstance)
        if isAttributeName(attributeName, objectNullArgsInstance)
    ]

def getMethodNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        methodName
        for methodName in dir(objectNullArgsInstance)
        if isNotPrivate(methodName) and isMethod(objectNullArgsInstance, methodName)
    ]

def isMethodInstance(methodInstance) :
    return getName(methodInstance.__class__) in METHOD_TYPE_NAME_LIST if ObjectHelper.isNotNone(methodInstance) else False

def isNotMethodInstance(methodInstance) :
    return not isMethodInstance(methodInstance)

def isMethod(objectInstance, name) :
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name) :
        return False
    return isMethodInstance(getAttributeOrMethod(objectInstance, name))

def isNotMethod(objectInstance, name) :
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name) :
        return False
    return isNotMethodInstance(getAttributeOrMethod(objectInstance, name))

def instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=None) :
    if ObjectHelper.isNone(args) :
        args = []
    for _ in range(amountOfNoneArgs) :
        args.append(None)
    objectInstance = None
    for _ in range(MAXIMUN_ARGUMENTS) :
        try :
            objectInstance = targetClass(*args)
            break
        except :
            args.append(None)
    if not isinstance(objectInstance, targetClass) :
        raise Exception(f'Not possible to instanciate {targetClass} class in instanciateItWithNoArgsConstructor() method with None as args constructor')
    return objectInstance

def getArgsOrder(targetClass) :
    noneArgs = []
    noneInstance = instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=noneArgs)
    strArgs = []
    for arg in range(len(noneArgs)) :
        strArgs.append(RandomHelper.string(minimum=10))
    try :
        instance = targetClass(*strArgs)
        instanceDataDictionary = getAttributeDataDictionary(instance)
        argsOrderDictionary = {}
        for key,value in instanceDataDictionary.items() :
            if StringHelper.isNotBlank(value) :
                argsOrderDictionary[strArgs.index(value)] = key
        argsOrder = [argsOrderDictionary[key] for key in sorted(argsOrderDictionary)]
    except Exception as exception :
        errorMessage = f'Not possible to get args order from "{getName(targetClass)}" target class'
        LogHelper.error(getArgsOrder, errorMessage, exception)
        raise Exception(errorMessage)
    return argsOrder

def isNotPrivate(attributeOrMethodName) :
    return StringHelper.isNotBlank(attributeOrMethodName) and (
        not attributeOrMethodName.startswith(f'{2 * c.UNDERSCORE}') and
        not attributeOrMethodName.startswith(c.UNDERSCORE) and
        not ObjectHelper.METADATA_NAME == attributeOrMethodName
    )

def getAttributePointerList(instance) :
    return [
        getattr(instance, instanceAttributeOrMethodName)
        for instanceAttributeOrMethodName in dir(instance)
        if isNotPrivate(instanceAttributeOrMethodName)
    ]

def getAttributeDataList(instance) :
    return [
        (getattr(instance, instanceAttributeName), instanceAttributeName)
        for instanceAttributeName in dir(instance)
        if isAttributeName(instanceAttributeName, instance)
    ]

def getAttributeDataDictionary(instance) :
    instanceDataDictionary = {}
    for name in dir(instance) :
        if isAttributeName(name, instance) :
            instanceDataDictionary[name] = getattr(instance, name)
    return instanceDataDictionary

def setAttributeOrMethod(instance, attributeOrMethodName, attributeOrMethodInstance) :
    setattr(instance, attributeOrMethodName, attributeOrMethodInstance)

def overrideSignatures(toOverride, original) :
    try :
        toOverride.__name__ = original.__name__
        toOverride.__module__ = original.__module__
        toOverride.__qualname__ = original.__qualname__
    except Exception as exception :
        LogHelper.error(overrideSignatures,f'''failed to override signatures of {toOverride} by signatures of {original} method''',exception)

def getName(thing, typeName=None) :
    name = None
    try :
        name = thing.__name__
    except :
        if ObjectHelper.isNone(typeName) or StringHelper.isBlank(typeName) :
            name = f'({NAME_NOT_PRESENT})'
        else :
            name = f'({typeName} {NAME_NOT_PRESENT})'
    return name

def printDetails(toDetail):
    print(f'{2 * c.TAB}printDetails({toDetail}):')
    try :
        print(f'{2 * c.TAB}type({toDetail}).__name__ = {getName(type(toDetail), typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__ = {type(toDetail).__class__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__module__ = {type(toDetail).__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__name__ = {getName(type(toDetail).__class__, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__name__ = {getName(toDetail.__class__, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__module__ = {toDetail.__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__qualname__ = {toDetail.__class__.__qualname__}')
    except :
        pass

def printClass(instanceClass) :
    print(f'{2 * c.TAB}printClass({instanceClass}):')
    try :
        print(f'{2 * c.TAB}{instanceClass}.__name__ = {getName(instanceClass, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__module__ = {instanceClass.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__qualname__ = {instanceClass.__qualname__}')
    except :
        pass
