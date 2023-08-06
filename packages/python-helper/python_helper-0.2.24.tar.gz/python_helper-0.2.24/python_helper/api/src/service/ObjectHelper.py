from numbers import Number
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import StringHelper
from python_helper.api.src.helper import ObjectHelperHelper

GENERATOR_CLASS_NAME = 'generator'
UNKNOWN_OBJECT_CLASS_NAME = c.UNKNOWN.lower()

METADATA_NAME = 'metadata'

NATIVE_CLASS_LIST = [
    bool,
    int,
    str,
    float,
    bytes,
    type(ObjectHelperHelper.generatorInstance())
]

COLLECTION_CLASS_LIST = [
    list,
    dict,
    tuple,
    set
]

def equal(responseAsDict,expectedResponseAsDict,ignoreKeyList=None,ignoreCharactereList=None) :
    innerIgnoreCharactereList = [c.SPACE]
    if isNotNone(ignoreCharactereList) :
        innerIgnoreCharactereList += ignoreCharactereList
    filteredResponse = StringHelper.filterJson(
        str(sortIt(filterIgnoreKeyList(responseAsDict,ignoreKeyList))),
        extraCharacterList=innerIgnoreCharactereList
    )
    filteredExpectedResponse = StringHelper.filterJson(
        str(sortIt(filterIgnoreKeyList(expectedResponseAsDict,ignoreKeyList))),
        extraCharacterList=innerIgnoreCharactereList
    )
    return filteredResponse == filteredExpectedResponse

def sortIt(thing) :
    if isDictionary(thing) :
        sortedDictionary = {}
        for key in getSortedCollection(thing) :
            sortedDictionary[key] = sortIt(thing[key])
        return sortedDictionary
    elif isCollection(thing) :
        newCollection = []
        for innerValue in thing :
            newCollection.append(sortIt(innerValue))
        return getSortedCollection(newCollection)
    else :
        return thing

def getSortedCollection(thing) :
    return thing if isNotCollection(thing) else sorted(
        thing,
        key=lambda x: (
            x is not None, c.NOTHING if isinstance(x, Number) else type(x).__name__, x
        )
    )

def filterIgnoreKeyList(objectAsDictionary,ignoreKeyList):
    if isDictionary(objectAsDictionary) and isNotNone(ignoreKeyList) :
        filteredObjectAsDict = {}
        for key, value in objectAsDictionary.items() :
            if key not in ignoreKeyList :
                if isDictionary(value) :
                    filteredObjectAsDict[key] = filterIgnoreKeyList(value,ignoreKeyList)
                else :
                    filteredObjectAsDict[key] = objectAsDictionary[key]
        return filteredObjectAsDict
    return objectAsDictionary

def isEmpty(thing) :
    return StringHelper.isBlank(thing) if isinstance(thing, str) else isNone(thing) or isEmptyCollection(thing)

def isNotEmpty(thing) :
    return not isEmpty(thing)

def isEmptyCollection(thing) :
    return isCollection(thing) and 0 == len(thing)

def isNotEmptyCollection(thing) :
    return isCollection(thing) and 0 < len(thing)

def isList(thing) :
    return isinstance(thing, list)

def isNotList(thing) :
    return not isList(thing)

def isSet(thing) :
    return isinstance(thing, set)

def isNotSet(thing) :
    return not isSet(thing)

def isTuple(thing) :
    return isinstance(thing, tuple)

def isNotTuple(thing) :
    return not isTuple(thing)

def isDictionary(thing) :
    return isinstance(thing, dict)

def isNotDictionary(thing) :
    return not isDictionary(thing)

def isDictionaryClass(thingClass) :
    return dict == thingClass

def isNotDictionaryClass(thingClass) :
    return not isDictionaryClass(thingClass)

def isNone(instance) :
    return instance is None

def isNotNone(instance) :
    return not isNone(instance)

def isNativeClass(instanceClass) :
    return isNotNone(instanceClass) and instanceClass in NATIVE_CLASS_LIST

def isNotNativeClass(instanceClass) :
    return not isNativeClass(instanceClass)

def isNativeClassIsntance(instance) :
    return isNotNone(instance) and isNativeClass(instance.__class__)

def isNotNativeClassIsntance(instance) :
    return not isNativeClassIsntance(instance)

def isCollection(instance) :
    return isNotNone(instance) and instance.__class__ in COLLECTION_CLASS_LIST

def isNotCollection(instance) :
    return not isCollection(instance)
