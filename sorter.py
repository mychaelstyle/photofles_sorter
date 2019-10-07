import os
import sys
import shutil
from struct import *
import cr2
import jpeg
import movie

def list_files(dirpath):
    """
    指定フォルダ以下のファイルを再帰的にリストアップし
    (dirname,filemane,funcの結果)のタプルをyieldで返す

    Parameters
    ----------
    dirname : string
        対象のフォルダパス
    func : def
        対象のファイルパスを処理して値を返す関数

    Returns
    -------
    fileinfo : tuple
        (ディレクトリパス, ファイル名, 関数実行結果)
    """
    for filename in os.listdir(dirpath):
        datetime_string = None
        path = os.path.join(dirpath, filename)
        if 0 == os.path.getsize(path):
            print(path + " is empty file")
        elif filename.startswith("._"):
            print(path + " is hidden file")
        elif os.path.isdir(path):
            list_files(path)
        else:
            if filename.endswith(".JPG") or filename.endswith(".jpg"):
                datetime_string = jpeg.get_datetime(path)
                print("%s : %s" % (path, datetime_string))
            elif filename.endswith(".CR2") or filename.endswith(".cr2"):
                datetime_string = cr2.getCR2DateTime(path)
                print("%s : %s" % (path, datetime_string))
            elif filename.endswith(".MOV") or filename.endswith(".mov"):
                datetime_string = movie.get_created_time(path)
                print("%s : %s" % (path, datetime_string))
            else:
                print("Not an image file : %s" % path)


def move_to_proper_dir(taginfo,dst):
    """
    ファイル情報と出力先フォルダパスを受け取って適切なフォルダにファイルを移動する

    Parameters
    ----------
    taginfo : tuple
        (フォルダパス,ファイル名,情報文字列)
    dst : string
        出力先フォルダパス
    """
    dirpath = taginfo[0]
    filename = taginfo[1]
    dt = taginfo[2]
    path = os.path.join(dirpath,filename)
    if dt is None:
        print( path + " is not exif file" )
        unknowndir = os.path.join(dirpath,"Unknown")
        if not os.path.exists(unknowndir):
            os.makedirs(unknowndir)
        shutil.copy(path,unknowndir)
    elif filename.endswith(".MOV") or filename.endswith(".mov"):
        [d,t] = dt.split()
        [yyyy,mm,dd] = d.split(":")
        dp = os.path.join(dst,"MOVIE")
        dp = os.path.join(dp,yyyy)
        dp = os.path.join(dp,mm)
        print(dp)
        if not os.path.exists(dp):
            os.makedirs(dp)
        shutil.copy(path,dp)
    else:
        [d,t] = dt.split()
        [yyyy,mm,dd] = d.split(":")
        dp = os.path.join(dst,"JPEG")
        dp = os.path.join(dp,yyyy)
        dp = os.path.join(dp,mm)
        print(dp)
        if not os.path.exists(dp):
            os.makedirs(dp)
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
            list_files(args[1])
#                move_to_proper_dir(taginfo,dst)
        else:
            print(src + " or " + dst + " is not a folder")
    else:
        print("src and dst is required!")

if __name__ == '__main__':
    main()
#    path = '/Volumes/HD-MN2017/JPEGS/2014/12/IMG_4437.CR2';
#    datetime_string = cr2.getCR2DateTime(path)
#    print(path + " : "+ datetime_string)

