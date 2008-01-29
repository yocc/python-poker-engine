import sys, os

from pyglet import media, image

RES_IMAGE, RES_SOUND = range(2)
RES_PATHS = { RES_IMAGE: 'images', RES_SOUND: 'sounds' }

def res(type, filename):
    """return resource given type (e.g. RES_IMAGE) and filename"""
    frozen = getattr(sys, 'frozen', None)
    res_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
    if frozen in ('windows_exe', 'console_exe'):
        res_dir = os.path.join(os.path.dirname(sys.executable), 'resources')
    elif frozen == 'macosx_app':
        res_dir = os.path.join(os.environ['RESOURCEPATH'], 'resources')
    path = os.path.join(res_dir, RES_PATHS[type], filename)
    if type == RES_IMAGE:
        return image.load(path)
    if type == RES_SOUND:
        return media.load(path, streaming=False)
    assert False

def image_res(file): return res(RES_IMAGE, file)
def sound_res(file): return res(RES_SOUND, file)
