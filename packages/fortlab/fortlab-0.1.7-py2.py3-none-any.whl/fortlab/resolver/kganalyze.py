# kgen_analyze.py


from fortlab.kgutils import KGName, ProgramException, UserException, traverse
from fortlab.resolver.kgparse import KGGenType, SrcFile, ResState
from fortlab.resolver.Fortran2003 import Name, Call_Stmt, Function_Reference, Part_Ref, Interface_Stmt, Actual_Arg_Spec_List, \
    Section_Subscript_List, Actual_Arg_Spec, Structure_Constructor_2, Proc_Component_Ref, Add_Operand
from collections import OrderedDict
from fortlab.resolver.typedecl_statements import TypeDeclarationStatement
from fortlab.resolver.block_statements import SubProgramStatement, Associate

def update_state_info(parent, config):

    def get_nodes(node, bag, depth):
        from fortlab.resolver.Fortran2003 import Name
        if isinstance(node, Name) and node.string==bag['name'] and not node.parent in bag:
            anc = [node]
            while hasattr(node, 'parent'):
                anc.insert(0, node.parent)
                node = node.parent
            bag['lineage'].append(anc)

    if hasattr(parent, 'content'):
        for stmt in parent.content:
            if isinstance(stmt, TypeDeclarationStatement) and \
                "parameter" not in stmt.attrspec and hasattr(stmt, 'geninfo') and \
                any(len(v)>0 for v in stmt.geninfo.values()):
                for uname, req in KGGenType.get_state_in(stmt.geninfo):
                    if KGGenType.has_uname_out(uname, stmt.geninfo): continue
                    # select names for searching
                    respairs = []
                    if req.originator in config["callsite"]['stmts']:
                        respairs.append((uname, req.originator))
                    elif isinstance(req.originator, Associate):
                        if uname in req.originator.assoc_map:
                            for auname in req.originator.assoc_map[uname]:
                                for aruname, arreq in KGGenType.get_state_in(req.originator.geninfo):
                                    if auname == aruname:
                                        respairs.append((auname, arreq.originator))

                    if len(respairs) > 0:
                        copied = False
                        for varname, org in respairs:
                            bag = {'name': varname.firstpartname(), 'lineage': [] }
                            traverse(org.f2003, get_nodes, bag)
                            for lineage in bag['lineage']:
                                for lidx, anc in enumerate(lineage):
                                    # get callname
                                    callname = None
                                    if anc.__class__ in [ Call_Stmt, Function_Reference ]:
                                        callname = anc.items[0].string
                                    elif anc.__class__ == Part_Ref:
                                        callname = anc.items[0].string
                                    elif anc.__class__ == Interface_Stmt:
                                        callname = anc.items[0].string

                                    # get caller and callee objects
                                    callobj = None
                                    subpobj = None
                                    if callname:
                                        for org_uname, org_req in org.unknowns.items():
                                            if org_uname.firstpartname()==callname:
                                                if isinstance(org_req.res_stmts[0], SubProgramStatement):
                                                    callobj = anc
                                                    subpobj = org_req.res_stmts[0]
                                                break
                                        
                                    # get argument index
                                    argidx = -1
                                    is_keyword = False
                                    if callobj and subpobj:
                                        if callobj.__class__ in [ Call_Stmt, Function_Reference ]:
                                            arglist = callobj.items[1]
                                            if arglist is None: pass
                                            elif isinstance(arglist, Actual_Arg_Spec):
                                                argobj = lineage[lidx+1]
                                                kword = argobj.items[0].string
                                                argidx = 0

                                                if kword in subpobj.args:
                                                    argidx = subpobj.args.index(kword)
                                                
                                            elif isinstance(arglist, Actual_Arg_Spec_List):
                                                argobj = lineage[lidx+2]
                                                if isinstance(argobj, Actual_Arg_Spec):
                                                    argidx = arglist.items.index(argobj)
                                                    kword = argobj.items[0].string
                                                    if kword in subpobj.args:
                                                        argidx = subpobj.args.index(kword)

                                                elif isinstance(argobj, (Name, Proc_Component_Ref,
                                                                Add_Operand, Part_Ref)):
                                                    argidx = arglist.items.index(argobj)
   
                                                else:
                                                    import pdb; pdb.set_trace()
                                                    raise Exception("Not implemented to handle: %s", argobj.__class__.__name__)
                                            else:
                                                argidx = 0
                                        elif anc.__class__ == Part_Ref:
                                            arglist = callobj.items[1]
                                            if arglist is None: pass
                                            elif isinstance(arglist, Structure_Constructor_2):
                                                argobj = lineage[lidx+1]
                                                kword = argobj.items[0].string
                                                argidx = subpobj.args.index(kword)
                                            elif isinstance(arglist, Section_Subscript_List):
                                                argobj = lineage[lidx+2]
                                                argidx = arglist.items.index(argobj)
                                                if isinstance(argobj, Structure_Constructor_2):
                                                    kword = argobj.items[0].string
                                                    argidx = subpobj.args.index(kword)
                                            else:
                                                argidx = 0
                                        elif anc.__class__ == Interface_Stmt:
                                            raise Exception("Interface Statement is not expected.")

                                    # get intent
                                    if argidx>=0:
                                        if argidx >= len(subpobj.args):
                                            raise Exception("argument index exceeds the length of arg. list: %d >= %d",
                                                argidx, len(subpobj.args))
                                        argname = subpobj.args[argidx]
                                        var = subpobj.a.variables[subpobj.args[argidx]]
                                        if var.is_intent_out() or var.is_intent_inout():
                                            req.gentype = KGGenType.STATE_OUT
                                            stmt.add_geninfo(uname, req)
                                            copied = True
                                            break
                                if copied: break
                            if copied: break

    if hasattr(parent, 'parent'):
        update_state_info(parent.parent, config)


def analyze(config):

    analyze_callsite(config)

def analyze_callsite(config):
    from fortlab.resolver.block_statements import EndStatement, Subroutine, Function, Interface
    from fortlab.resolver.statements import SpecificBinding
    from fortlab.resolver.kgsearch import f2003_search_unknowns

    # read source file that contains callsite stmt
    cs_file = SrcFile(config["callsite"]['filepath'])

    #process_directive(cs_file.tree)

    if len(config["callsite"]['stmts'])==0:
        raise UserException('Can not find callsite')

    # ancestors of callsite stmt
    ancs = config["callsite"]['stmts'][0].ancestors()

    # add geninfo for ancestors
    prevstmt = config["callsite"]['stmts'][0]
    prevname = None

    for anc in reversed(ancs):
        if not hasattr(anc, 'geninfo'):
            anc.geninfo = OrderedDict()
        if len(anc.content)>0 and isinstance(anc.content[-1], EndStatement) and \
            not hasattr(anc.content[-1], 'geninfo'):
            anc.content[-1].geninfo = OrderedDict()

        if prevname:
            dummy_req = ResState(KGGenType.STATE_IN, KGName(prevname), None, [anc])
            dummy_req.res_stmts = [ prevstmt ]
            anc.check_spec_stmts(dummy_req.uname, dummy_req)

        if hasattr(anc, 'name'): prevname = anc.name
        else: prevname = None
        prevstmt = anc

    # populate parent block parameters
    config["parentblock"]['stmt'] = ancs[-1]

    # populate top block parameters
    config["topblock"]['stmt'] = ancs[0]

    for cs_stmt in config["callsite"]['stmts']:
        #resolve cs_stmt
        f2003_search_unknowns(cs_stmt, cs_stmt.f2003, config)
        for uname, req in cs_stmt.unknowns.items():
            cs_stmt.resolve(req, config)
            if not req.res_stmts:
                raise ProgramException('Resolution fail.')


    # update state info of callsite and its upper blocks
    update_state_info(config["parentblock"]['stmt'], config)

    # update state info of modules
    for modname, moddict in config["modules"].items():
        modstmt = moddict['stmt']
        if modstmt != config["topblock"]['stmt']:
            update_state_info(moddict['stmt'], config)
