from pyguard import guard
from pyvalid import accepts
@accepts(int, int, int, int)
def sumall(a,b,c, *args, **kwargs):
	return sum([a,b,c])


sumall(1, 2, 3, 4, 5, six=6, seven=7)
