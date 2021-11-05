from contextlib import nullcontext as no_exception
from pyguardian import guard
from pyguardian.errors import InvalidArgumentTypeError, UnknownKeywordArgumentWarning
import pytest

class TestClass:
    __test__ = False
    
    @guard(object, int, bool)
    def __init__(self, a, b):
        pass

    @guard(object, int)
    def tc_instancemethod(self, c):
        pass

    @staticmethod
    @guard(int)
    def tc_staticmethod(d):
        pass

    @classmethod
    @guard(object, int)
    def tc_classmethod(cls, e):
        pass

@pytest.fixture
def tc():
    return TestClass(1, True)

def test_initmethod():
    tc = TestClass(1, True)
    assert tc

def test_bad_initmethod():
    with pytest.raises(InvalidArgumentTypeError):
        tc = TestClass(1, "not an int")

def test_instancemethod(tc):
    tc.tc_instancemethod(1)

def test_bad_instancemethod(tc):
    with pytest.raises(InvalidArgumentTypeError):
        tc.tc_instancemethod("not an int")

def test_staticmethod():
    TestClass.tc_staticmethod(1)

def test_bad_staticmethod():
    with pytest.raises(InvalidArgumentTypeError):
        TestClass.tc_staticmethod("not an int")

def test_classmethod():
    TestClass.tc_classmethod(1)

def test_bad_classmethod():
    with pytest.raises(InvalidArgumentTypeError):
        TestClass.tc_classmethod("not an int")
