#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: january 2021 -*-
# -*- copyright: GH/IPHC 2021 -*-
# -*- file: lpoly.py -*-
# -*- purpose: -*-

'''
Defines the `lpoly` function that compute the value of the
 Legendre polynomials values
'''


def lpoly(x: float, n: int) -> list:
    'Return the n Legendre polynomials values at x'
    pl = [1.0, x]
    for i in range(2, n):
        pl.append(((2. * i - 1.) * x * pl[-1] - (i - 1.) * pl[-2]) / (i * 1.))
    return pl

# EOF
