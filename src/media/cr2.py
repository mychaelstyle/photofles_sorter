from struct import *
import subprocess
import os

EXIFTOOL = "/usr/local/bin/exiftool"
LABEL_DATETIME = "Date/Time Original"

def get_info_strings(path):
    """
    exiftoolを実行して結果文字列をチャプター情報も含めて取得

    Parameters
    ----------
    path : string
        対象の写真ファイルパス

    Returns
    -------
    string
        exiftoolの実行結果文字列、ファイルが存在しなかった場合はNone。
    """
    if not os.path.exists(path):
        return None
    proc = subprocess.run([EXIFTOOL,path],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE,
            encoding = "utf8", errors='ignore')
    response = proc.stdout+"\n"+(proc.stderr)
    return response.strip()

def get_exif_tag_value(path, tag):
    strings = get_info_strings(path)
    if strings is None:
        return None
    for line in strings.splitlines():
        if line.startswith(tag):
            line = line.strip()
            cpos = line.find(':')
            if cpos >= 0:
                line = line[(cpos+1):]
                return line.strip()
            else:
                return None

def get_exif_dict(path):
    strings = get_info_strings(path)
    exifdict = {}
    if strings is None:
        return None
    for line in strings.splitlines():
        if line.strip().startswith("File ") or line.strip().startswith("Directory "):
            continue
        else:
            cpos = line.find(':')
            if cpos >= 0:
                name = line[:cpos].strip()
                val  = line[(cpos+1):].strip()
                exifdict[name] = val
    return exifdict

def get_datetime(path):
    if 0 == os.path.getsize(path):
        return None
    return get_exif_tag_value(path, LABEL_DATETIME)

def is_equal(path1, path2):
    size1 = os.path.getsize(path1)
    size2 = os.path.getsize(path2)
    if not size1 == size2:
        return False
    elif 0 == size1 and 0 == size2:
        return True
    else:
        res1 = get_exif_dict(path1)
        res2 = get_exif_dict(path2)
        for name in res1:
            if not name in res2:
                return False
            if not res1[name] == res2[name]:
                return False
        return True
    return False

