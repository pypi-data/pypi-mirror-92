
def TrueToObs(X_true, X_err):
    import numpy as np
    return X_true + np.random.normal(0,1,len(X_true)) * X_err

def Mags_to_distance(absmag, appmag, Coef_extinction, Dist_min, Dist_max, n_mock_dist, ll, bb):
    import numpy as np
    from dustmaps.bayestar import BayestarQuery
    bayestar = BayestarQuery(version='bayestar2019')
    from astropy.coordinates import SkyCoord
    import astropy.units as units
    mock_dist = np.linspace(Dist_min, Dist_max, n_mock_dist)
    mock_ll = np.zeros_like(mock_dist) + ll
    mock_bb = np.zeros_like(mock_dist) + bb
    coords = SkyCoord(mock_ll * units.deg, mock_bb * units.deg,
                      distance=mock_dist * units.kpc, frame='galactic')
    ebv = bayestar(coords, mode="median")
    A_mag = ebv * Coef_extinction
    mock_absmag = appmag - A_mag - 5*np.log10(mock_dist*100)
    ind_min = np.argmin(np.abs(mock_absmag - absmag))
    return mock_dist[ind_min], mock_absmag[ind_min], ebv[ind_min]
