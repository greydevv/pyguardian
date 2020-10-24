from pyguard import guard
from pyvalid import accepts
@accepts(int, int, int, int)
def sumall(a,b,c, *args, **kwargs):
	return sum([a,b,c])


sumall(1, 2, 3, 4, 5, six=6, seven=7)



# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/greysonDEV/pyguard.git
# git push -u origin main