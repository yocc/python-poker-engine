import sys, os

from pyglet import media, image

RESOURCE_IMAGE, RESOURCE_SOUND, RESOURCE_MUSIC = range(3)

RESOURCE_PATHS = { 
    RESOURCE_IMAGE: 'images', 
    RESOURCE_SOUND: 'sounds',
    RESOURCE_MUSIC: 'music'
}

def get_resource(type, filename):
    """return resource given type (e.g. RESOURCE_IMAGE) and filename"""

    frozen = getattr(sys, 'frozen', None)

    if frozen in ('windows_exe', 'console_exe'):
        res_dir = os.path.join(os.path.dirname(sys.executable), 'resources')
    elif frozen == 'macosx_app':
        res_dir = os.path.join(os.environ['RESOURCEPATH'], 'resources')
    else:
        res_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')

    path = os.path.join(res_dir, RESOURCE_PATHS[type], filename)

    if type == RESOURCE_IMAGE:
        return image.load(path)

    if type == RESOURCE_SOUND:
        return media.load(path, streaming=False)

    if type == RESOURCE_MUSIC:
        return media.load(path, streaming=True)

    assert False

def image_resource(file): 
    return get_resource(RESOURCE_IMAGE, file)

def sound_resource(file): 
    return get_resource(RESOURCE_SOUND, file)
