#!python


"""Usage:
    test.py PATH [ --svg] [ --png] [--scope=<SCP>]
    test.py [ -h | --help ]
    test.py -v

Arguments:
    PATH                The path to directory that you want to generate its graph. This can be the root of a project and code2graph will recursively finds all the python files there or just any directory containing python files. Note: the path must end with "/" for example:("/home/guest/workspace/")

Options:
    -h --help           Show this screen
    --svg               Generates an svg file in addition to the dot files
    --png               Generates a png file in addition to the dot files
    --scope=<SCP>       Defines the scope of the generating graph:
                        file --> graph (dot file + svg/png) will be created only for each python file and will be saved with the same name and at the same path of the file
                        project --> graph (dot file + svg/png) will be created only for the whole project (PATH) and single graphs will not be created for each python file
                        all --> both will be generated [default: all]
    -v                  Version
"""
from docopt import docopt

import os
import glob
import sys

import symtable
from symtable import Function

import pygraphviz as pgv

# =================== GLOBAL VARIABLES ===================
# flag for single file graph
SF = True
# flag for project-wide graph
SP = False
# project-wide graph
G_All = pgv.AGraph(directed=True)

SVG = False
PNG = False

VERSION = "0.0.2"

# =================== Helper Functions ===================
def extract_class(G, G_All, class_name, class_symbol_table):
    """
    This function gets:
    - G: the file graph
    - G_All: the overal graph
    - class_name: the name of class --> we use this to define class functions
    - class_symbol_table: class symbol table (from a class)
    and extracts its graph and returns the graph
    """
    for f in class_symbol_table:
        if (getattr(f, "get_type")())=='class':
            class_name = getattr(f, "get_name")()
            if SF:
                G.add_node(class_name)
            if SP:
                G_All.add_node(class_name)
            continue

        current_node = getattr(f, "get_name")()
        class_current_node = class_name+'.'+current_node
        # print("class_current_node: "+class_current_node)
        if SF:
            G.add_node(class_current_node)
        if SP:
            G_All.add_node(class_current_node)

        used_nodes = getattr(f, "get_globals")()
        # print("used_nodes:")
        for n in used_nodes:
            # print("n: "+n)
            if SF:
                G.add_node(n)
                G.add_edge(class_current_node, n)
            if SP:
                G_All.add_node(n)
                G_All.add_edge(class_current_node, n)



def extractgraph(filepath):
    print('start extracting graph for: '+filepath)
    
    global G_All
    G = pgv.AGraph(directed=True)

    with open(filepath) as f:
        content = f.read()

    table = symtable.symtable(content, "string", "exec")
    for f in table.get_children():
        if (getattr(f, "get_type")())=='class':
            class_name = getattr(f, "get_name")()
            class_symbol_table = getattr(f, "get_children")()
            extract_class(G, G_All, class_name, class_symbol_table)
            if SF:
                G.add_node(class_name)
            if SP:
                G_All.add_node(class_name)
            continue

        current_node = getattr(f, "get_name")()
        if SF:
            G.add_node(current_node)
        if SP:
            G_All.add_node(current_node)

        used_nodes = getattr(f, "get_globals")()
        for n in used_nodes:
            if SF:
                G.add_node(n)
                G.add_edge(current_node, n)
            if SP:
                G_All.add_node(n)
                G_All.add_edge(current_node, n)

    if SF:
        G.layout(prog='dot')
        G.write(filepath+'-graph.dot')
        if SVG:
            G.draw(filepath+'-graph.svg')
        if PNG:
            G.draw(filepath+'-graph.png')



# =================== Main Functions ===================
if __name__ == '__main__':
    args = docopt(__doc__)
    # print(args)

    if args['-v']:
        print("Code2graph version "+VERSION)
        exit()
    
    if args['--svg']:
        SVG = True
    if args['--png']:
        PNG = True
    
    if args['--scope']=='file':
        print("Scope file selected")
    elif args['--scope']=='project':
        print("Scope project selected")
        SP = True
        SF = False
    elif args['--scope']=='all':
        print("Scope all selected")
        SP = True
        SF = True

    diraddress = args['PATH']

    for filename in glob.iglob(diraddress + '**/**', recursive=True):
        if os.path.isfile(filename):
            if filename.split('.')[-1] == 'py':
                extractgraph(filename)

    G_All.layout(prog='dot')
    if SP:
        G_All.write(diraddress+'/c2g-project.dot')
        if SVG:
            print("generating svg and saving it at "+diraddress)
            G_All.draw(diraddress+'/c2g-project.svg')
        if PNG:
            print("generating png and saving it at "+diraddress)
            G_All.draw(diraddress+'/c2g-project.png')
    
    print("End.")