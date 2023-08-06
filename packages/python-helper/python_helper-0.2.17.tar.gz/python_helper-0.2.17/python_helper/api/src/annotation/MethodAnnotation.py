from python_helper.api.src.service import LogHelper, ReflectionHelper
from python_helper.api.src.domain import Constant as c

def Function(function,*args,**kwargs) :
    def wrapedFunction(*args,**kwargs) :
        try :
            functionReturn = function(*args,**kwargs)
        except Exception as exception :
            functionName = ReflectionHelper.getName(function, typeName=ReflectionHelper.FUNCTION_TYPE_NAME)
            LogHelper.wraper(Function,f'''failed to execute "{functionName}(args={args}, kwargs={kwargs})" {ReflectionHelper.FUNCTION_TYPE_NAME} call''',exception)
            raise Exception(f'{functionName} {ReflectionHelper.FUNCTION_TYPE_NAME} error{c.DOT_SPACE_CAUSE}{str(exception)}')
        return functionReturn
    ReflectionHelper.overrideSignatures(wrapedFunction, function)
    return wrapedFunction

def FunctionThrough(function,*args,**kwargs) :
    def wrapedFunction(*args,**kwargs) :
        try :
            functionReturn = function(*args,**kwargs)
        except Exception as exception :
            functionName = ReflectionHelper.getName(function, typeName=ReflectionHelper.FUNCTION_TYPE_NAME)
            LogHelper.wraper(Function,f'''exception trace passed through "{functionName}(args={args}, kwargs={kwargs})" {ReflectionHelper.FUNCTION_TYPE_NAME} call''',exception)
            raise exception
        return functionReturn
    ReflectionHelper.overrideSignatures(wrapedFunction, function)
    return wrapedFunction

def Method(method,*args,**kwargs) :
    def wrapedMethod(*args,**kwargs) :
        try :
            methodReturn = method(*args,**kwargs)
        except Exception as exception :
            className = ReflectionHelper.getName(args[0].__class__, typeName=ReflectionHelper.CLASS_TYPE_NAME)
            methodName = ReflectionHelper.getName(method, typeName=ReflectionHelper.METHOD_TYPE_NAME)
            LogHelper.wraper(Method,f'''failed to execute "{className}{c.DOT}{methodName}(args={args}, kwargs={kwargs})" {ReflectionHelper.METHOD_TYPE_NAME} call''',exception)
            raise Exception(f'{className}{c.DOT}{methodName} {ReflectionHelper.METHOD_TYPE_NAME} error{c.DOT_SPACE_CAUSE}{str(exception)}')
        return methodReturn
    ReflectionHelper.overrideSignatures(wrapedMethod, method)
    return wrapedMethod
