import subprocess
import os

# FFPROBEへのパス
FFPROBE = "/usr/local/bin/ffprobe"
# 撮影日時の項目名文字列
CREATED_DATETIME = "creation_time"

def get_info_strings(path):
    """
    ffprobeを実行して結果文字列をチャプター情報も含めて取得

    Parameters
    ----------
    path : string
        対象の動画ファイルパス

    Returns
    -------
    string
        ffprobeの実行結果文字列、ファイルが存在しなかった場合はNone。
    """
    if not os.path.exists(path):
        return None
    proc = subprocess.run([FFPROBE,"-show_chapters","-hide_banner",path],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE,
            encoding = "utf8", errors='ignore')
    response = proc.stdout+"\n"+(proc.stderr)
    strings = ""
    for line in response.splitlines():
        if line.startswith("Input ") or line.startswith("Unsupported codec"):
            continue
        else:
            strings = strings + "\n" + line
    return strings.strip()

def get_datetime(path):
    """
    指定の動画ファイルの撮影日時文字列を取得

    Parameters
    ----------
    path : string
        対象の動画ファイルパス

    Returns
    -------
    string
        撮影日時文字列(EXIF情報のフォーマットに合わせたフォーマット)
    """
    response = get_info_strings(path)
    if response is None:
        return None
    for line in response.splitlines():
        if CREATED_DATETIME in line:
            str = line.strip().replace(CREATED_DATETIME,"").strip().replace(": ","").strip().replace("T"," ").replace("Z","")
            return str.replace("-",":")

def is_equal(path1, path2):
    """
    指定の動画ファイルの撮影日時文字列を取得

    Parameters
    ----------
    path1 : string
        対象の動画ファイルパス
    path2 : string
        対象の動画ファイルパス

    Returns
    -------
    Boolean
        ２つのファイルのffprobe情報が一致したらTrue
    """
    if not os.path.exists(path1):
        raise FileNotFoundError("%s is not found." % path1)
    if not os.path.exists(path2):
        raise FileNotFoundError("%s is not found." % path2)

    res1 = get_info_strings(path1)
    res2 = get_info_strings(path2)

    if res1 is None or res2 is None:
        return False
    elif res1 == res2:
        if os.path.getsize(path1) == os.path.getsize(path2):
            return True
        else:
            return False
    else:
        return False

