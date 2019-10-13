import pytest
from media import cr2

def test_get_datetime():
    path = './fixtures/IMG_8610.CR2'
    dt = cr2.get_datetime(path)
    assert dt == '2015:12:24 12:01:32'

def test_is_equal():
    path1 = './fixtures/IMG_8610.CR2'
    path2 = './fixtures/IMG_8610.CR2'
    assert cr2.is_equal(path1,path2)

    path2 = './fixtures/IMG_5192.CR2'
    assert not cr2.is_equal(path1,path2)

