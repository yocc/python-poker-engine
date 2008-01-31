import sys, os

from pyglet import media, image, font

RESOURCE_IMAGE, RESOURCE_SOUND, RESOURCE_MUSIC, RESOURCE_FONT = range(4)

PATH_FOR_RESOURCE_TYPES = { 
    RESOURCE_IMAGE: 'images', 
    RESOURCE_SOUND: 'sounds',
    RESOURCE_MUSIC: 'music',
    RESOURCE_FONT:  'fonts'
}

def path_for_resource_type(type):
    """return path to directory containing resources of given type"""

    frozen = getattr(sys, 'frozen', None)

    if frozen in ('windows_exe', 'console_exe'):
        res_dir = os.path.join(os.path.dirname(sys.executable), 'resources')
    elif frozen == 'macosx_app':
        res_dir = os.path.join(os.environ['RESOURCEPATH'], 'resources')
    else:
        res_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')

    return os.path.join(res_dir, PATH_FOR_RESOURCE_TYPES[type])

def find_resource(type, filename):
    """return resource given type (e.g. RESOURCE_IMAGE) and filename"""

    path = os.path.join(path_for_resource_type(type), filename)

    if type == RESOURCE_IMAGE: return image.load(path)
    if type == RESOURCE_FONT:  return font.load(path)
    if type == RESOURCE_SOUND: return media.load(path, streaming=False)
    if type == RESOURCE_MUSIC: return media.load(path, streaming=True)

    assert False

def image_resource(file): 
    """returns a pyglet.image.AbstractImage"""
    return find_resource(RESOURCE_IMAGE, file)

def font_resource(file, size=12, **kwargs):  
    """returns a pyglet.font.Font"""
    return font.load(file, size, **kwargs)

def sound_resource(file): 
    """returns a pyglet.media.StaticSource"""
    return find_resource(RESOURCE_SOUND, file)

def music_resource(file): 
    """returns a pyglet.media.StreamingSource"""
    return find_resource(RESOURCE_MUSIC, file)

# add fonts directory to search path
font.add_directory(path_for_resource_type(RESOURCE_FONT))
