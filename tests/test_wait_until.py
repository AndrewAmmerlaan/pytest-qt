import pytest


def test_wait_until(qtbot, wait_4_ticks_callback, tick_counter):
    tick_counter.start(100)
    qtbot.waitUntil(wait_4_ticks_callback, 1000)
    assert tick_counter.ticks >= 4


def test_wait_until_timeout(qtbot, wait_4_ticks_callback, tick_counter):
    tick_counter.start(200)
    with pytest.raises(AssertionError):
        qtbot.waitUntil(wait_4_ticks_callback, 100)
    assert tick_counter.ticks < 4


def test_invalid_callback_return_value(qtbot):
    with pytest.raises(ValueError):
        qtbot.waitUntil(lambda: [])


def test_pep8_alias(qtbot):
    qtbot.wait_until


@pytest.fixture(params=['predicate', 'assert'])
def wait_4_ticks_callback(request, tick_counter):
    """Parametrized fixture which returns the two possible callback methods that can be
    passed to ``waitUntil``: predicate and assertion.
    """
    if request.param == 'predicate':
        return lambda: tick_counter.ticks >= 4
    else:
        def check_ticks():
            assert tick_counter.ticks >= 4
        return check_ticks


@pytest.yield_fixture
def tick_counter():
    """
    Returns an object which counts timer "ticks" periodically.
    """
    from pytestqt.qt_compat import QtCore

    class Counter:

        def __init__(self):
            self._ticks = 0
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self._tick)

        def start(self, ms):
            self.timer.start(ms)

        def _tick(self):
            self._ticks += 1

        @property
        def ticks(self):
            return self._ticks

    counter = Counter()
    yield counter
    counter.timer.stop()
