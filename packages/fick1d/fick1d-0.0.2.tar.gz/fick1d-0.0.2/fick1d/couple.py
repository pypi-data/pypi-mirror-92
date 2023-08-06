from numpy import exp,pi,sin,array,linspace, zeros, sqrt
from scipy.special import erf


def couple(T, D, Xlow, Xhi, cb,  xstep = 1000):
    ''' 
    T :list ints of times to sample
    Xlow: x start
    Xhi: x end
    cb: 
    D: Diffusivity 
    xstep: step size for x range
    yoff: 
    '''
    total = zeros((len(T), xstep))
    for count_t,t in enumerate(T):
        if t == 0:
            middle = int(xstep/2) - 1
            total[0,0:middle] = 0
            total[0,middle:] = cb
        else:
            for count_x,x in enumerate(linspace(Xlow,Xhi,xstep)):
                total[count_t,count_x] = (cb/2)*(1+erf(x/sqrt(4*D*t)))
    return total
