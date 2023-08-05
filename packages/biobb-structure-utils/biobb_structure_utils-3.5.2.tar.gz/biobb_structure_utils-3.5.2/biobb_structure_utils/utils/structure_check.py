#!/usr/bin/env python3

"""Module containing the StructureCheck class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.utils.common import *

class StructureCheck():
    """
    | biobb_structure_utils StructureCheck
    | This class is a wrapper of the Structure Checking tool to generate summary checking results on a json file.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to generate summary checking results on a json file from a given structure and a list of features.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_summary_path (str): Output summary checking results. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/summary.json>`_. Accepted formats: json (edam:format_3464).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **features** (*list*) - (None) Features to summarize. If None, all the features will be computed. Values: models (multiple molecules or coordinate sets in a single file), chains (multiple chains in a single file), altloc (atom alternative conformation given an alternate location indicator and occupancy), metals (metals present in the structure), ligands (heteroatoms present in the structure), chiral (to say that a structure is chiral is to say that its mirror image is not the same as it self), getss (detect SS bonds or disulfides), cistransbck (detact cis/trans backbone), backbone (detect backbone breaks), amide (detect too close amides), clashes (detect clashes).
            * **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.structure_check import structure_check
            prop = { 
                'features': ['models', 'chains', 'ligands']
            }
            structure_check(input_structure_path='/path/to/myInputStr.pdb, 
                            output_summary_path='/path/to/newSummary.json', 
                            properties=prop)

    Info:
        * wrapped_software:
            * name: Structure Checking from MDWeb
            * version: >=3.0.3
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
            
    """

    def __init__(self, input_structure_path, 
                 output_summary_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = str(input_structure_path)
        self.output_summary_path = str(output_summary_path)

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')
        self.features = properties.get('features', None)
        self.properties = properties

        # Common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    def check_data_params(self, out_log, err_log):
        """ Checks all the input/output paths and parameters """
        self.input_structure_path = check_input_path(self.input_structure_path, out_log, self.__class__.__name__)
        self.output_summary_path = check_output_path_json(self.output_summary_path, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`StructureCheck <utils.structure_check.StructureCheck>` utils.structure_check.StructureCheck object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log, err_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_summary_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step,  out_log, self.global_log)
                return 0

        if not self.features:
            fu.log('No features provided, all features will be computed: %s' % 'models, chains, altloc, metals, ligands, chiral, getss, cistransbck, backbone, amide, clashes', out_log)
            self.features = ['models', 'chains', 'altloc', 'metals', 'ligands', 'chiral', 'getss', 'cistransbck', 'backbone', 'amide', 'clashes']
        else: 
            fu.log('Computing features: %s' % ', '.join(self.features), out_log)

        # create temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        command_list = self.tmp_folder + '/command_list.lst'

        with open(command_list, 'w') as f:
            for item in self.features:
                f.write("%s\n" % item)

        # run command line
        cmd = [self.check_structure_path,
               '-i', self.input_structure_path,
               '--json', self.output_summary_path,
               '--check_only',
               '--non_interactive',
               'command_list',
               '--list',
               command_list]

        returncode: int = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        fu.log('File %s created' % self.output_summary_path,  out_log, self.global_log)

        # remove temporary folder
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removing %s temporary folder' % self.tmp_folder, out_log)

        return returncode

def structure_check(input_structure_path: str, output_summary_path: str, properties: dict = None, **kwargs) -> int:
    """Execute the :class:`StructureCheck <utils.structure_check.StructureCheck>` class and
    execute the :meth:`launch() <utils.structure_check.StructureCheck.launch>` method."""

    return StructureCheck(input_structure_path=input_structure_path, 
                                output_summary_path=output_summary_path,
                                properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="This class is a wrapper of the Structure Checking tool to generate summary checking results on a json file.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_structure_path', required=True, help="Input structure file path. Accepted formats: pdb.")
    required_args.add_argument('-o', '--output_summary_path', required=True, help="Output summary checking results. Accepted formats: json.")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    structure_check(input_structure_path=args.input_structure_path, 
                        output_summary_path=args.output_summary_path, 
                        properties=properties)

if __name__ == '__main__':
    main()
