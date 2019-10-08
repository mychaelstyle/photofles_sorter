import os
import sys
import shutil
from struct import *
import cr2
import jpeg
import movie
import datetime

def list_files(dirpath):
    """
    指定フォルダ以下のファイルを再帰的にリストアップし
    (filetype, dirpath, filemane, datetime_string)のタプルをyieldで返す

    Parameters
    ----------
    dirname : string
        対象のフォルダパス

    Returns
    -------
    fileinfo : tuple
        (ファイルタイプ文字列, ディレクトリパス, ファイル名, 撮影日時)
    """
    for filename in os.listdir(dirpath):
        datetime_string = None
        path = os.path.join(dirpath, filename)
        if 0 == os.path.getsize(path):
            print(path + " is empty file")
            yield ("EMPTY", dirpath, filename, None)
        elif filename.startswith("._"):
            print(path + " is hidden file")
            yield ("HIDDEN", dirpath, filename, None)
        elif os.path.isdir(path):
            yield from list_files(path)
        else:
            if filename.endswith(".JPG") or filename.endswith(".jpg"):
                datetime_string = jpeg.get_datetime(path)
                print("%s : %s" % (path, datetime_string))
                yield ("JPG", dirpath, filename, datetime_string)
            elif filename.endswith(".CR2") or filename.endswith(".cr2"):
                datetime_string = cr2.getCR2DateTime(path)
                print("%s : %s" % (path, datetime_string))
                yield ("RAW", dirpath, filename, datetime_string)
            elif filename.endswith(".MOV") or filename.endswith(".mov"):
                datetime_string = movie.get_created_time(path)
                print("%s : %s" % (path, datetime_string))
                yield ("MOVIE", dirpath, filename, datetime_string)
            elif filename.endswith(".MP4") or filename.endswith(".mp4"):
                datetime_string = movie.get_created_time(path)
                print("%s : %s" % (path, datetime_string))
                yield ("MOVIE", dirpath, filename, datetime_string)
            elif filename.endswith(".3GP") or filename.endswith(".3gp"):
                datetime_string = movie.get_created_time(path)
                print("%s : %s" % (path, datetime_string))
                yield ("MOVIE", dirpath, filename, datetime_string)
            else:
                ot = os.stat(path).st_ctime
                dt = datetime.datetime.fromtimestamp(ot)
                datetime_string = dt.strftime("%Y:%m:%d %H:%M:%S")
                print("%s : %s" % (path, datetime_string))
                yield ("OTHER", dirpath, filename, datetime_string)

def move_to_proper_dir(dst, ftype, dirpath, filename, datetime_string):
    """
    ファイル情報と出力先フォルダパスを受け取って適切なフォルダにファイルを移動する

    Parameters
    ----------
    dst: string
        出力対象のフォルダパス
    ftype: string
        ファイルタイプ
    dirpath: string
        移動元ファイルのディレクトリ
    filename: string
        移動元ファイル名
    datetime_string: string
        撮影日時文字列

    """
    [d,t] = datetime_string.split()
    [yyyy,mm,dd] = d.split(":")
    dp = os.path.join(dst, ftype)
    dp = os.path.join(dp, yyyy)
    dp = os.path.join(dp, mm)
    print(dp)
    if not os.path.exists(dp):
        os.makedirs(dp)
    path = os.path.join(dirpath, filename)
    shutil.copy(path,dp)

def main():
    """
    メイン関数
    第一引数に元フォルダ、第二引数に異動先フォルダのパス文字列を渡して実行する
    """
    args = sys.argv
    if 3 <= len(args):
        src = args[1]
        dst = args[2]
        print("src="+ src)
        print("dst="+ dst)
        if os.path.isdir(src) and os.path.isdir(dst):
            for (ftype, dirpath, filename, datetime_string) in list_files(args[1]):
                move_to_proper_dir(dst, ftype, dirpath, filename, datetime_string)
        else:
            print(src + " or " + dst + " is not a folder")
    else:
        print("src and dst is required!")

if __name__ == '__main__':
    main()

