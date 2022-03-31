#!/usr/bin/env python3

import os
import re
import sys
from datetime import datetime
from optparse import OptionParser

# This block need for check uncatchable error from installed library. Don't touch it
try:
    from N2G import yed_diagram
    import openpyxl
except ModuleNotFoundError:
    print(
        "[!] Output from " + __file__ + "\nUnknown error. Please make sure, what you have install "
        "all required libraries from requirements.txt, using command: "
        "pip3 install -r requirements.txt"
    )
    sys.exit(1)

parser = OptionParser()
parser.add_option("-f", "--file", dest="file",
                  help="PATH to file.", metavar="PATH")

(options, args) = parser.parse_args()


def check_for_errors():
    """
        [?] This function using for catch most common erros for launching this script
    """
    if options.file is None or options.file == "":
        print("[!] Output from " + __file__ + "\nYou must specify path to file in --path argument")
        sys.exit(1)
    elif not os.path.exists(options.file):
        print("[!] Output from " + __file__ + "\nFile " + options.file + " not found!")
        sys.exit(1)

    return True


class LogToDictConverter:
    def get_converted_output(self):
        """
            [?] This method return cleaned dictionary from file, specified in
                --file argument for this script
        """
        if check_for_errors():
            output_in_dict = {
                # SW-0-1: ["SW-0-0", "SW-0-1", "SW-0-2", "SW-0-3", "H-1", "H-2", "H-3", "H-4"]
            }
            with open(options.file, "r") as file_r:
                blocks_array = re.findall(r"[^\r\n\s]+[^\r\n]+(?:\r?\n[^\r\n\S]{2,}[^\r\n]+)+", file_r.read())
                if blocks_array is None:
                    print("[!] Output from " + __file__ + "\nSpecified file has incorrect format for parser")
                    sys.exit(1)
                for block in blocks_array:
                    block_params = re.search(r"([^\r\n\s]+)[^\r\n\S]+([^\r\n\s]+)\r?\n", block)
                    connection_from = block_params.group(2)  # SW-1-0
                    connections_array = re.findall(r"[^\r\n\S]{2,}P\d+[^\r\n\S]+[^\r\n]+", block)

                    output_in_dict[connection_from] = []
                    for connection in connections_array:
                        connection_params = re.search(
                            r"(P\d+)[^\r\n\S]+-(\S+)->[^\r\n\S]+(\S+)[^\r\n\S]+(\S+)[^\r\n\S]+(P\d+)",
                            connection
                        )
                        connection_to = connection_params.group(4)  # H-1 or SW-1-0-0
                        if connection_from not in output_in_dict:
                            output_in_dict[connection_from] = []
                        output_in_dict[connection_from].append(connection_to)
            return output_in_dict

    def show_converted_output(self):
        """
            This method only showing cleaned output from
            file in python dictionary format
        """
        print(self.get_converted_output())
        sys.exit(0)


class DisplayScheme:
    """
        [!] Visual C++ required for windows pc.
    """

    def __init__(self, data):
        self.data = data

    def draw_diagram_using_n2g(self):
        """
            [?] This method has a logic for creating a .graphml file from
            dictionary, specified in constructor.
        """
        diagram = yed_diagram()
        for connection_from in self.data:
            for connection_to in self.data[connection_from]:
                diagram.add_node(connection_from)
                diagram.add_node(connection_to)
                diagram.add_link(connection_from, connection_to)
            diagram.dump_file(filename=f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.graphml",
                              folder="./graphml files/")
        print(
            "[+] Output from " + __file__ +
            f"\n{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.graphml successfully saved "
            f"in folder 'graphml files'"
        )
        sys.exit(0)


scheme = DisplayScheme(LogToDictConverter().get_converted_output())
scheme.draw_diagram_using_n2g()
