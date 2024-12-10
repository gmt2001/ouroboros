from inspect import getframeinfo, currentframe
from logging import getLogger
from os.path import dirname, abspath
from pathlib import Path

def get_exec_dir() -> str:
    """
    Returns the absolute path to the directory of this script, without trailing slash
    """
    filename = getframeinfo(currentframe()).filename
    path = dirname(abspath(filename))
    if path.endswith('/'):
        path = path[:-1]
    return path

def run_hook(hookname:str, myglobals:dict|None=None, mylocals:dict|None=None):
    """
    Looks for python scripts in the `hooks/hookname` sub-directory, relative to the location of this script, and executes them

    `myglobals` will be updated (and created, if None) with `__file__` set to the hook script and `__name__` to `__main__`

    Args:
        hookname (str): The name of the hook sub-directory to search
        myglobals (dict|None) : An optional dict of data made available under globals()
        mylocals (dict|None) : An optional dict of data made available under locals()
    """
    try :
        pathlist = Path(get_exec_dir() + '/hooks/' + hookname).rglob('*.py')
    except:
        getLogger().error("An error was raised while scanning the directory for hook %s", hookname, exc_info=True)
        return
    for path in pathlist:
        execfile(str(path), myglobals, mylocals)

# Copied from https://stackoverflow.com/a/41658338
def execfile(filepath:str, myglobals:dict|None=None, mylocals:dict|None=None):
    """
    Compiles and executes a python script with compile() and exec()

    Unhandled raised errors will be caught and sent to the logger

    `myglobals` will be updated (and created, if None) with `__file__` set to the hook script and `__name__` to `__main__`

    Args:
        filename (str): The path to the file to execute
        myglobals (dict|None) : An optional dict of data made available under globals()
        mylocals (dict|None) : An optional dict of data made available under locals()
    """
    if myglobals is None:
        myglobals = {}
    myglobals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    try :
        with open(filepath, 'rb') as file:
            try:
                exec(compile(file.read(), filepath, 'exec'), myglobals, mylocals)
            except:
                getLogger().error("An error was raised while executing hook script %s", filepath, exc_info=True)
    except:
        getLogger().error("An error was raised while reading hook script %s", filepath, exc_info=True)

def isContainerNetwork(container) -> bool:
    """
    Returns `True` if the network type of the provided container dict is "container"
    """
    parts = container.attrs['HostConfig']['NetworkMode'].split(':')
    return len(parts) > 1 and parts[0] == 'container'

def set_properties(old, new, self_name:str|None=None) -> dict:
    """
    Cretates a configuration dict for a new container, based on the configuration of the old container

    Args:
        old: The old container
        new: The new image (unused)
        self_name (str|None): The name of the new container; `None` to use the old container name

    Returns:
        dict: The new configuration
    """
    properties = {
        'name': self_name if self_name else old.name,
        'hostname': '' if isContainerNetwork(old) else old.attrs['Config']['Hostname'],
        'user': old.attrs['Config']['User'],
        'detach': True,
        'domainname': old.attrs['Config']['Domainname'],
        'tty': old.attrs['Config']['Tty'],
        'ports': None if isContainerNetwork(old) or not old.attrs['Config'].get('ExposedPorts') else [
            (p.split('/')[0], p.split('/')[1]) for p in old.attrs['Config']['ExposedPorts'].keys()
        ],
        'volumes': None if not old.attrs['Config'].get('Volumes') else [
            v for v in old.attrs['Config']['Volumes'].keys()
        ],
        'working_dir': old.attrs['Config']['WorkingDir'],
        'image': old.attrs['Config']['Image'],
        'command': old.attrs['Config']['Cmd'],
        'host_config': old.attrs['HostConfig'],
        'labels': old.attrs['Config']['Labels'],
        'entrypoint': old.attrs['Config']['Entrypoint'],
        'environment': old.attrs['Config']['Env'],
        'healthcheck': old.attrs['Config'].get('Healthcheck', None)
    }

    return properties


def remove_sha_prefix(digest:str) -> str:
    """
    Utility function to strip the `sha256:` prefix from a digest
    """
    if digest.startswith("sha256:"):
        return digest[7:]
    return digest


def get_digest(image) -> str:
    """
    Utility to locate the digest of an image and return it
    """
    digest = image.attrs.get(
            "Descriptor", {}
        ).get("digest") or image.attrs.get(
            "RepoDigests"
        )[0].split('@')[1] or image.id
    return remove_sha_prefix(digest)
