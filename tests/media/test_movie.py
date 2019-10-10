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

