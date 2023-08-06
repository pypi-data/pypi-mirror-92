import sys
def getOSPlatform():
    platforms={"win32":"Windows","darwin":"Mac OS X","linux":"Linux","linux2":"Android"}
    return platforms[sys.platform]