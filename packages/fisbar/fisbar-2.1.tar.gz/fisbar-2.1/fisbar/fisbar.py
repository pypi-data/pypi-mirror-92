#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: november 2020 -*-
# -*- copyright: GH/IPHC 2020 -*-
# -*- file: fisbar.py -*-
# -*- purpose: -*-


'''
Defines the fisbar funciton


subroutine fisrot(A,Z,il,bfis,segs,elmax)

c    This subroutine returns the barrier height bfis, the ground-state
c    energy segs, in MeV, and the angular momentum at which the fission
c    barrier disappears,  Lmax,  in units of h-bar,
c    when called with integer arguments iz, the atomic number,
c    ia, the atomic mass number, and il, the angular momentum in units
c    of h-bar, (Planck's constant divided by 2*pi).
'''

from typing import Dict, Union
from math import log, exp, pi, cos, sin

import fisbar.tables as tables
from fisbar.lpoly import lpoly


def barfit(Z: int, A: int, il: int = 0) -> dict:
    'Unified call to the fisbar and momfit functions, return clean dict'
    return_dict = {
        'Z': Z, 'A': A, 'L': int(il),
        'bfis': float('NaN'),
        'elmax': float('NaN'),
        'egs': float('NaN'),
        'imin': float('NaN'),
        'imid': float('NaN'),
        'imax': float('NaN'),
    }
    try:
        fb = fisbar(Z, A, il)
        return_dict['bfis'] = fb.get('bfis', float('NaN'))
        return_dict['elmax'] = fb.get('elmaxc', float('NaN'))
        return_dict['egs'] = fb.get('egs', float('NaN'))
        mf = momfit(Z, A, il)
        return_dict['imin'] = mf.get('saimin', float('NaN'))
        return_dict['imid'] = mf.get('saimid', float('NaN'))
        return_dict['imax'] = mf.get('saimax', float('NaN'))
    except Exception as err:
        print(err)
    return return_dict


def fisbar(Z: int, A: int, il: int) -> dict:
    '''Returns a dictionarry woth the calculated bfis, egs and elmax'''
    out_dict: Dict[str, Union[str, float, int, bool]] = {
        'success': True,
        'Z': Z, 'A': A, 'L': il,
        'bfis': 0., 'elmax': 0., 'egs': 0.
    }
    try:
        assert 19 < Z < 111
        assert not (Z > 102 and il == 0)
    except AssertionError:
        out_dict['success'] = False
        out_dict['cause'] = "Parameters out of bound"
        return out_dict
    el: float = float(il)
    amin: float = 1.2 * Z + 0.01 * Z * Z
    amax: float = 5.8 * Z - 0.024 * Z * Z
    try:
        assert amin < A < amax
    except AssertionError:
        out_dict['success'] = False
        out_dict['cause'] = "Parameters out of bound"
        return out_dict
    aa: float = 2.5e-3 * A
    zz: float = 1.0e-2 * Z
    bfis0: float = 0.0
    pz = lpoly(zz, 7)
    pa = lpoly(aa, 7)
    for i in range(7):
        for j in range(7):
            bfis0 += tables.elzcof[j + i * 7] * pz[j] * pa[i]
    egs: float = 0.0
    segs: float = egs
    bfis: float = bfis0
    out_dict['bfis'] = bfis
    amin2: float = 1.4 * Z + 0.009 * Z * Z
    amax2: float = 20.0 + 3.0 * Z
    if ((A < amin2 - 5 or A > amax2 + 10) and il > 0):
        out_dict['success'] = False
        out_dict['cause'] = "Parameters out of bound"
        return out_dict
    el80: float = 0.0
    el20: float = 0.0
    elmax: float = 0.0
    for i in range(4):
        for j in range(5):
            el80 += tables.elmcof[j + i * 5] * pz[j] * pa[i]
            el20 += tables.emncof[j + i * 5] * pz[j] * pa[i]
    sel80 = float(el80)
    sel20 = float(el20)
    out_dict['sel80'] = sel80
    out_dict['sel20'] = sel20
    for i in range(5):
        for j in range(7):
            elmax += tables.emxcof[j + i * 7] * pz[j] * pa[i]
    selmax = elmax
    out_dict['elmax'] = selmax
    out_dict['elmaxc'] = elmaxc(Z, A)
    selmax = float(out_dict['elmaxc'])
    if il < 1:
        out_dict['exit'] = 'condition(il < 1)'
        return out_dict
    x = sel20 / selmax
    y = sel80 / selmax
    if el > sel20:
        aj = (-20.0 * x ** 5 + 25.0 * x ** 4 - 4.0) * (y - 1.0) ** 2 * y * y
        ak = (-20.0 * y ** 5 + 25.0 * y ** 4 - 1.0) * (x - 1.0) ** 2 * x * x
        q = 0.20 / ((y - x) * ((1.0 - x) * (1.0 - y) * x * y) ** 2)
        qa = q * (aj * y - ak * x)
        qb = -q * (aj * (2.0 * y + 1.0) - ak * (2.0 * x + 1.0))
        z = el / selmax
        a1 = 4.0 * z ** 5 - 5.0 * z ** 4 + 1.0
        a2 = qa * (2.0 * z + 1.0)
        bfis *= (a1 + (z - 1.0) * (a2 + qb * z) * z * z * (z - 1.0))
    else:
        q = 0.20 / (sel20 ** 2 * sel80 ** 2 * (sel20 - sel80))
        qa = q * (4.0 * sel80 ** 3 - sel20 ** 3)
        qb = -q * (4.0 * sel80 ** 2 - sel20 ** 2)
        bfis *= (1.0 + qa * el ** 2 + qb * el ** 3)
    if bfis <= 0.0:
        bfis = 0.0
        out_dict['found_bf_lower_than_0'] = True
    out_dict['bfis'] = bfis
    if el > selmax:
        bfis = 0.0
        out_dict['given_el_larger_than_elmax'] = True
    # c    Now calculate rotating ground-state energy
    ell = el / elmax
    if il == 1000:
        ell = 1.
    pl = lpoly(ell, 9)
    for k in range(5):
        for l in range(7):
            for m in range(5):
                egs += tables.egs[m + (l + k * 7) * 5] * pz[l] * pa[k] * pl[2 * m]
    segs = egs if egs >= 0. else 0.0
    out_dict['egs'] = segs
    return out_dict


def elmaxc(Z: int, A: int) -> float:
    '''
    Improved `elmax` routine from A. Sierk
c   This subroutine written February, 1994.
c   Updated constants and extended Z and A range of fit, May, 1996.
    '''
    xz: float = Z / 100.0
    xa: float = A / 320.0
    elmax = 0.0
    plz = lpoly(xz, 8)
    pla = lpoly(xa, 5)
    for iz in range(8):
        for ia in range(5):
            ib = ia + (5 * iz)
            elmax += tables.elmaxc_b[ib] * plz[iz] * pla[ia]
        # end for ia
    # end for iz
    return elmax


def momfit(Z: int, A: int, il: int) -> dict:
    '''
    This subroutine returns the three principal-axis moments of inertia
    '''
    out_dict: Dict[str, Union[str, float, int, bool]] = {
        'success': True,
        'Z': Z, 'A': A, 'L': il,
        'saimin': float('nan'), 'saimid': float('nan'), 'saimax': float('nan')
    }
    if not (19 < Z <= 101):
        out_dict['success'] = False
        out_dict['reason'] = "Z out of limits"
        return out_dict
    amin = 1.2 * Z + 0.01 * Z * Z
    amax = 5.8 * Z - 0.024 * Z * Z
    if not (amin < A < amax):
        out_dict['success'] = False
        out_dict['reason'] = "A out of limits"
        return out_dict
    aa = A / 400.0
    zz = Z / 100.0
    amin2 = 1.4 * Z + 0.009 * Z * Z
    amax2 = 20.0 + 3.0 * Z
    if ((A < amin2 - 5.0 or A > amax2 + 10) and il > 0.):
        out_dict['success'] = False
        out_dict['reason'] = "L out of limits"
        return out_dict
    pa = lpoly(aa, 6)
    pz = lpoly(zz, 7)
    elmax = elmaxc(Z, A)
    out_dict['elmaxc'] = elmax
    ell = il / elmax
    if (il == 1000):
        ell = 1.0
    if (il > elmax):
        out_dict['success'] = False
        out_dict['reason'] = "L larger than Lmax"
        return out_dict
    saimin, saimx, saimid = 0., 0., 0.
    aizro, ai70, aimax, ai95, aimin = 0., 0., 0., 0., 0.
    bizro, bi70, bimax, bi95, bimin = 0., 0., 0., 0., 0.
    aimax2, ai952 = 0., 0.
    # Now calculate rotating moments of inertia
    for l in range(6):
        for k in range(5):
            t = l + k * 6
            aizro += tables.aizroc[t] * pz[l] * pa[k]
            ai70 += tables.ai70c[t] * pz[l] * pa[k]
            ai95 += tables.ai95c[t] * pz[l] * pa[k]
            aimax += tables.aimaxc[t] * pz[l] * pa[k]
            ai952 += tables.ai952c[t] * pz[l] * pa[k]
            aimax2 += tables.aimax2c[t] * pz[l] * pa[k]
        # end for  k
        for m in range(4):
            t = l + m * 6
            bizro += tables.bizroc[t] * pz[l] * pa[m]
            bi70 += tables.bi70c[t] * pz[l] * pa[m]
            bi95 += tables.bi95c[t] * pz[l] * pa[m]
            bimax += tables.bimaxc[t] * pz[l] * pa[m]
        # end for m
    # end of l
    ff1, ff2, fg1, fg2 = 1., 0., 1., 0.
    if (Z > 70):
        out_dict['Z_over_70'] = True
        aimaxh, aimidh = 0., 0.
        for l in range(4):
            for k in range(4):
                t = l + k * 4
                aimaxh += tables.aimax3c[t] * pz[l] * pa[k]
                aimidh += tables.aimax4c[t] * pz[l] * pa[k]
            # end for k
        # end for l
        if Z > 80:
            out_dict['Z_over_80'] = True
            ff1 = 0.0
        if Z >= 80:
            out_dict['Z_over_or_eq_80'] = True
            fg1 = 0.0
        if bimax > 0.95:
            out_dict['bimax_over_0095'] = True
            fg1 = 0.0
        if aimaxh > aimax:
            out_dict['aimaxh_over_aimax'] = True
            out_dict['aimaxh'] = aimaxh
            out_dict['aimax'] = aimax
            ff1 = 0.0
        ff2 = 1.0 - ff1
        fg2 = 1.0 - fg1
        aimax = aimax * ff1 + ff2 * aimaxh
        aimax2 = aimax2 * ff1 + ff2 * aimidh
        bimax = bimax * fg1 + aimidh * fg2
    # end if Z>70
    saizro = max(aizro, 0.0)
    sai70 = max(ai70, 0.0)
    sai95 = max(ai95, 0.0)
    saimax = max(aimax, 0.0)
    sai952 = max(ai952, 0.0)
    saimax2 = max(aimax2, 0.0)
    sbimax = max(bimax, 0.0)
    sbi70 = max(bi70, 0.0)
    sbi95 = max(bi95, 0.0)
    sbizro = max(bizro, 0.0)
    q1 = -3.1488495690
    q2 = 4.4650587520
    q3 = -1.3162091830
    q4 = 2.261292330
    q5 = -4.947433520
    q6 = 2.686141190
    gam = -20.0 * log(abs(saizro - sai95) / abs(saizro - saimax))
    aa = q1 * saizro + q2 * sai70 + q3 * sai95
    bb = q4 * saizro + q5 * sai70 + q6 * sai95
    gam2 = -20.0 * log(abs(saizro - sai952) / abs(saizro - saimax2))
    aa2 = q1 * saizro + q2 * sai70 + q3 * sai952
    bb2 = q4 * saizro + q5 * sai70 + q6 * sai952
    aa3 = q1 * sbizro + q2 * sbi70 + q3 * sbi95
    bb3 = q4 * sbizro + q5 * sbi70 + q6 * sbi95
    gam3 = 60.0
    alpha = pi * (ell - 0.70)
    beta = 5.0 * pi * (ell - 0.90)
    silt = saizro + aa * ell ** 2 + bb * ell ** 4
    sjlt = sbizro + aa3 * ell ** 2 + bb3 * ell ** 4
    silt2 = saizro + aa2 * ell ** 2 + bb2 * ell ** 4
    sigt = saizro + (saimax - saizro) * exp(gam * (ell - 1.0))
    sjgt = sbi95 + (sbimax - sbi95) * exp(gam3 * (ell - 1.0))
    sigt2 = saizro + (saimax2 - saizro) * exp(gam2 * (ell - 1.0))
    f1 = silt * cos(alpha) ** 2 + sigt * sin(alpha) ** 2
    f2 = silt * cos(beta) ** 2 + sigt * sin(beta) ** 2
    f1m = silt2 * cos(alpha) ** 2 + sigt2 * sin(alpha) ** 2
    f2m = silt2 * cos(beta) ** 2 + sigt2 * sin(beta) ** 2
    f3 = sjlt * cos(alpha) ** 2 + sjgt * sin(alpha) ** 2
    f4 = sjlt * cos(beta) ** 2 + sjgt * sin(beta) ** 2
    if ell <= 0.7:
        saimin = sjlt
        saimx = silt
        saimid = silt2
    elif ell <= 0.95:
        saimx = f1
        saimin = f3
        saimid = f1m
    else:
        saimx = f2
        saimin = f4
        saimid = f2m
    if (ff2 > 0.01 and fg2 > 0.01):
        out_dict['ff2_and_fg2_over_0.01'] = True
        q1 = 4.0016006400
        q2 = 0.9607843140
        q3 = 2.0408163270
        aa3 = q1 * sai70 - q2 * saimax - (1.0 + q3) * saizro
        bb3 = -q1 * sai70 + (1.0 + q2) * saimax + q3 * saizro
        aa4 = q1 * sai70 - q2 * saimax2 - (1.0 + q3) * saizro
        bb4 = -q1 * sai70 + (1.0 + q2) * saimax2 + q3 * saizro
        saimx = saizro + aa3 * ell ** 2 + bb3 * ell ** 4
        saimid = saizro + aa4 * ell ** 2 + bb4 * ell ** 4
    if (saimid > saimx):
        out_dict['saimid_over_saimx'] = True
        saimid = saimx
    saimin = max(saimin, 0.0)
    out_dict['saimin'] = saimin
    out_dict['saimid'] = saimid
    out_dict['saimax'] = saimx
    return out_dict

# EOF
