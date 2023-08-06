"""
Strucure analysis
=============================

The rules are quite limited right now (only 6).
The approach, a statefull line-by-line test using a class,
smells a lot.

We will need to do a simpler version of this with we want to go furthet.
(Well, for the moment,  if it ain't broke, don't fix it... )

"""

import re
from flinter.initialize import rate
from flinter.fmt_analysis import fmt_analysis



__all__ = ["scan_fortran_file"]


def scan_fortran_file(path, readlines_, rules):
    """
    :params content: list of lines in FORTRAN
    """
    out = list()
    joined_stmts = join_statements(clean_statements(readlines_))
    last_stmt = joined_stmts[-1]

    buff_list = list()
    bname = None
    btype = None
    for statement in joined_stmts:
        buff_list.append(statement)
        starting_block = block_start(statement,rules["syntax"])
        if starting_block is not None:
            bname = bstart_getname(statement, starting_block)
            btype = starting_block

        if starting_block is not None and len(buff_list)>1:
            out.append(test_bufferlist(buff_list,path, bname, btype, rules))
            buff_list = list()
            continue
    
        if statement == last_stmt:
            out.append(test_bufferlist(buff_list,path, bname, btype,  rules))
            buff_list = list()
            continue
    
    return out

def test_bufferlist(buff_list,path, bname, btype,  rules):
    """Test a buffer list
    
    should be like a FUNCTION or a SUBROUTINE
    with statements joined (no multiline), cleaned, as lower case
    and no void or comment line
    """
    if bname is None:
        bname = "Not found"
        btype = "not provided"

    test_st = test_blockst(buff_list, rules["syntax"], rules["struct-rules"])
    regexp_rules = fmt_analysis(
        buff_list, rules["regexp-rules"], verbose=False)
    
    struct_nb = 0
    for err in test_st["errors"]:
        struct_nb+= len(test_st["errors"][err])

    regexp_nb = 0
    for wng in regexp_rules:
        regexp_nb+= regexp_rules[wng]

    dict_ = {
        "name": bname,
        "type": btype,
        "size": len(buff_list),
        "path": path + "/"+ bname,
        "children": list(),
        "struct_rules": test_st["errors"],
        "struct_nberr": struct_nb,
        "regexp_nberr": regexp_nb,
        "regexp_rules": regexp_rules,
        "rate": rate(len(buff_list), struct_nb, regexp_nb)
    }
    return dict_




def block_start(stmt, syntax):
    """ return true when statement is a starting block
    """
    clean_st = clean_line(stmt)
    # needed else end block  can be understood as start
    for blocktype in syntax["blocks"]:
        if clean_st.startswith(blocktype):
            return blocktype
    # Typed functions
    for var_type in syntax["types"]:
        if clean_st.startswith(var_type):
            if " function " in clean_st:
                return blocktype
    return None

    
def bstart_getname(stmt, type_):
    """ return the name of a starting block (needtype)

    eg:

    function totoro(a,b,c) -> (function, totoro)
    """
    try:
        clean_st = clean_line(stmt)
        tail= clean_st.split(type_)[-1]
        wo_args = tail.split("(")[0]
        name = wo_args.strip()
    except IndexError as e:
        raise RuntimeError(f"{stmt} \n {e}")
    return  name


def test_blockst(statement_lst, syntax, struct_rules):
    """ analysis of a block """
    join_statements_lst = join_statements(statement_lst)

    out = {
        "statements": join_statements_lst,
        "args": get_arguments(join_statements_lst[0]),
        "locals": list(),
        "errors": dict(),
    }

    for name in get_variables(join_statements_lst, syntax["types"]):
        if name not in out["args"]:
            out["locals"].append(name)

    max_nest_depth = get_ifdo_nesting(join_statements_lst)

    list_errors = list()

    list_errors.extend(
        statements_errors(
            join_statements_lst,
            maxline=struct_rules["max-statements-in-context"]
        )
    )
    list_errors.extend(
        vars_errors(out["locals"],
            max_declared_locals=struct_rules["max-declared-locals"],
            min_varlen=struct_rules["min-varlen"],
            max_varlen=struct_rules["max-varlen"],
        )
    )
    list_errors.extend(
        args_errors(out["args"],
            max_arguments=struct_rules["max-arguments"],
            min_arglen=struct_rules["min-arglen"],
            max_arglen=struct_rules["max-arglen"],
        )
    )
    list_errors.extend(ifdoerrors(
        max_nest_depth, 
        max_depth=struct_rules["max-nesting-levels"]))

    for error in list_errors:
        key = error.split(":")[0].strip()
        specifier =error.split(":")[1].strip()
        add_record(out["errors"], key, specifier)

    return out


def get_ifdo_nesting(join_statements_lst):#clean_st, cur_ifdo, cur_depth):
    """ Find the nesting of ifs and dos
    """
    cur_ifdo = 0
    cur_depth = 0
    for clean_st in join_statements_lst:
        for st_match in ["if", "do"]:
            if clean_st.startswith(st_match):
                cur_ifdo += 1
                cur_depth = max(cur_depth, cur_ifdo)

            for ending in ["end", "end "]:
                if clean_st.startswith(ending + st_match):
                    cur_ifdo -= 1

    return cur_depth


def get_arguments(head):
    """ get arguments in the header of a block

    I do not like this one, I am sure it can be done better
    """
    start_idx = head.find("(") + 1
    end_idx = head.find(")")
    list_args = head[start_idx:end_idx].split(",")
    list_args = [name.strip() for name in list_args]
    # remove empty items "".
    list_args = list(filter(lambda item: item, list_args))
    return list_args


def get_variables(statement_lst, types):
    """ identifie a declaration line and give the list of varaibles
    """
    list_var = list()
    for statement in statement_lst:
        for typename in types:
            if statement.startswith(typename):
                if "::" in statement:
                    list_var.extend(parse_varline_re(statement.split("::")[-1]))
    return list_var


def parse_varline_re(line):
    """The rexexp version of parse varline, quite faster"""
    out = re.findall("(\w+)(?:\(.*\)|,|)", line)
    return out


def add_record(dict_, key, specifier):
    """Add a record to a dict"""
    if key not in dict_:
        dict_[key] = [specifier]
    else:
        dict_[key].append(specifier)


def clean_line(statement_str):
    """remove comment in statement_string
    """
    out = statement_str.strip().lower()
    
    if out =="":
        return out
    # handing exceptions in comments
    for comm_exception in ["double", "complex"]:
        if out.startswith(comm_exception):
            return out

    if out[0] in ["!", "c", "d "]:
        out = str()
    if "!" in out:
        out =  out.split("!")[0]
    return out


def clean_statements(statement_lst):
    """Return statements witout comments and block lines"""
    out = list(filter(None, (clean_line(st) for st in statement_lst)))
    return out


def join_statements(statement_lst):
    """Join statements if continuation line char is present."""

    if len(statement_lst) == 0:
        return list()

    if len(statement_lst) == 1:
        return statement_lst[0]

    out = list()
    former_line = statement_lst[0]
    for line in statement_lst[1:]:
        if line.startswith("$"):
            former_line = former_line.strip("$") + line.strip("$")
        elif former_line.endswith("&"):
            former_line = former_line.strip("&") + line.strip("&")
        else:
            out.append(former_line)
            former_line = line
    out.append(former_line)
    return out


def statements_errors(stt_list, maxline=50):
    """Assess staments"""
    out = list()
    lstat = len(stt_list)
    if lstat > maxline:
        out.append(f"too-many-lines : {str(lstat)}/{str(maxline)}")
        for _ in range(int(lstat/maxline)-1):
            out.append(f"too-many-lines : warning")
    return out


def vars_errors(
        var_list,
        max_declared_locals=12,
        min_varlen=3,
        max_varlen=20,
        ):
    """Assess variables errors"""
    out = list()
    lstat = len(var_list)
    if lstat > max_declared_locals:
        out.append(f"too-many-locals : {str(lstat)} /{str(max_declared_locals)}")
        for _ in range(int(lstat/max_declared_locals)-1):
            out.append(f"too-many-locals : warning")

    for varname in var_list:
        if len(varname) < min_varlen:
            out.append(f"short-varname : {varname}")
        if len(varname) > max_varlen:
            out.append(f"long-varname: {varname}")
    return out


def ifdoerrors(depth, max_depth=3):
    """Assess bock if and do complexity"""
    out = list()

    if depth > max_depth:
        out.append(
            f"too-many-levels : {str(depth)}/{str(max_depth)} nested IF and DO blocks"
        )

    return out


def args_errors(
            arg_list, 
            max_arguments=4,
            min_arglen=3,
            max_arglen=20,
        ):
    """Assess arguments errors"""
    out = list()
    larg = len(arg_list)

    if larg > max_arguments:
        out.append(f"too-many-arguments : {str(larg)} /{str(max_arguments)}")
        for _ in range(int(larg/max_arguments)-1):
            out.append(f"too-many-arguments : warning")

    for varname in arg_list:
        if len(varname) < min_arglen:
            out.append(
                f"short-argname :{varname}")
        if len(varname) > max_arglen:
            out.append(
                f"long-argname : {varname}")
    return out