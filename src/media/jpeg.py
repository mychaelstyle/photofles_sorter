from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_items(img):
    """
    Parameters
    ----------
    img : Image

    Returns
    ----------
    exif_items : dict
    """
    items = {}
    exif = img._getexif()
    for id,val in exif.items():
        tg = TAGS.get(id,id)
        items[tg] = val
    return items

def get_datetime_from_image(img):
    """
    指定のイメージオブジェクトのexif情報DateTimeOriginalを返す

    Parameters
    ----------
    img : Image
        対象のイメージオブジェクト

    Returns
    -------
    datetimeoriginal : string
        EXIF情報のDateTimeOriginal文字列
    """
    items = get_exif_items(img)
    return items["DateTimeOriginal"]

def get_datetime(path):
    try:
        img = Image.open(path)
        datetimeinfo = get_datetime_from_image(img)
        img.close()
        return datetimeinfo
    except:
        return None

def is_equal(path1, path2):
    img1 = Image.open(path1)
    img2 = Image.open(path2)
    items1 = get_exif_items(img1)
    items2 = get_exif_items(img2)
    if not len(items1) == len(items2):
        return False

    for key in items1:
        val = items[key]
        if not key in items2.keys():
            return False
        if not val == items2[key]:
            return False

    return True

