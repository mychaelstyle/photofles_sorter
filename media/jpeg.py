from PIL import Image
from PIL.ExifTags import TAGS

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
    exif = img._getexif()

    try:
        for id,val in exif.items():
            tg = TAGS.get(id,id)
            if tg == "DateTimeOriginal":
                return val
    except AttributeError:
        return None

    return None

def get_datetime(path):
    try:
        img = Image.open(path)
        datetimeinfo = get_datetime_from_image(img)
        img.close()
        return datetimeinfo
    except:
        return None


