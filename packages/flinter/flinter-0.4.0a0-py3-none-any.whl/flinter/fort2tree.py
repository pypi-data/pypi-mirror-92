"""Scan a folder for fortran files and build the tree."""

import os, sys, glob, math
import yaml

import circlify as circ
from nobvisual import tkcirclify, path_as_str

from flinter.initialize import init_format_rules, rate
from flinter.struct_analysis import scan_fortran_file


__all__= ["dumpstats", "score_cli"]

def dumpstats(wdir, fname, flinter_rc=None):
    """Dump score stats in a yaml file"""
    rules = init_format_rules(flinter_rc=flinter_rc)

    scantree  = fort2tree(wdir, rules)
    with open(fname, "w") as fout:
        yaml.dump(scantree,fout)

def score_cli(wdir, flinter_rc=None, max_lvl=None):
    """Show stats in terminal"""
    rules = init_format_rules(flinter_rc=flinter_rc)
    scantree  = fort2tree(wdir, rules)

    if max_lvl ==0:
        rating = '{:.2f}'.format(scantree['rate'])
        size = scantree['size']
        print(f"Flinter global rating -->|{rating}|<--  ({size} statements)")
        return


    head = "  {:<3} {:<50} {:<10} {:<10}".format("lvl", "path", "rate", "size (stmt)")
    print(head)
        
    indent = "........"
    def _rec_print(data,  lvl=0):
 
        # head = str()
        # head +=f"{indent(lvl, char='-')}{data['path']}"
        # head += f" rate : {'{:.2f}'.format(data['rate'])}"
        # head += f" size : {data['size']} statements"

       
        head = "  {:<3} {:<50} {:<10} {:<10}".format(lvl, data['path'], '{:.2f}'.format(data['rate']), data['size'])

        print(head)
        if "regexp_rules" in data:
            for key in data["regexp_rules"]:
                print(f"{indent} {key} :  {str(data['regexp_rules'][key])}")
        if "struct_rules" in data:
            for key in data["struct_rules"]:
                print(f"{indent} {key} :  {'/'.join(data['struct_rules'][key])}")
        

        if data["children"]:
            if lvl >= max_lvl:
                print(f"{indent}.")
                return
            else:
                for child in data["children"]:
                    _rec_print(child, lvl=lvl+1 )
    _rec_print(scantree)


def visualfort(wdir, flinter_rc=None, minrate=-10, norate=False):
    """Visualization os fortran source code
    """
    rules = init_format_rules(flinter_rc=flinter_rc)
    scantree  = fort2tree(wdir, rules)
    circ_ob = tree2circ(scantree, minrate=minrate, norate=norate)
    circles = circ.circlify(circ_ob, show_enclosure=True)

    if norate:
        colorscale = None
    else:
        colorscale=("Standard compliance", "High (10)", f"Low ({str(minrate)})")

    tkcirclify(
        circles,
        color="#eeeeee",
        colorscale=colorscale,
        title=f"Flinter showing {str(wdir)}",
    )

def fort2tree(wdir, rules):
    """ Build the structure of a folder tree.

    :params wdir: path to a directory
    """

    def _rec_subitems(path):
        name = os.path.split(path)[-1]
        out = {
            "name": name,
            "path": path,
            "size": 0,
            "struct_nberr":0,
            "regexp_nberr":0,
            "rate":0,
            "children": list()
        }
        if os.path.isfile(path):
            ext = os.path.splitext(path)[-1]
            if ext.lower() in [".f90", ".f"]:
                try:
                    with open(path, "r", encoding="utf8") as fin:
                        out["children"] = scan_fortran_file(path,fin.readlines(), rules)
                        for block in out["children"]:
                            out["size"]+= block["size"]
                            out["struct_nberr"]+= block["struct_nberr"]
                            out["regexp_nberr"]+= block["regexp_nberr"]

                    out["rate"] = rate(
                        out["size"], out["struct_nberr"], out["regexp_nberr"]
                    )
                except UnicodeDecodeError:
                    print(f"File {path} is not encoded in UTF-8")

        else:
            out["children"] = list()
            paths = glob.glob(os.path.join(path, "**"))
            for nexpath in paths:
                record = _rec_subitems(nexpath)
                if record["size"] > 0:
                    out["children"].append(record)
                
                    out["size"]+= record["size"]
                    out["struct_nberr"]+= record["struct_nberr"]
                    out["regexp_nberr"]+= record["regexp_nberr"]
            
            out["rate"] = rate(
                out["size"], out["struct_nberr"], out["regexp_nberr"]
            )


        return out
    out = _rec_subitems(os.path.relpath(wdir))

    return out




def tree2circ(tree,  minrate=-20, norate=False):
    """Translate the tree structure to a circlify object"""

    def _rec_tree2circ(subtree):

        out = {
            "id": path_as_str(subtree["path"].split("/")),
            "datum": subtree["size"],
            "children": list()
        }
        
        for childtree in subtree["children"]:
            out["children"].append(_rec_tree2circ(childtree))
        
        if norate:
            pass
        else:
            #if not subtree["children"]:
            try:
                value = max((10-subtree["rate"])/(10.-minrate),0)
                out["id"] += "\n rate "+str(subtree["rate"])
                out["id"] += "|COLOR=colormap:"+str(value)
            except KeyError:
                out["id"] += "|COLOR=#ff0000"
        return out

    out = [_rec_tree2circ(tree)]
    return out 