import pytest

def test_is_equal(path1, path2):
    path1 = "IMG_4530.JPG"
    path2 = "IMG_5156.JPG"
    result = is_equal(path1,path2)
    assert False == result
    result = is_equal(path1,path1)
    assert result

def test_get_datetime(path):
    path1 = "IMG_4530.JPG"
    dt = get_datetime(path)
    assert dt == ''

def test():
    assert False

