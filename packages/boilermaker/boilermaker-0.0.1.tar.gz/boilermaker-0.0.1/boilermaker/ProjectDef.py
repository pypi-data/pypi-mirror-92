from humon import humon, enums as humonEnums
from .loader import loadHumonFile
from .platformEnums.enums import Enums
from .platforms.Cplusplus import CplusplusDef
from .platformEnums.Cplusplus import CplusplusEnums

class ProjectDef:
    def __init__(self, path, platformDefaultDefs):
        '''Make a ProjectDef. platformDefaultDefs should be a dict of str:PlatformDef.'''
        self.path = path
        self.trove, self.version, _ = loadHumonFile(path)
        self.enums = Enums()
        defsNode = self.trove.root['defs']
        if defsNode:
            for platformNode in defsNode:
                platformName = platformNode.key
                if platformName == 'c++':
                    platformSources = [pd.value for pd in platformNode['sources']]
                    scanner = CplusplusEnums()
                    for platformSource in platformSources:
                        scanner.processHeader(platformSource, self.enums)
                    for enumNode in platformNode['attributes']:
                        for attribNode in enumNode:
                            enum = self.enums.getEnum(enumNode.key, platformName)
                            enum.setAttrib(attribNode.value)

        self.platformDefs = {}
        configNode = self.trove.root['platforms']
        for platformNode in configNode:
            platformName = platformNode.key
            if platformName == 'c++':
                backup = platformDefaultDefs.get(platformName, None)
                self.platformDefs[platformName] = CplusplusDef(platformNode, path, backup[0], self.getPodsNode())


    def getPlatformValue(self, platformName, nodeAddress):
        if platform in self.platformDefs:
            return self.platformDefs[platformName].getValue(nodeAddress)


    def getOutputPath(self, platformName, fileType = 'header', podName = None):
        val = self.getPlatformValue(platformName, f'outputFiles/{fileType}')
        if val:
            val = str(val).replace('*', podName)
        return val


    def getSetting(self, platformName, key):
        return self.getPlatformValue(platformName, f'settings/{key}')


    def getFeature(self, platformName, key):
        return self.getPlatformValue(platformName, f'features/{key}')


    def getPodsNode(self):
        podsNode = self.trove.getNodeByAddress(f'/pods')
        return podsNode
            

    def generateCode(self):
        for platformName, platform in self.platformDefs.items():
            platform.generateArtifacts(self.getPodsNode(), self.enums)
    