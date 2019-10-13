import pytest
from media import movie

def test_get_created_time():
    path = 'fixtures/IMG_6478.mov'
    dt = movie.get_datetime(path)
    assert not dt is None
    assert dt == '2016:10:29 12:09:15.000000'

    path = 'fixtures/150721_112157.3gp'
    dt = movie.get_datetime(path)
    assert not dt is None
    assert dt == '2015:07:21 02:22:12.000000'

    path = 'fixtures/IMG_8047.MOV'
    dt = movie.get_datetime(path)
    assert not dt is None
    assert dt == '2017:01:21 12:37:08.000000'

    path = 'fixtures/IMG_3788.mp4'
    dt = movie.get_datetime(path)
    assert not dt is None
    assert dt == '2015:12:14 03:25:08.000000'

    path = 'fixtures/IMG_0493.m4v'
    dt = movie.get_datetime(path)
    assert not dt is None
    assert dt == '2018:05:06 02:37:00.000000'

def test_is_equal():
    # 同じケース
    path1 = 'fixtures/IMG_6478.mov'
    path2 = 'fixtures/IMG_6478.mov'
    res = movie.is_equal(path1, path1)
    assert res
    # ファイル名だけ違うケース
    path1 = 'fixtures/IMG_8047.MOV'
    path2 = 'fixtures/IMG_8047(1).MOV'
    res = movie.is_equal(path1, path2)
    assert res
    # 違うケース
    path1 = 'fixtures/IMG_6478.mov'
    path2 = 'fixtures/IMG_8047.MOV'
    res = movie.is_equal(path1, path2)
    assert not res

