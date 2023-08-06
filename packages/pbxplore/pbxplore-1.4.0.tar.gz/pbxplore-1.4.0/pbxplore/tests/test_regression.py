#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression tests for PBxplore.

This test suite run the various PBxplore programs with various argument, and
makes sure the output is the expected one. The aim is to check that the
programs are not broken during development.

Be careful this test suite does not test that the output is right. It just
test that the output is the expected one based on a previous version.
"""

# Use print as a function like in python 3


from os import path
from uuid import uuid1
from functools import wraps
import os
import subprocess
import shutil
import sys

import pytest

import MDAnalysis

import matplotlib


try:
    import weblogo
    IS_WEBLOGO = True
except ImportError:
    IS_WEBLOGO = False


here = os.path.abspath(os.path.dirname(__file__))
# Resources for the tests are stored in the following directory
REFDIR = os.path.join(here, "test_data/")


class TemplateTestCase(object):
    """
    Template TestCase class for the other TestCase class to inherit from.

    Children class must overload the `_build_command_line` and the
    `_validate_output` methods.
    """
    def _run_program_and_validate(self, out_run_dir, reference, **kwargs):
        """
        Run the program to test and validate its outputs.
        """
        # Build the command line to run. This relies on the _build_command_line
        # method that is a virtual method, which must be overloaded by the
        # child class.
        command = self._build_command_line(str(out_run_dir), **kwargs)
        print(command)

        # Run the command.
        exe = subprocess.Popen(command,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = exe.communicate()
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))

        # The return code should be 0.
        assert exe.returncode == 0, 'Program exited with a {} code.'.format(
            exe.returncode)

        # Validate the output files. This relies on the _validate_output
        # virtual method.
        self._validate_output(str(out_run_dir), reference, **kwargs)

    def _build_command_line(self, **kwargs):
        """
        Build the command line to run.

        This is a virtual method. It must be overloaded by the child class.
        """
        raise NotImplementedError

    def _validate_output(self, reference, **kwargs):
        """
        Validate the output files.

        This is a virtual method. It must be overloaded by the child class.
        """
        raise NotImplementedError


class TestPBAssign(TemplateTestCase):
    """
    Regression tests for PBAssign.py
    """
    references = ["1BTA", "1AY7", "2LFU", "3ICH"]
    extensions = [".pdb", ".cif.gz"]

    def _run_PBassign(self, out_run_dir, pdbid, extension,
                      multiple=None, indir=REFDIR):
        """
        Run a PBxplore program on a PDBID with the given options.

        `options` is expected to be a list that will be directly passed to
        subprocess, it must not contain the input or output options.
        """
        if multiple is None:
            test_input = path.join(REFDIR, pdbid + extension)
            out_basename = path.join(out_run_dir, pdbid)
            input_args = ['-p', test_input]
        else:
            input_args = []
            for basename in pdbid:
                input_args += ['-p', path.join(REFDIR, basename + extension)]
            out_basename = path.join(out_run_dir, multiple)

        run_list = (['PBassign'] + input_args + ['-o', out_basename + extension])
        exe = subprocess.Popen(run_list,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = exe.communicate()
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))

        return exe.returncode, out_run_dir

    def _test_PBassign_options(self, out_run_dir, basename, extension, outfiles,
                               multiple=None, expected_exit=0):
        out_run_dir = str(out_run_dir)
        if multiple is not None:
            out_name = multiple
        status, out_run_dir = self._run_PBassign(out_run_dir, basename, extension, multiple)
        assert status == expected_exit, \
               'PBassign stoped with a {0} exit code'.format(status)
        assert len(os.listdir(out_run_dir)) == len(outfiles),\
                ('PBassign did not produced the right number of files: '
                 '{0} files produced instead of {1}').format(
                    len(os.listdir(out_run_dir)), len(outfiles))
        out_name = basename if multiple is None else multiple
        for outfile in (template.format(out_name + extension)
                        for template in outfiles):
            test_file = path.join(out_run_dir, outfile)
            ref_file = path.join(REFDIR, outfile)
            _assert_identical_files(test_file, ref_file)

    @pytest.mark.parametrize('reference', references)
    @pytest.mark.parametrize('extension', extensions)
    def test_fasta(self, tmpdir, reference, extension):
        """
        Run PBAssign on PDB files, and check the fasta output.
        """
        self._test_PBassign_options(tmpdir, reference, extension,
                                    ['{0}.PB.fasta'])

    @pytest.mark.parametrize('extension', extensions)
    def test_multiple_inputs(self, tmpdir, extension):
        """
        Run PBassign with multiple inputs.
        """
        self._test_PBassign_options(tmpdir, self.references, extension,
                                    ['{0}.PB.fasta'], multiple='all')

    def test_xtc_input(self, tmpdir):
        """
        Run PBassign on a trajectory in the XTC format.

        This test should produce the righ output with python 2. With python 3,
        PBassign should fail as MDanalysis is not available.
        """
        name = 'barstar_md_traj'
        out_run_dir = str(tmpdir)
        output_fname = name + '.PB.fasta'
        call_list = ['PBassign',
                     '-x', os.path.join(REFDIR, name + '.xtc'),
                     '-g', os.path.join(REFDIR, name + '.gro'),
                     '-o', os.path.join(out_run_dir, name)]
        exe = subprocess.Popen(call_list,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        out, err = exe.communicate()
        status = exe.wait()
        print(out.decode('utf-8'))
        print(err.decode('utf-8'))

        # MDanalysis is available, PBassign should run and produce the
        # correct output
        assert status == 0, 'PBassign exited with an error'
        _assert_identical_files(os.path.join(REFDIR, output_fname),
                                os.path.join(out_run_dir, output_fname))


    @pytest.mark.xfail(strict=True, raises=AssertionError)
    def test_different_outputs(self, tmpdir):
        """
        Test if the tests properly fail if an output content is different from
        expected.
        """
        reference = "test_fail"
        extension = ".pdb"
        self._test_PBassign_options(tmpdir, reference, extension, ['{0}.PB.fasta'])


class TestPBcount(TemplateTestCase):
    """
    Test running PBcount.
    """
    def _build_command_line(self, out_run_dir, input_files, output, first_residue=None):
        output_full_path = os.path.join(out_run_dir, output)
        command = ['PBcount', '-o', output_full_path]
        for input_file in input_files:
            command += ['-f', os.path.join(REFDIR, input_file)]
        if first_residue is not None:
            command += ['--first-residue', str(first_residue)]
        return command

    def _validate_output(self, out_run_dir, reference, output, **kwargs):
        reference_full_path = os.path.join(REFDIR, reference)
        output_full_path = os.path.join(out_run_dir,
                                        output + '.PB.count')
        _assert_identical_files(output_full_path, reference_full_path)

    def test_single_file_single_model(self, tmpdir):
        """
        Run PBcount with a single input file that contains a single model.
        """
        input_files = ['count_single1.PB.fasta', ]
        output = 'output'
        reference = 'count_single1.PB.count'
        self._run_program_and_validate(tmpdir, reference,
                                       input_files=input_files, output=output)

    def test_single_file_multiple_models(self, tmpdir):
        """
        Run PBcount with a single input file that contains multiple models.
        """
        input_files = ['count_multi1.PB.fasta', ]
        output = 'output'
        reference = 'count_multi1.PB.count'
        self._run_program_and_validate(tmpdir, reference,
                                       input_files=input_files, output=output)

    def test_multiple_files_single_model(self, tmpdir):
        """
        Run PBcount with multiple input files that contain a single model.
        """
        input_files = ['count_single1.PB.fasta',
                       'count_single2.PB.fasta',
                       'count_single3.PB.fasta']
        output = 'output'
        reference = 'count_single123.PB.count'
        self._run_program_and_validate(tmpdir, reference,
                                       input_files=input_files, output=output)

    def test_multiple_files_multiple_models(self, tmpdir):
        """
        Run PBcount with multiple input files that contain multiple models each.
        """
        input_files = ['count_multi1.PB.fasta',
                       'count_multi2.PB.fasta',
                       'count_multi3.PB.fasta']
        output = 'output'
        reference = 'count_multi123.PB.count'
        self._run_program_and_validate(tmpdir, reference,
                                       input_files=input_files, output=output)

    def test_first_residue_positive(self, tmpdir):
        """
        Test PBcount on with the --first-residue option and a positive value.
        """
        input_files = ['count_multi1.PB.fasta',
                       'count_multi2.PB.fasta',
                       'count_multi3.PB.fasta']
        output = 'output'
        reference = 'count_multi123_first20.PB.count'
        self._run_program_and_validate(tmpdir, reference,
                                       input_files=input_files, output=output,
                                       first_residue=20)

    def test_first_residue_negative(self, tmpdir):
        """
        Test PBcount on with the --first-residue option and a negative value.
        """
        input_files = ['count_multi1.PB.fasta',
                       'count_multi2.PB.fasta',
                       'count_multi3.PB.fasta']
        output = 'output'
        reference = 'count_multi123_first-20.PB.count'
        self._run_program_and_validate(tmpdir, reference,
                                       input_files=input_files, output=output,
                                       first_residue=-20)



class TestPBstat(TemplateTestCase):
    def _build_command_line(self, out_run_dir, input_file, output,
                            mapdist=False, neq=False,
                            logo=False, image_format=None,
                            residue_min=None, residue_max=None):
        input_full_path = os.path.join(REFDIR, input_file)
        output_full_path = os.path.join(str(out_run_dir), output)
        command = ['PBstat', '-f', input_full_path, '-o', output_full_path]
        if mapdist:
            command += ['--map']
        if neq:
            command += ['--neq']
        if logo:
            command += ['--logo']
        if image_format is not None:
            command += ['--image-format', image_format]
        if residue_min is not None:
            command += ['--residue-min', str(residue_min)]
        if residue_max is not None:
            command += ['--residue-max', str(residue_max)]

        return command

    def _validate_output(self, out_run_dir, reference, input_file, output,
                         mapdist=False, neq=False, logo=False, image_format=None,
                         residue_min=None, residue_max=None, **kwargs):

        suffix_residue = ''
        if residue_min or residue_max:
            suffix_residue = ".{}-{}".format(residue_min, residue_max)

        suffix_args = ''
        extension = '.png'
        if neq:
            suffix_args = '.Neq'
        if mapdist:
            suffix_args = '.map'
        if logo:
            suffix_args = '.logo'
        if image_format is None:
            extension = '.png'
        else:
            extension = '.' + image_format

        reference_full_path = os.path.join(REFDIR, reference + '.PB'
                                           + suffix_args + suffix_residue)
        output = os.path.join(str(out_run_dir), output)
        output_full_path = output + '.PB' + suffix_args + suffix_residue

        if neq:
            # Assess the validity of the Neq file
            _assert_identical_files(output_full_path, reference_full_path)

        # Assess the creation of the graph file (png or pdf)
        value, msg = _file_validity(output_full_path + extension)
        assert value, msg

    def test_neq(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       neq=True)
        self._run_program_and_validate(tmpdir,
                                       reference='count_single123',
                                       input_file='count_single123.PB.count',
                                       output='output',
                                       neq=True)

    def test_neq_with_range_residues(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       neq=True,
                                       residue_min=10, residue_max=30)

    def test_neq_with_first_residue(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123_first20',
                                       input_file='count_multi123_first20.PB.count',
                                       output='output',
                                       neq=True)

    def test_neq_with_first_range_residues(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123_first20',
                                       input_file='count_multi123_first20.PB.count',
                                       output='output',
                                       neq=True,
                                       residue_min=25, residue_max=35)

    def test_neq_pdf(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       neq=True, image_format='pdf')

    def test_mapdist(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       mapdist=True)

    def test_mapdist_pdf(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       mapdist=True, image_format='pdf')

    def test_mapdist_with_range_residues(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       mapdist=True,
                                       residue_min=10, residue_max=30)

    @pytest.mark.skipif(not IS_WEBLOGO, reason="Weblogo is not present")
    def test_weblogo(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       logo=True)

    @pytest.mark.skipif(not IS_WEBLOGO, reason="Weblogo is not present")
    def test_weblogo_logo_pdf(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       logo=True, image_format='pdf')

    @pytest.mark.skipif(not IS_WEBLOGO, reason="Weblogo is not present")
    def test_weblogo_logo_png(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       logo=True, image_format='png')

    @pytest.mark.skipif(not IS_WEBLOGO, reason="Weblogo is not present")
    def test_weblogo_logo_jpg(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       logo=True, image_format='jpg')

    @pytest.mark.skipif(not IS_WEBLOGO, reason="Weblogo is not present")
    @pytest.mark.xfail(strict=True, raises=AssertionError)
    def test_weblogo_logo_invalid_format(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       logo=True, image_format='invalid')

    @pytest.mark.skipif(not IS_WEBLOGO, reason="Weblogo is not present")
    def test_weblogo_with_range_residues(self, tmpdir):
        self._run_program_and_validate(tmpdir,
                                       reference='count_multi123',
                                       input_file='count_multi123.PB.count',
                                       output='output',
                                       logo=True,
                                       residue_min=10, residue_max=30)


def _file_validity(file_a):
    """
    Check wether file_a exists and is not empty.
    Return a tuple containing:
        - True if all went well, False otherwise
        - the error message, empty if True is returned

    """
    if os.path.isfile(file_a):
        if os.path.getsize(file_a) > 0:
            return True, ''
        else:
            return False, '{0} is empty'.format(file_a)
    else:
        return False, '{0} does not exist'.format(file_a)


def _same_file_content(file_a, file_b, comment_char=">"):
    """
    Return True if two files are identical. Take file path as arguments.
    Ignore the content of lines which start with `comment_char`.
    """
    with open(file_a) as f1, open(file_b) as f2:
        # Compare content line by line
        for f1_line, f2_line in zip(f1, f2):
            if (f1_line != f2_line):
                # If both lines start with a comment,
                # it's a valid one no matter the content of the comment
                f1_firstchar = f1_line.strip().startswith(comment_char)
                f2_firstchar = f2_line.strip().startswith(comment_char)
                if f1_firstchar != f2_firstchar:
                    print(file_a, file_b)
                    print(f1_line, f2_line, sep='//')
                    return False
        # Check if one file is longer than the other; it would result as one
        # file iterator not completely consumed
        for infile in (f1, f2):
            try:
                next(infile)
            except StopIteration:
                pass
            else:
                # The iterator is not consumed, it means that this file is
                # longer than the other
                print('File too long')
                return False
    # If we reach this line, it means that we did not find any difference
    return True


def _assert_identical_files(file_a, file_b, comment_char=">"):
    """
    Raise an Assert exception if the two files are not identical.

    Take file path as arguments.
    Ignore the content of lines which start with `comment_char`.
    """
    assert _same_file_content(file_a, file_b), '{0} and {1} are not identical'\
                                               .format(file_a, file_b)
