import os
import sys
import shutil
from struct import *
from media import cr2
from media import jpeg
from media import movie
import datetime
import logging

def get_info(dirpath,filename):
    path = os.path.join(dirpath,filename)
    size = os.path.getsize(path)
    if 0 == size:
        print(path + " is empty file")
        return ("TRUSH", dirpath, filename, None, 0)
    elif filename.startswith("."):
        print(path + " is hidden file")
        return ("TRUSH", dirpath, filename, None, size)
    elif filename.endswith(".JPG") or filename.endswith(".jpg"):
        datetime_string = jpeg.get_datetime(path)
        print("%s : %s" % (path, datetime_string))
        return ("JPG", dirpath, filename, datetime_string, size)
    elif filename.endswith(".CR2") or filename.endswith(".cr2"):
        datetime_string = cr2.getCR2DateTime(path)
        print("%s : %s" % (path, datetime_string))
        return ("RAW", dirpath, filename, datetime_string, size)
    elif filename.endswith(".MOV") or filename.endswith(".mov"):
        datetime_string = movie.get_created_time(path)
        print("%s : %s" % (path, datetime_string))
        return ("MOVIE", dirpath, filename, datetime_string, size)
    elif filename.endswith(".MP4") or filename.endswith(".mp4"):
        datetime_string = movie.get_created_time(path)
        print("%s : %s" % (path, datetime_string))
        return ("MOVIE", dirpath, filename, datetime_string, size)
    elif filename.endswith(".3GP") or filename.endswith(".3gp"):
        datetime_string = movie.get_created_time(path)
        print("%s : %s" % (path, datetime_string))
        return ("MOVIE", dirpath, filename, datetime_string, size)
    else:
        ot = os.stat(path).st_ctime
        dt = datetime.datetime.fromtimestamp(ot)
        datetime_string = dt.strftime("%Y:%m:%d %H:%M:%S")
        print("%s : %s" % (path, datetime_string))
        return ("OTHER", dirpath, filename, datetime_string, size)

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
        src_path = os.path.join(dirpath, filename)
        size = os.path.getsize(src_path)
        if os.path.isdir(src_path):
            yield from list_files(src_path)
        else:
            yield get_info(dirpath, filename)

def move_to_proper_dir(dst, ftype, dirpath, filename, datetime_string, size, overwrite):
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
    size: long
        ファイルサイズ    
    overwrite: boolean
        上書きする場合はTrue

    """
    src_path = os.path.join(dirpath, filename)
    dest_dir= dst
    if datetime_string is None:
        dest_dir= os.path.join(dst,ftype)
    else:        
        [d,t] = datetime_string.split()
        [yyyy,mm,dd] = d.split(":")
        dest_dir= os.path.join(dst, ftype)
        dest_dir= os.path.join(dest_dir, yyyy)
        dest_dir= os.path.join(dest_dir, mm)
    dest_path = os.path.join(dest_dir,filename)
    print(dest_dir)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    if not os.path.exists(dest_path) or overwrite:
        logging.info("%s:%s", src_path, dest_path)
        shutil.copy(src_path,dest_path)
    else:
        (dftype, ddirpath, dfilename, ddatetime_string, dsize) = get_info(dest_dir,filename)
        if filename==dfilename and datetime_string==ddatetime_string and size==dsize:
            print("%s : same file exists" % src_path)
        else:
            elms = filename.split(".")
            extension = elms.pop((len(elms)-1))
            basename = ".".join(elms)
            for num in range(1, 99):
                fn = "%s(%s).%s" % (basename, num, extension)
                dpf = os.path.join(dest_dir, fn)
                if not os.path.exists(dpf):
                    logging.info("%s:%s", src_path, dpf)
                    shutil.copy(src_path,dpf)
                    break

def main():
    """
    メイン関数
    第一引数に元フォルダ、第二引数に異動先フォルダのパス文字列を渡して実行する
    """
    dt_now = datetime.datetime.now()
    dt_log = dt_now.strftime("%Y-%m-%d-%H%M%S")
    logging.basicConfig(filename='info-%s.log'%dt_log, level=logging.DEBUG)

    args = sys.argv
    if 3 <= len(args):
        src = args[1]
        dst = args[2]
        overwrite = False
        if 4 <= len(args):
            opt = args[3]
            if "--force" == opt:
                overwrite = True
        logging.info('src = %s', src)
        logging.info('dst = %s', dst)
        print("src="+ src)
        print("dst="+ dst)
        if os.path.isdir(src) and os.path.isdir(dst):
            for (ftype, dirpath, filename, datetime_string, size) in list_files(args[1]):
                move_to_proper_dir(dst, ftype, dirpath, filename, datetime_string, size, overwrite)
        else:
            logging.info(src + " or " + dst + " is not a folder")
            print(src + " or " + dst + " is not a folder")
    else:
        print("src and dst is required!")
        logging.info("src and dst is required!")

if __name__ == '__main__':
    main()

