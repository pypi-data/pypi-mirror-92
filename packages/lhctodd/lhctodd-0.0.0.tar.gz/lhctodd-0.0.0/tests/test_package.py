import lhctodd as m


def test_version():
    assert m.__version__

def test_data():
    try:
        m.list()
    except:
        raise RuntimeError('Failed to fetch data from database')
