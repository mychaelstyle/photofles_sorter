import pytest
from media import jpeg as jpg

def test_is_equal():
    path1 = "./fixtures/IMG_4530.JPG"
    path2 = "./fixtures/IMG_5157.JPG"
    result = jpg.is_equal(path1,path2)
    assert False == result
    result = jpg.is_equal(path1,path1)
    assert result

def test_get_datetime():
    path = "fixtures/IMG_4530.JPG"
    dt = jpg.get_datetime(path)
    assert dt == '2014:11:03 14:24:46'

