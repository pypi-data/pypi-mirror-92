#%% this is used to mock the catalog of the MW
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as units
from dustmaps.bayestar import BayestarQuery
bayestar = BayestarQuery(version="bayestar2019")

def mock_disk_R(a, b, N, Rmin = 10, Rmax = 40):
    """
    disk distribution follows: log(sigma) = a * R + b
    where a is related to the scale length L of the disk a = -1 / L
    b is the intercept
    N is the numbers of the mock stars
    Rmin/Rmax is the minimum/maximum galactocentric distance R, the default
    values are 10 and 30
    """
    def integrate_sig_disk(a, b, R):
        # integrating the distribution returns exp(a*R+b)/a
        return np.exp(a * R + b) / a

    def de_rnd_to_R(a, b, rnd, Rmin = 10):
        int_sig_min = integrate_sig_disk(a, b, Rmin)
        rnd_pp = int_sig_min + rnd
        return (np.log(rnd_pp * a) - b)/a

    int_sig_max = integrate_sig_disk(a, b, Rmax)
    int_sig_min = integrate_sig_disk(a, b, Rmin)
    tot_unnorm = int_sig_max - int_sig_min
    rnd_sig = np.random.uniform(0, 1, N) * tot_unnorm
    R = de_rnd_to_R(a, b, rnd_sig, Rmin)
    return R


def mock_disk_z(h, N):
    # sech(x) = 1/(e**x+e**(-x))
    # integrate sech(x)**2 = tanh(x) = sinh(x)/cosh(x)
    # sinh(x) = (e**x-e**(-x))/2
    # cosh(x) = (e**x+e**(-x))/2
    def integrate_sig_disk(h,z):
        return np.tanh(0.5*z/h)

    def de_rnd_to_Z(h,rnd):
        int_sig_min = integrate_sig_disk(h,10)
        rnd_pp = int_sig_min+rnd
        return 2*h*np.arctanh(rnd_pp)

    int_sig_max = integrate_sig_disk(h,0)
    int_sig_min = integrate_sig_disk(h,10)
    tot_unnorm  = int_sig_max-int_sig_min
    rnd_sig = np.random.uniform(0,1,N)*tot_unnorm
    Z = de_rnd_to_Z(h,rnd_sig)
    return Z

