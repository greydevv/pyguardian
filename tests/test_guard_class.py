from pyguardian import guard
import pytest

class TestClass:
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

def test_testclass_initmethod():
	# this function must be manually tested because pytest cannot collect classes with __init__ methods
	tc = TestClass(1, True)

def test_testclass_instancemethod():
	tc = TestClass(1, True)
	tc.tc_instancemethod(1)

def test_testclass_staticmethod():
	TestClass.tc_staticmethod(1)

def test_testclass_classmethod():
	TestClass.tc_classmethod(1)