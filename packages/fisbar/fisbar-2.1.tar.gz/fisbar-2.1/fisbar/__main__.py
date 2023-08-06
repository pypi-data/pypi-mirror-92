#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: december 2020 -*-
# -*- copyright: GH/IPHC 2020 -*-
# -*- file: __main__.py -*-
# -*- purpose: -*-


'''
Run the module at stand alone program

Call `python -m fisbar` to access the code as a standalone.
Arguments are Z, A (both mandatory), L (default = 0) and output style

When using `columns` output style, the results are outputed as columns following
Z A L bfis Egs Lmax
'''

import argparse

import fisbar


def stylized_columns(dIn: dict) -> str:
    'make coulumns output'
    return " ".join([str(dIn.get(k, '***')) for k in ('Z', 'A', 'L',
                                                      'bfis', 'egs', 'elmax',
                                                      'imin', 'imid', 'imax')])


def stylized_human(dIn: dict) -> str:
    'make human readable output'
    return "\n".join(['',
                      f"# Fisbar calculation for Z={dIn['Z']}, A={dIn['A']} and L={dIn['L']}",
                      " ",
                      f"- Fission barrier at L={dIn['L']} = {dIn.get('bfis', '***')} MeV",
                      f"- Ground state energy = {dIn.get('egs', '***')} MeV",
                      f"- Maximum angular momentum = {dIn.get('elmax', '***')}",
                      "- Moments of inertia:",
                      f"    - min = {dIn.get('imin', '***')}",
                      f"    - mid = {dIn.get('imid', '***')}",
                      f"    - max = {dIn.get('imax', '***')}",
                      '', ''])


def stylized_yaml(dIn: dict) -> str:
    'output in yaml format'
    return "\n".join([f"{k}: {str(dIn.get(k, '***'))}" for k in ('Z', 'A', 'L',
                                                                 'bfis', 'egs', 'elmax',
                                                                 'imin', 'imid', 'imax')])


def run_fisbar(Z: int, A: int, L: int = 0,
               style: str = 'dict') -> str:
    'Runs the fisbar routine and write the output'
    dOut: dict = fisbar.barfit(Z, A, L)
    if style == 'columns':
        return stylized_columns(dOut)
    if style == 'human':
        return stylized_human(dOut)
    if style == 'yaml':
        return stylized_yaml(dOut)
    return str(dOut)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog="fisbar",
                                         description=__doc__)
    arg_parser.add_argument('Z', type=int,
                            help="Atomic number of the nucleus")
    arg_parser.add_argument('A', type=int,
                            help="Mass number of the nucleus")
    arg_parser.add_argument('L', type=int,
                            default=0,
                            nargs='?',
                            help="Angular momentum at which to calculate")
    arg_parser.add_argument('--style', type=str,
                            choices=('columns', 'human', 'dict', 'yaml'),
                            default='dict',
                            help='Style of the output')
    the_args = arg_parser.parse_args()
    print(run_fisbar(**vars(the_args)))

# EOF
