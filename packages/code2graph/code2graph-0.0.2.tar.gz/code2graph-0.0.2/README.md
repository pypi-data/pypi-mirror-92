# Code2graph
This repo contains a project for creating a directed graph from python files in a specific destination. The code2graph generates a dot files that can be visualized by Graphviz (or any other application). If you want code2graph also can generate an svg/png file but if your host machine doesn't have enough memory it will face problems to visualize huge projects. 

Each node in the graph is a function in the python files and it points to all other functions/libraries that have been used in that function. 

## NOTE:
This project has been tested only on Linux and not on Windows or Mac.

# Usage
```bash
$ code2graph.py -h
Usage:
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

# Example usage:
$ code2graph.py /home/user/workspace/code2graph/sample_graph/ --png --scope all
```
The above example usage will generate one dot file and one png file for each python file in the `sample_graph` directory and in addition to that it will also generate one dot file and one png file for all the python files in that directroy which you can see here as an example:
![c2g-project](c2g-project.png)
