from typing import List
from box import Box
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.container.ContainerInterface import ContainerInterface
from injecta.service.Service import Service
from injecta.service.ServiceAlias import ServiceAlias

class Bundle:

    def getConfigFiles(self):
        return ['config.yaml']

    def getCompilerPasses(self) -> List[CompilerPassInterface]:
        return []

    def modifyRawConfig(self, rawConfig: dict) -> dict:
        return rawConfig

    def modifyServices(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box): # pylint: disable = unused-argument
        return services, aliases

    def modifyParameters(self, parameters: Box) -> Box:
        return parameters

    def boot(self, container: ContainerInterface):
        pass
