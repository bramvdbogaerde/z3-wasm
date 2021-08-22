"""
This module provides a generator to generate Javascript Glue code that can be used in combination with Z3 compiled for WASM
"""


import traceback
from cast import *
from exceptions import CommandLineArgumentError, CouldNotParseHeader, UnexpectedASTNode
from clang.cindex import Index
from visitor import visitor, visit, get_next
import clang.cindex as cindex
import sys


USAGE = """
Please provide the location of the Z3 source code.

Usage: generate_bindings.py Z3_SOURCE_LOCATION OUTPUT_LOCATION
"""

@visitor(on = lambda token: token.kind)
class HeaderVisitor:
    def default(self, _): 
        return None

    @visit(cindex.CursorKind.FUNCTION_DECL)
    def visit_function_decl(self, decl):
        """
        Visits a function declaration. This is what we need.

        A function declaration consists of a: 
        - visibility attribute (we ignore this)
        - a return type
        - a variable number of arguments

        :return This function always returns a declaration object or results in an error.
        
        """
        # We are only interested in Z3 functions 
        if decl.spelling.startswith("Z3_"):
            children = decl.get_children()

            # Ignore the visibility attribute 
            next(children)

            # TODO: use a different representaton for void
            ret_tpy_maybe = get_next(children)
            ret_tpy = "void"
            parameters = []
            if ret_tpy_maybe and ret_tpy_maybe.kind == cindex.CursorKind.TYPE_REF:
                # return type is defined 
                ret_tpy = self.accept(ret_tpy_maybe)
            elif ret_tpy_maybe and ret_tpy_maybe.kind == cindex.CursorKind.PARM_DECL:
                # no return type proceed with parameters
                parameters = [ self.accept(ret_tpy_maybe) ]
            elif not(ret_tpy_maybe):
                # not return type and no parameters
                return Declaration(decl.spelling, ret_tpy, parameters)
            else:
                raise UnexpectedASTNode(ret_tpy_maybe)

            # Variable number of parameters
            parameters = parameters + [ self.accept(parameter) for parameter in children ]

            return Declaration(decl.spelling, ret_tpy, parameters)

    @visit(cindex.CursorKind.TYPE_REF)
    def visit_type_ref(self, type_ref):
        return type_ref.spelling

    @visit(cindex.CursorKind.PARM_DECL)
    def visit_param_decl(self, param):
        """
        A parameter declaration consists of a type and optionally a name,
        we are only interested in the type.
        """
        tpy_ref = get_next(param.get_children())
        if tpy_ref:
            # use the type if available
            return tpy_ref.spelling
        else:
            # if libclang failed to parse the type of the argument, default to int
            return "int"
  

def parse_file(filename): 
    """
    Parses a header file into a list of declarations

    :return a list of ast.Declaration instances
    """
    index = Index.create()
    # TODO: discover the correct include path
    tu = index.parse(filename, ["-I", "/usr/lib/clang/12.0.1/include/"])
    visitor = HeaderVisitor()
    if not tu: 
        raise CouldNotParseHeader()

    if len(tu.diagnostics) > 0:
        print("Some error(s) occured while parsing file")
        for diag in tu.diagnostics:
            print(diag)

        raise CouldNotParseHeader()

    return filter(lambda decl: decl, [ visitor.accept(token) for token in tu.cursor.get_children() ])

def open_file_writer(filename, options = "w"):
    return open(filename, options)

def translate_tpy(tpy):
    """
    Translates a Z3 C type to a Javascript type.

    :return Either "string" or "number", "number" is used for any other type than a string, because Z3 API mostly
    works with opaque pointers.
    """

    if tpy == "Z3_string": 
        return "string"
    else:
        return "number"

def translate_decl(decl, writer):
    """
    Translates a single declaration into a Javascript function by writing to a sink using the given writer
    """
    javascript_name = decl.name[3:] # remove Z3_ prefix from javascript name
    c_name = decl.name
    ret_tpy = translate_tpy(decl.ret_tpy)
    argument_types = ",".join([ translate_tpy(tpy) for tpy in decl.parameters ])
    writer.write("""      "%s": Module.cwrap("%s", "%s", [%s]),
    """ % (javascript_name, c_name, ret_tpy, argument_types))

def translate_decls(declarations, writer):
    writer.write("const Z3 = {\n")
    for declaration in declarations:
        translate_decl(declaration, writer)
    writer.write("}\n")

def __parse_args():
    """
    Parses the command line arguments, and raises an error if not all required
    arguments are provided

    :return A dictionary containing the keys associated with the command line options.
    """
    args = sys.argv

    if len(args) != 3: 
        raise CommandLineArgumentError()
    else:
        return dict(z3_location = args[1], program_name = args[0], output_location = args[2])


if __name__ == "__main__":
    try: 
        config = __parse_args()
        declarations = parse_file(config["z3_location"]+"/src/api/z3.h")
        writer = open_file_writer(config["output_location"]+"/z3-bindings.js")
        translate_decls(declarations, writer)
        writer.close()
    except CommandLineArgumentError as e:
        print(USAGE)
    except Exception as e:
        print(f"An unexpected error occured {e}")
        traceback.print_exc()



