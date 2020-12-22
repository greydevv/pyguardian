from pyguardian import guard

@guard(bool, int)
def foo(a, b):
	pass

@guard(bool, (int, float))
def foo_multi(a, b):
	pass

@guard(bool, int)
def bar(a, *args):
	pass

@guard(bool, (int, float))
def bar_multi(a, *args):
	pass

@guard(int, str)
def baz(a, **kwargs):
	pass

@guard(bool, (int, float))
def baz_multi(a, **kwargs):
	pass

@guard(int, str)
def qux(*args, **kwargs):
	pass

@guard((int, float), (bool, str))
def qux_multi(*args, **kwargs):
	pass

def test_foo():
	assert foo(True, 1) == None

def test_foo_multi():
	assert foo_multi(True, 1.2) == None

def test_bar():
	assert bar(True, 1, 2, 3, 4, 5) == None

def test_bar_multi():
	assert bar_multi(True, 1, 2, 3.4, 4, 5.6) == None

def test_baz():
	assert baz(1, x="Hello", y="World") == None

def test_baz_multi():
	assert baz_multi(True, x=1, y=2.3, z=3) == None

def test_qux():
	assert qux(1, 2, 3, x="Hello", y="World") == None

def test_qux_multi():
	assert qux_multi(1, 2.3, 4, 5.6, x=True, y="Hello") == None