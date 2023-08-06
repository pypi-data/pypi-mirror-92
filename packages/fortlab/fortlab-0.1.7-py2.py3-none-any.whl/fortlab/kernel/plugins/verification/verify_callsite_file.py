# gen_read_callsite_file.py
from __future__ import absolute_import

from fortlab.resolver import statements, block_statements, typedecl_statements
from fortlab.kgplugin import Kgen_Plugin
from .verify_utils import VERIFY_PBLOCK_USE_PART, VERIFY_PBLOCK_DECL_PART, VERIFY_PBLOCK_EXEC_PART, \
    VERIFY_PBLOCK_CONTAINS_PART, VERIFY_PBLOCK_SUBP_PART, VERIFY_PBLOCK_EXTERNS, VERIFY_PBLOCK_LOCALS, \
    VERIFY_PBLOCK_INIT

class Verify_K_Callsite_File(Kgen_Plugin):
    def __init__(self):
        self.frame_msg = None

    # registration
    def register(self, msg):
        self.frame_msg = msg

        # register initial events

        self.frame_msg.add_event(KERNEL_SELECTION.ALL, FILE_TYPE.KERNEL, GENERATION_STAGE.NODE_CREATED, \
            getinfo('parentblock_stmt'), None, self.create_parentblock_parts)

        self.frame_msg.add_event(KERNEL_SELECTION.ALL, FILE_TYPE.KERNEL, GENERATION_STAGE.NODE_CREATED, \
            getinfo('topblock_stmt'), None, self.create_topblock_parts)

    def create_topblock_parts(self, node):

        #attrs = {'name': 'kgen_utils_mod', 'isonly': True, 'items':['check_t', 'kgen_init_check', 'kgen_tolerance', \
        #    'kgen_minvalue', 'CHECK_IDENTICAL', 'CHECK_IN_TOL', 'CHECK_OUT_TOL']}
        #part_append_genknode(node, USE_PART, statements.Use, attrs=attrs)

        prenode = getinfo('blocknode_aftercallsite_main')
        self.frame_msg.add_event(KERNEL_SELECTION.ALL, FILE_TYPE.KERNEL, GENERATION_STAGE.BEGIN_PROCESS, \
            prenode, None, self.create_verification_parts)

        namedpart_create_subpart(prenode, VERIFY_PBLOCK_INIT, EXEC_PART)
        namedpart_append_comment(prenode.kgen_kernel_id, VERIFY_PBLOCK_INIT, '')
        namedpart_append_comment(prenode.kgen_kernel_id, VERIFY_PBLOCK_INIT, 'verify init')

        namedpart_create_subpart(prenode, VERIFY_PBLOCK_EXTERNS, EXEC_PART)
        namedpart_append_comment(prenode.kgen_kernel_id, VERIFY_PBLOCK_EXTERNS, '')
        namedpart_append_comment(prenode.kgen_kernel_id, VERIFY_PBLOCK_EXTERNS, 'extern verify variables')

        namedpart_create_subpart(prenode, VERIFY_PBLOCK_LOCALS, EXEC_PART)
        namedpart_append_comment(prenode.kgen_kernel_id, VERIFY_PBLOCK_LOCALS, '')
        namedpart_append_comment(prenode.kgen_kernel_id, VERIFY_PBLOCK_LOCALS, 'local verify variables')

    def create_verification_parts(self, node):

        attrs = {'designator': 'kgen_init_verify', 'items': ['tolerance=%s'%getinfo('verify_tol'), \
            'minvalue=%s'%getinfo('verify_minval'), 'verboseLevel=%s'%getinfo('verbose_level')]}
        namedpart_append_genknode(node.kgen_kernel_id, VERIFY_PBLOCK_INIT, statements.Call, attrs=attrs)

        attrs = {'designator': 'kgen_init_check', 'items': ['check_status', 'rank=kgen_mpirank']}
        namedpart_append_genknode(node.kgen_kernel_id, VERIFY_PBLOCK_INIT, statements.Call, attrs=attrs)

        attrs = {'expr': 'check_status%rank == 0'}
        ifrank = part_append_genknode(node, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'items': ['""']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        # verification statistics
        attrs = {'expr': 'kgen_verboseLevel > 0'}
        ifstatobj = part_append_genknode(node, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'expr': 'check_status%rank == 0'}
        ifrank = part_append_genknode(ifstatobj, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'items': ['"Number of output variables: "','check_status%numTotal']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        attrs = {'items': ['"Number of identical variables: "','check_status%numIdentical']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        attrs = {'items': ['"Number of non-identical variables within tolerance: "','check_status%numInTol']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        attrs = {'items': ['"Number of non-identical variables out of tolerance: "','check_status%numOutTol']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        attrs = {'items': ['"Tolerance: "','kgen_tolerance']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        attrs = {'expr': 'check_status%rank == 0'}
        ifrank = part_append_genknode(node, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'items': ['""']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        # verification result
        attrs = {'expr': 'check_status%numOutTol > 0'}
        ifobj = part_append_genknode(node, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'expr': 'check_status%rank == 0'}
        ifrank = part_append_genknode(ifobj, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'items': ['"Verification FAILED with" // TRIM(ADJUSTL(kgen_filepath))']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)
        
        attrs = {'variable': 'check_status%Passed', 'sign': '=', 'expr': '.FALSE.'}
        part_append_genknode(ifobj, EXEC_PART, statements.Assignment, attrs=attrs)

        attrs = {'variable': 'kgen_isverified', 'sign': '=', 'expr': '.FALSE.'}
        part_append_genknode(ifobj, EXEC_PART, statements.Assignment, attrs=attrs)

        part_append_genknode(ifobj, EXEC_PART, statements.Else, attrs=attrs)

        attrs = {'expr': 'check_status%rank == 0'}
        ifrank = part_append_genknode(ifobj, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'items': ['"Verification PASSED with " // TRIM(ADJUSTL(kgen_filepath))']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)
        
        attrs = {'variable': 'check_status%Passed', 'sign': '=', 'expr': '.TRUE.'}
        part_append_genknode(ifobj, EXEC_PART, statements.Assignment, attrs=attrs)

        attrs = {'variable': 'kgen_isverified', 'sign': '=', 'expr': '.TRUE.'}
        part_append_genknode(ifobj, EXEC_PART, statements.Assignment, attrs=attrs)

        attrs = {'expr': 'check_status%rank == 0'}
        ifrank = part_append_genknode(node, EXEC_PART, block_statements.IfThen, attrs=attrs)

        attrs = {'items': ['""']}
        part_append_genknode(ifrank, EXEC_PART, statements.Write, attrs=attrs)

        if getinfo('add_mpi_frame'):
            part_append_comment(node, EXEC_PART, '')
            part_append_comment(node, EXEC_PART, '#ifdef _MPI', style='rawtext')
            part_append_comment(node, EXEC_PART, 'call mpi_barrier(mpi_comm_world, kgen_ierr)', style='rawtext')
            part_append_comment(node, EXEC_PART, '#endif', style='rawtext')
            part_append_comment(node, EXEC_PART, '')

    def create_parentblock_parts(self, node):

        namedpart_link_part(node, VERIFY_PBLOCK_USE_PART, USE_PART)
        namedpart_link_part(node, VERIFY_PBLOCK_DECL_PART, DECL_PART)
        namedpart_link_part(node, VERIFY_PBLOCK_EXEC_PART, EXEC_PART)
        namedpart_link_part(node, VERIFY_PBLOCK_CONTAINS_PART, CONTAINS_PART)
        namedpart_link_part(node, VERIFY_PBLOCK_SUBP_PART, SUBP_PART)

        attrs = {'type_spec': 'TYPE', 'selector':(None, 'check_t'), 'entity_decls': ['check_status']}
        part_append_genknode(node, DECL_PART, typedecl_statements.Type, attrs=attrs)
