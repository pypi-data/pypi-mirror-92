#!/usr/bin/env python
"""
Command line Interface
======================


CLI using Click. The scoring formula and presentation is also in this module.

"""
import os
import glob
import click
from flinter.initialize import new_rules
from flinter.fort2tree import dumpstats, visualfort, score_cli

#from flinter.struct_analysis import struct_analysis
#from flinter.fmt_analysis import fmt_analysis


@click.group()
def main_cli():
    """--------------------    FLINT  ---------------------

.      - Flint, because our code stinks... -


You are now using the Command line interface of Flint,
a Fortran linter created at CERFACS (https://cerfacs.fr),
for the EXCELLERAT center of excellence (https://www.excellerat.eu/).

This is a python package currently installed in your python environement.

"""
    pass


@click.command()
@click.argument("path", nargs=1)
@click.option("--flintrc", "-r", type=str, default=None, help="Custom rules file")
@click.option("--depth", "-d", type=int, default=3, help="Depth of stats [1-10000]")
def score(path, flintrc, depth=1000):
    """Score the formatting of a Fortran  folder
    """

    if not os.path.isdir(path):
        print(f"\n Flint could not score directory {path} \n")
        return
    
    score_cli(path, flinter_rc=flintrc, max_lvl=depth)

main_cli.add_command(score)


@click.command()
@click.argument("path", nargs=1)
@click.option("--flintrc", "-r", type=str, default=None, help="Custom rules file")
@click.option("--minrate", "-m", type=int, default=-10, help="Minimum rate allowed")
@click.option("--norate", is_flag=True, help="only structure, no rates")
def tree(path, flintrc, minrate, norate):
    """Visual representation of the score
    """    
    if os.path.isdir(path):
        print(f"\n Showing  scoring tree of Directory {path} \n")
    else:
        print(f"\n Directory {path} is not a valid path\n")
        exit(1)
    visualfort(path, flinter_rc=flintrc, minrate=minrate, norate=norate)
main_cli.add_command(tree)

@click.command()
@click.argument("path", nargs=1)
@click.argument("fname", nargs=1)
@click.option("--flintrc", "-r", type=str, default=None, help="Custom rules file")
def dump(path, fname, flintrc):
    """Dump full stats.
    """
    ext = os.path.splitext(fname)[-1]
    if ext in [".yml", ".yaml"]:
        pass
    elif ext == "":
        fname += ".yml"
    else:
        print(f"\n Yaml Dump file {fname} should have .yml extenion\n")
        exit(1)

    if os.path.isdir(path):
        print(f"\n Dumping  scoring stats of  {path} in file {fname} \n")
    else:
        print(f"\n Directory {path} is not a valid path\n")
        exit(1)
    
    dumpstats(path, fname, flinter_rc=flintrc)

main_cli.add_command(dump)

@click.command()
def config(fname):
    """Copy the default rule file .flint_rc.yml locally
    """
    new_rules()

main_cli.add_command(config)
