from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import LogHelper, EnvironmentHelper, ObjectHelper, SettingHelper

def getOriginalEnvironmentVariables(environmentVariables) :
    originalActiveEnvironment = None if ObjectHelper.isNone(SettingHelper.ACTIVE_ENVIRONMENT_VALUE) else f'{c.NOTHING}{SettingHelper.ACTIVE_ENVIRONMENT_VALUE}'
    if ObjectHelper.isNotEmpty(originalActiveEnvironment) :
        SettingHelper.ACTIVE_ENVIRONMENT_VALUE = None
    originalEnvironmentVariables = {}
    if ObjectHelper.isDictionary(environmentVariables) :
        for key,value in environmentVariables.items() :
            originalEnvironmentVariables[key] = EnvironmentHelper.switch(key, value)
    SettingHelper.getActiveEnvironment()
    LogHelper.loadSettings()
    return originalEnvironmentVariables, originalActiveEnvironment

def resetEnvironmentVariables(environmentVariables, originalEnvironmentVariables, originalActiveEnvironment) :
    EnvironmentHelper.reset(environmentVariables, originalEnvironmentVariables)
    LogHelper.loadSettings()
    SettingHelper.ACTIVE_ENVIRONMENT_VALUE = originalActiveEnvironment
