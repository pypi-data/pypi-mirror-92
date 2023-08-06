import sys
import os
import os.path
import subprocess
from .platforms.Cplusplus import CplusplusDef
from .ProjectDef import ProjectDef
from .loader import loadHumonFile
from . import ansi

defs = {}
defaultDefs = {}     # {'Cplusplus': Def, ...}


def processTrove_1_0(defEntry, trove, version, ppArgs):
    defEntry['config'] = Config(version, ppArgs)
    print (len(trove.root))
    configNode = trove.root['config']
    if configNode:
        argsNode = configNode['args']
        if argsNode:
            defEntry['config'].preprocessArgs.append(argsNode.value)
        langsNode = configNode['platforms']
        for langNode in langsNode:
            if str(langNode.key).lower() == "c++":
                defEntry['config'].platforms['c++'] = langNode.objectify()
                cpp10.processCplusplus_1_0(defEntry['config'].platforms['c++'], langNode)
            else:
                raise ValueError(f'Boilermaker: Unsupported language {langNode.key}')

    # get types
    typesNode = trove.root['pods']
    
    defEntry['seenTypes'] = {}

    # record lang-agnostic types
    defEntry['pods'] = {}
    defEntry['pods']['data'] = typesNode.objectify()

    # TODO: for each lang, record lang-specific types
    defEntry['seenTypes']['c++'] = []
    defEntry['pods']['c++'] = {}
    cpp10.processCplusplusTypes_1_0(defEntry, typesNode)


def reportDecls(decls):
    # Get access to the global namespace
    global_namespace = declarations.get_global_namespace(decls)

    # Get access to the namespace
    ns = global_namespace.namespace("og")

    for decl in ns.declarations:
        print         (f"decl:                {decl}")
        print         (f"attributes:          {decl.attributes}")
        print         (f"decl_string:         {decl.decl_string}")
        print         (f"location:            {decl.location}")
        print         (f"name:                {decl.name}")
        print         (f"parent:              {decl.parent}")
        print         (f"partial_decl_string: {decl.partial_decl_string}")
        print         (f"partial_name:        {decl.partial_name}")
        print         (f"top_parent:          {decl.top_parent}")
        if hasattr(decl, "elaborated_type_specifier"):
            print     (f"elaborated_type_specifier:  {decl.elaborated_type_specifier}")
        if hasattr(decl, "values"):
            for value in decl.values:
                print (f"value:                      {value}")
        if hasattr(decl, "decl_type"):
            print     (f"decl_type:           {decl.decl_type}")
        if hasattr(decl, "is_artificial"):
            print     (f"is_artificial:       {decl.is_artificial}")
        print ("")
    
    #print (dir(ns.declarations[0]))
    #print (dir(ns.declarations[4]))


def findPod(defName, podName):
    if defName in defs:
        for defEntry in defs[defName]:
            for podKey, podValue in defEntry.pods.items():
                if podKey == podName:
                    return (podValue, defsEntry.config)
    
    return (None, None)


def loadDefaultPlatformDefs():
    global defaultDefs

    scriptDir = f'{os.path.dirname(os.path.realpath(__file__))}/platforms'
    for huPath in [f'{scriptDir}/{f}' for f in os.listdir(scriptDir) if os.path.isfile(f'{scriptDir}/{f}') and f.endswith('.hu')]:
        trove, version, platformName = loadHumonFile(huPath)
        if platformName == 'c++':
            defaultDefs[platformName] = (CplusplusDef(trove.root, huPath), trove, version)
        else:
            raise RuntimeError(f"Unsupported platform '{platformName}'")

    print(f'{ansi.dk_blue_fg}Default defs: {ansi.lt_blue_fg}{defaultDefs}{ansi.all_off}')


def loadProjectDef(defsPath):
    projectDef = ProjectDef(defsPath, defaultDefs)
    print(f'{ansi.dk_blue_fg}Project def: {ansi.lt_blue_fg}{projectDef}{ansi.all_off}')
    return projectDef


def main():
    defFile = None
    troves = []
    for i, arg in enumerate(sys.argv[1:]):
        defFile = arg
    
    loadDefaultPlatformDefs()

    if defFile:
        projectDef = loadProjectDef(os.path.realpath(defFile))
        projectDef.generateCode()
