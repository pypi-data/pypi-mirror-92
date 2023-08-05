import pypungi
import numpy as np

pp = pypungi.app()
pp.plot([1,2,3,4])


e = np.random.normal(0,1,[100,1])
x = np.arange(100).reshape([100,1])
y = 3*x + e
#model = ModelHub()
pp.model('ols',y,100*x)


