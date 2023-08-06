"""Module containing base functions to lint
    and dectect broken formatting rules
"""
import re
import os
import pkg_resources
import yaml
import shutil


__all__ = ["rate", "new_rules", "init_format_rules"]

def rate(lines_nb, struct_nb, regexp_nb):
    """rate the quality of each record"""
    if lines_nb == 0:
        rate= 0
    else:
        rate = (float(struct_nb * 5 + regexp_nb) / lines_nb) * 10
        rate = 10.0 - rate
    return rate

def new_rules(filename=None):
    """Create default rules file."""
    if filename is None:
        filename = "./flinter_rc.yml"
    write = True
    if os.path.isfile(filename):
        msg = f'File {filename} already exists. Overwrite ? [y/N] '
        if input(msg).lower() == 'n':
            write = False
    if write:
        print(f'Generating rule file {filename} for Flinter.')
        shutil.copy2(
            pkg_resources.resource_filename("flinter", "flinter_rc_default.yml"),
            filename,
        )

def init_format_rules(flinter_rc=None):
    """Load format rules from resosurces.
    """
    if flinter_rc is None:
        flinter_rc = pkg_resources.resource_filename(
            "flinter", "flinter_rc_default.yml")

    with open(flinter_rc) as fin:
        rules = yaml.load(fin, Loader=yaml.FullLoader)

    # create syntax reference 
    syntax = rules["fortran-syntax"]

    # create syntax copy for regular expression replacement
    syntax_re = dict()
    for key in syntax:
        syntax_re[key] = r"|".join(syntax[key])
    syntax_re["types_upper"] = syntax_re["types"].upper()

    # select active rules
    myrules = dict()
    for key in rules["regexp-rules"]:
        if rules["regexp-rules"][key]["active"]:
            myrules[key] = rules["regexp-rules"][key]

    # compile the rules
    for key in myrules:
        myrules[key] = _compile_format_rule(myrules[key], syntax_re)
    
    
    out= {
        "syntax": syntax,
        "regexp-rules": myrules,
        "struct-rules": rules["structure-rules"],
    }

    return out

def _compile_format_rule(rule, syntax):
    """Compile the regexp action for a rule
    :param rule: dict
        - message
        - regexp
        - repalcement
        the rules to be implemented
        some rules a based upon lists stored in syntax
    :param syntax: dict
        - types
        - operators
        - structs
        - punctuation
        language specific lists of items

    """
    if rule["message"] is not None:
        rule["message"] = rule["message"].format(**syntax)
    else:
        rule["message"] = None

    rule["regexp"] = re.compile(rule["regexp"].format(**syntax))

    return rule



