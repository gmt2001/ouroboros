from inspect import getframeinfo, currentframe
from os.path import dirname, abspath
from pathlib import Path

def get_exec_dir():
    filename = getframeinfo(currentframe()).filename
    path = dirname(abspath(filename))
    if path.endswith('/'):
        path = path[:-1]
    return path

def run_hook(hookname, myglobals=None, mylocals=None):
    pathlist = Path(get_exec_dir() + '/hooks/' + hookname).rglob('*.py')
    for path in pathlist:
        execfile(str(path), myglobals, mylocals)

# Copied from https://stackoverflow.com/a/41658338
def execfile(filepath, myglobals=None, mylocals=None):
    if myglobals is None:
        myglobals = {}
    myglobals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), myglobals, mylocals)

def isContainerNetwork(container):
    parts = container.attrs['HostConfig']['NetworkMode'].split(':')
    return len(parts) > 1 and parts[0] == 'container'

def set_properties(old, new, self_name=None):
    """Store object for spawning new container in place of the one with outdated image"""
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


def remove_sha_prefix(digest):
    if digest.startswith("sha256:"):
        return digest[7:]
    return digest


def get_digest(image):
    digest = image.attrs.get(
            "Descriptor", {}
        ).get("digest") or image.attrs.get(
            "RepoDigests"
        )[0].split('@')[1] or image.id
    return remove_sha_prefix(digest)
