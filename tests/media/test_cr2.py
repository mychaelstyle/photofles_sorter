import pytest
from media import cr2

def test_get_datetime():
    path = './fixtures/IMG_8610.CR2'
    dt = cr2.get_datetime(path)
    assert dt == '2015:12:24 12:01:32'

