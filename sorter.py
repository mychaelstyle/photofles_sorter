import os
import sys
import shutil
from struct import *
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_from_cr2buf( buffer, ifd_offset ):
    (num_of_entries,) = unpack_from('H', buffer, ifd_offset)
    print("ifd #0 contains %d entries"%num_of_entries)
    # Work out where the date time is stored
    datetime_offset = -1
    for entry_num in range(0,num_of_entries-1):
        (tag_id, tag_type, num_of_value, value) = unpack_from('HHLL', buffer, ifd_offset+2+entry_num*12)
        print("%s : %s : %s : %s " % (tag_id, tag_type, num_of_value, value))
        #if tag_id == 0x0132:
        if tag_id == 306:
            datetime_offset = value
    return datetime_offset

def get_exif_from_cr2(filepath):
    with open(filepath, "rb") as f:
        buffer = f.read(1024)
        datetime_offset = get_exif_from_cr2buf(buffer, 0x10)
        print("offset = %s" % datetime_offset)
        return unpack_from(20*'s', buffer, datetime_offset)

def get_exif(img):
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

def list_files(dirpath,func):
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
        path = os.path.join(dirpath, filename)
        if filename.startswith("._"):
            print(path + " is hidden file")
        elif os.path.isdir(path):
            list_files(path,func)
        else:
            try:
                img = Image.open(path)
                datetimeinfo = func(img)
                yield (dirpath,filename,datetimeinfo)
                img.close()
            except:
                yield (dirpath,filename,None)

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
            for taginfo in list_files(args[1],get_exif):
                print(taginfo)
                move_to_proper_dir(taginfo,dst)
        else:
            print(src + " or " + dst + " is not a folder")
    else:
        print("src and dst is required!")

if __name__ == '__main__':
    #main()
    dt = get_exif_from_cr2('/Volumes/HD-MN2017/JPEGS/2014/12/IMG_4437.CR2')
    print(dt)

