from humon import humon, enums as humonEnums
from . import ansi

def loadHumonFile(defsFile):
    '''Load a humon file and validate the version. Useful for defs files and default configs.'''
    trove = humon.Trove.fromFile(defsFile)

    if not trove.getTroveAnnotations(key="app", value="boma"):
        raise ValueError(f"input file {defsFile} is not a 'boma' file.")

    bomaVersion = (1, 0, 0)
    troveVersion = trove.getTroveAnnotations(key='boma-version')
    if troveVersion:
        bomaVersion = str(troveVersion).split(".")
        if len(bomaVersion) != 3:
            raise ValueError(f"input file {defsFile}: boma-version must be a three-component semver.")

    platformDef = None
    trovePlatformDef = trove.getTroveAnnotations(key='boma-platform')
    if trovePlatformDef:
        platformDef = str(trovePlatformDef)

    print (f"{ansi.dk_yellow_fg}Loaded humon file {ansi.lt_yellow_fg}{defsFile}{ansi.dk_yellow_fg}: version: {ansi.lt_yellow_fg}{bomaVersion}{ansi.all_off}")
    return (trove, bomaVersion, platformDef)
