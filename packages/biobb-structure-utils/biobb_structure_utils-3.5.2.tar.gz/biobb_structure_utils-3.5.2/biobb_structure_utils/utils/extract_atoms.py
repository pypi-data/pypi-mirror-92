#!/usr/bin/env python3

"""Module containing the ExtractAtoms class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.gro_lib.gro import Gro
from biobb_structure_utils.utils.common import *

class ExtractAtoms():
    """
    | biobb_structure_utils ExtractAtoms
    | Class to extract atoms from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/OE2_atoms.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **regular_expression_pattern** (*str*) - ("^D") Python style regular expression matching the selected atom names.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.extract_atoms import extract_atoms
            prop = { 
                'regular_expression_pattern': '^D' 
            }
            extract_atoms(input_structure_path='/path/to/myStructure.pdb, 
                        output_structure_path='/path/to/newStructure.pdb', 
                        properties=prop)

    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
            
    """

    def __init__(self, input_structure_path, output_structure_path, 
                properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = str(input_structure_path)
        self.output_structure_path = str(output_structure_path)

        # Properties specific for BB
        self.regular_expression_pattern = properties.get('regular_expression_pattern', '^D')

        # Common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`ExtractAtoms <utils.extract_atoms.ExtractAtoms>` utils.extract_atoms.ExtractAtoms object."""
        
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_structure_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step,  out_log, self.global_log)
                return 0

        extension = Path(self.input_structure_path).suffix.lower()
        if extension.lower() == '.gro':
            fu.log('GRO format detected, extracting all atoms matching %s' % self.regular_expression_pattern, out_log)
            gro_st = Gro()
            gro_st.read_gro_file(self.input_structure_path)
            gro_st.select_atoms(self.regular_expression_pattern)
            if gro_st.num_of_atoms:
                fu.log('%d atoms found writting GRO file' % gro_st.num_of_atoms, out_log, self.global_log)
                gro_st.write_gro_file(self.output_structure_path)
            else:
                fu.log('No matching atoms found writting empty GRO file', out_log, self.global_log)
                open(self.output_structure_path, 'w').close()

        else:
            fu.log('PDB format detected, extracting all atoms matching %s' % self.regular_expression_pattern, out_log)
            # Direct aproach solution implemented to avoid the issues presented in commit message (c92aab9604a6a31d13f4170ff47b231df0a588ef)
            # with the Biopython library
            atoms_match_cont = 0
            with open(self.input_structure_path, "r") as input_pdb, open(self.output_structure_path, "w") as output_pdb:
                for line in input_pdb:
                    record = line[:6].upper().strip()
                    if len(line) > 10 and record in PDB_SERIAL_RECORDS: #Avoid MODEL, ENDMDL records and empty lines
                        pdb_atom_name = line[12:16].strip()
                        if re.search(self.regular_expression_pattern, pdb_atom_name):
                            atoms_match_cont += 1
                            output_pdb.write(line)
            if atoms_match_cont:
                fu.log('%d atoms found writting PDB file' % atoms_match_cont, out_log, self.global_log)
            else:
                fu.log('No matching atoms found writting empty PDB file', out_log, self.global_log)

        if self.remove_tmp:
            fu.rm_file_list(tmp_files)

        return 0

def extract_atoms(input_structure_path: str, output_structure_path: str, properties: dict = None, **kwargs) -> int:
    """Execute the :class:`ExtractAtoms <utils.extract_atoms.ExtractAtoms>` class and
    execute the :meth:`launch() <utils.extract_atoms.ExtractAtoms.launch>` method."""

    return ExtractAtoms(input_structure_path=input_structure_path, 
                    output_structure_path=output_structure_path,
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Remove the selected ligand atoms from a 3D structure.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_structure_path', required=True, help="Input structure file name")
    required_args.add_argument('-o', '--output_structure_path', required=True, help="Output structure file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    extract_atoms(input_structure_path=args.input_structure_path, 
                output_structure_path=args.output_structure_path, 
                properties=properties)

if __name__ == '__main__':
    main()
