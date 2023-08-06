# this is the file containing the functions for converting the coordinates
# ----------------------------------------------------------------------------
def Correct_PM_From_Solar_Motion(ra, dec, pmra, pmdec, dist, degree=True, kpc=True,
                                 radec=True, X_Sun=8.34, UVW_Sun=[11.1, 12.24, 7.25], V_LSR=232):
    """
    This is used to correct the proper motions from the solar motion,
    the default values are
    X_Sun=8.34, UVW_Sun=[11.1, 12.24, 7.25], V_LSR=232
    return the corrected proper motion along l and b
    """
    import galpy.util.bovy_coords as gub
    import numpy as np
    # convert the proper motion along ra dec to those along l b
    if radec:
        llbb = gub.radec_to_lb(ra, dec, degree=True)
        ll = llbb[:, 0]
        bb = llbb[:, 1]
        pmllbb = gub.pmrapmdec_to_pmllpmbb(pmra, pmdec, ra, dec, degree=True)
        pmll = pmllbb[:, 0]
        pmbb = pmllbb[:, 1]
    else:
        ll = ra * 1.
        bb = dec * 1.
        pmll = pmra * 1.
        pmbb = pmdec * 1.

    rvpm = gub.vxvyvz_to_vrpmllpmbb(dist * 0 - UVW_Sun[0], dist * 0 - (V_LSR + UVW_Sun[1]), dist * 0 - UVW_Sun[2],
                                    ll, bb, dist, XYZ=False, degree=True)
    pmlMC = pmll[:, 0] - rvpm[:, 1]
    pmbMC = pmbb[:, 1] - rvpm[:, 2]
    pmradecMC = gub.pmllpmbb_to_pmrapmdec(pmlMC, pmbMC, ll, bb, degree=True)
    return pmlMC, pmbMC, pmradecMC[:, 0], pmradecMC[:, 1]


def to_sag_coord(ra, dec, degree=True):
    import math as m
    import numpy as np
    # -------------------------------
    n = len(ra)
    if degree:
        ra_tmp = ra * m.pi / 180
        dec_tmp = dec * m.pi / 180
    else:
        ra_tmp = ra * 1.0
        dec_tmp = dec * 1.0
    # conversion matrix
    a11, a12, a13 = -0.93595354, -0.31910658, 0.14886895
    a21, a22, a23 = 0.21215555, -0.84846291, -0.48487186
    b11, b12, b13 = 0.28103559, -0.42223415, 0.86182209

    sag_lam = np.arctan2(a11 * np.cos(ra_tmp) * np.cos(dec_tmp) +
                         a12 * np.sin(ra_tmp) * np.cos(dec_tmp) +
                         a13 * np.sin(dec_tmp),
                         a21 * np.cos(ra_tmp) * np.cos(dec_tmp) +
                         a22 * np.sin(ra_tmp) * np.cos(dec_tmp) +
                         a23 * np.sin(dec_tmp))
    sag_bet = np.arcsin(b11 * np.cos(ra_tmp) * np.cos(dec_tmp) +
                        b12 * np.sin(ra_tmp) * np.cos(dec_tmp) +
                        b13 * np.sin(dec_tmp))

    sag_coo = np.zeros((n, 2))
    if degree:
        sag_coo[:, 0] = sag_lam * 180 / m.pi
        sag_coo[:, 1] = sag_bet * 180 / m.pi
    else:
        sag_coo[:, 0] = sag_lam
        sag_coo[:, 1] = sag_bet
    return sag_coo


def sag_to_radec(lam, bet, degree=True):
    # """ this code is done according to
    #     the conversion by Belokurov et al 2014 437 116
    #     here arctan2 returns angle from -180 to 180                             """
    import numpy as np
    import math as m
    if degree:
        lam_tmp = lam * m.pi / 180
        bet_tmp = bet * m.pi / 180
    else:
        lam_tmp = lam
        bet_tmp = bet

    a11, a12, a13 = -0.84846291, -0.31910658, -0.42223415
    a21, a22, a23 = 0.21215555, -0.93595354, 0.28103559
    b11, b12, b13 = -0.48487186, 0.14886895, 0.86182209
    radec = np.zeros((len(lam), 2))
    radec[:, 0] = np.arctan2(a11 * np.cos(lam_tmp) * np.cos(bet_tmp) +
                             a12 * np.sin(lam_tmp) * np.cos(bet_tmp) +
                             a13 * np.sin(bet_tmp),
                             a21 * np.cos(lam_tmp) * np.cos(bet_tmp) +
                             a22 * np.sin(lam_tmp) * np.cos(bet_tmp) +
                             a23 * np.sin(bet_tmp))
    radec[:, 1] = np.arcsin(b11 * np.cos(lam_tmp) * np.cos(bet_tmp) +
                            b12 * np.sin(lam_tmp) * np.cos(bet_tmp) +
                            b13 * np.sin(bet_tmp))
    if degree:
        return radec * 180 / m.pi
    else:
        return radec
