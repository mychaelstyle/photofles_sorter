import os

def get_info(dirpath,filename):
    """
    ファイルの情報に撮影日時の情報を付与して取得します。

    Parameters
    ----------
    dirpath : string
        対象ディレクトリパス
    filename : string
        対象ファイル名
    """
    path = os.path.join(dirpath,filename)
    fnlower = filename.lower()
    if os.path.exists(path):
        size = os.path.getsize(path)
        if 0 == size:
            return ("TRUSH", dirpath, filename, None, 0)
        elif filename.startswith("."):
            return ("TRUSH", dirpath, filename, None, size)
        elif fnlower.endswith(".jpg") or fnlower.endswith(".jpeg"):
            datetime_string = jpeg.get_datetime(path)
            return ("JPG", dirpath, filename, datetime_string, size)
        elif fnlower.endswith(".cr2"):
            datetime_string = cr2.getCR2DateTime(path)
            return ("RAW", dirpath, filename, datetime_string, size)
        elif fnlower.endswith(".mov"):
            datetime_string = movie.get_created_time(path)
            return ("MOVIE", dirpath, filename, datetime_string, size)
        elif fnlower.endswith(".mp4"):
            datetime_string = movie.get_created_time(path)
            return ("MOVIE", dirpath, filename, datetime_string, size)
        elif fnlower.endswith(".3gp"):
            datetime_string = movie.get_created_time(path)
            return ("MOVIE", dirpath, filename, datetime_string, size)
        else:
            #ot = os.stat(path).st_ctime
            #dt = datetime.datetime.fromtimestamp(ot)
            #datetime_string = dt.strftime("%Y:%m:%d %H:%M:%S")
            return ("OTHER", dirpath, filename, None, size)
    return (None, None, None, None, None)


