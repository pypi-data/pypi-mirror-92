
# class SingleStar
def Calc_Orbit(ra, dec, dist, pmra, pmdec, rv,t=None, PV_Sun=None, Potential=None):
    import numpy as np
    from astropy import units
    # from galpy.actionAngle import actionAngleStaeckel
    from galpy.orbit import Orbit
    # import galpy.util.bovy_conversion as bc
    from galpy.potential import MWPotential2014

    if PV_Sun is None:
        U_sun, V_sun, W_sun = 11.1, 12.24, 7.25
        X_sun = 8.3  # Reid et al 2014
        V_LSR = 232
    else:
        U_sun, V_sun, W_sun = PV_Sun[0:3]
        X_sun = PV_Sun[3]
        V_LSR = PV_Sun[4]
    print(X_sun,V_LSR,'---------------')
    if Potential is None:
        pot = MWPotential2014
    else:
        pot = Potential

    o = Orbit([ra, dec, dist, pmra, pmdec, rv],ro=X_sun, vo=V_LSR,radec=True, solarmotion='dehnen')
    if t is None:
        print("t is none")
        ts = np.linspace(0,10,1001)*units.Gyr
    else:
        ts = t*units.Gyr
    o.integrate(ts, pot=pot)
    return o, ts

