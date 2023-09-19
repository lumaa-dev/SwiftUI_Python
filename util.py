def removeSlash(path: str):
    '''Removes the first slash in file/directory paths'''
    if path.startswith("/"):
        return path.replace("/", "", 1)
    else:
        return path