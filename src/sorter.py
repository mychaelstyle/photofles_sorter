import os
import sys
import shutil
from struct import *
import media
from media import cr2
from media import jpeg
from media import movie
import datetime
import logging

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
        if os.path.isdir(src_path):
            yield from list_files(src_path)
        else:
            yield media.get_info(dirpath, filename)

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
    duplicated_dir = os.path.join(dst,"DUPLICATED")
    if datetime_string is None:
        logging.info("Skip:No timestamp:%s:", src_path)
        print("Skip:No timestamp:%s:" % src_path)
        return
    else:        
        [d,t] = datetime_string.split()
        [yyyy,mm,dd] = d.split(":")
        dest_dir= os.path.join(dest_dir, ftype)
        dest_dir= os.path.join(dest_dir, yyyy)
        dest_dir= os.path.join(dest_dir, mm)
        duplicated_dir= os.path.join(duplicated_dir, ftype)
        duplicated_dir= os.path.join(duplicated_dir, yyyy)
        duplicated_dir= os.path.join(duplicated_dir, mm)

    dest_path = os.path.join(dest_dir,filename)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    if not os.path.exists(dest_path) or overwrite:
        logging.info("Moved:done:%s:%s", src_path, dest_path)
        print("Moved:done:%s:%s" % (src_path,dest_path))
        shutil.move(src_path,dest_path)
    else:
        (dftype, ddirpath, dfilename, ddatetime_string, dsize) = media.get_info(dest_dir,filename)
        if filename==dfilename and datetime_string==ddatetime_string and size==dsize:
            dup_path = os.path.join(duplicated_dir,filename)
            if not os.path.exists(duplicated_dir):
                os.makedirs(duplicated_dir)
            if not os.path.exists(dup_path):
                logging.info("Duplicated:moved:%s:%s", src_path, dup_path)
                print("Duplicated:moved:%s:%s" % (src_path, dup_path))
                shutil.move(src_path,dup_path)
            else:
                elms = filename.split(".")
                extension = elms.pop((len(elms)-1))
                basename = ".".join(elms)
                for num in range(1, 99):
                    fn = "%s(%s).%s" % (basename, num, extension)
                    dpf = os.path.join(duplicated_dir, fn)
                    if not os.path.exists(dpf):
                        logging.info("Duplicated:moved:%s:%s", src_path, dpf)
                        print("Duplicated:moved:%s:%s" % (src_path,dpf))
                        shutil.move(src_path,dpf)
                        break
        else:
            elms = filename.split(".")
            extension = elms.pop((len(elms)-1))
            basename = ".".join(elms)
            for num in range(1, 99):
                fn = "%s(%s).%s" % (basename, num, extension)
                dpf = os.path.join(dest_dir, fn)
                if not os.path.exists(dpf):
                    logging.info("Moved:done:%s:%s", src_path, dpf)
                    print("Moved:done:%s:%s" % (src_path,dpf))
                    shutil.move(src_path,dpf)
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
                if not ftype is None:
                    move_to_proper_dir(dst, ftype, dirpath, filename, datetime_string, size, overwrite)
        else:
            print(src + " or " + dst + " is not a folder")
    else:
        print("src and dst is required!")

if __name__ == '__main__':
    main()

