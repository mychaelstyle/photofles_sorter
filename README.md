# photofles_sorter
sort and arrangement jpeg photo files to YYYY/MM folder.

iPhone、デジカメで撮ったJPEG,MOV,CR2,3GPファイルが大量に入っているフォルダを指定すると、フォルダ内を再帰的に検索し、ファイルの撮影日時情報を取得できたファイルを年月ごとにフォルダを作成して振り分けます。

## Environment

- Python >= 3.7
- ffmpeg
- ffprove

## How to use

cloneしたらsetup.pyを実行

    python setup.py install

振り分けたい写真ファイルが入ったフォルダと出力先となるフォルダを指定して実行してください。

    python sorter.py [src folder path] [dest folder path]


