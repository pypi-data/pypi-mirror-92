from pathlib import Path
from typing import List
from box import Box
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.config.ConfigLoader import ConfigLoader
from injecta.config.ConfigMerger import ConfigMerger
from injecta.service.Service import Service
from injecta.package.pathResolver import resolvePath
from injecta.service.ServiceAlias import ServiceAlias
from pyfonybundles.Bundle import Bundle

class BundleManager:

    def __init__(self, bundles: List[Bundle]):
        self.__bundles = bundles
        self.__configLoader = ConfigLoader()
        self.__configMerger = ConfigMerger()

    def getCompilerPasses(self) -> List[CompilerPassInterface]:
        compilerPasses = []

        for bundle in self.__bundles:
            compilerPasses += bundle.getCompilerPasses()

        return compilerPasses

    def getBundlesConfig(self) -> dict:
        config = dict()

        for bundle in self.__bundles:
            rootModuleName = bundle.__module__[:bundle.__module__.find('.')]
            configBasePath = resolvePath(rootModuleName) + '/_config'

            for configFileName in bundle.getConfigFiles():
                configFilePath = Path(configBasePath + '/' + configFileName)
                newConfig = self.__configLoader.load(configFilePath)

                config = self.__configMerger.merge(config, newConfig, False)

        return config

    def getProjectBundlesConfig(self, bundlesConfigsDir: str) -> dict:
        config = dict()

        for bundle in self.__bundles:
            rootPackageName = bundle.__module__[:bundle.__module__.find('.')]
            projectBundleConfigPath = Path(bundlesConfigsDir + '/' + rootPackageName + '.yaml')

            if projectBundleConfigPath.exists():
                projectBundleConfig = self.__configLoader.load(projectBundleConfigPath)

                config = self.__configMerger.merge(config, projectBundleConfig)

        return config

    def modifyRawConfig(self, rawConfig: dict) -> dict:
        for bundle in self.__bundles:
            rawConfig = bundle.modifyRawConfig(rawConfig)

        return rawConfig

    def modifyServices(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box):
        for bundle in self.__bundles:
            services, aliases = bundle.modifyServices(services, aliases, parameters)

        return services, aliases

    def modifyParameters(self, parameters: Box) -> Box:
        for bundle in self.__bundles:
            parameters = bundle.modifyParameters(parameters)

        return parameters
