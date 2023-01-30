import argparse
import sys
import os
import shutil
import json

import numpy as np
import pandas as pd
import pytest

import pydicom
from rt_utils import RTStructBuilder
import surface_distance as sd

import Hausdorff_Dice

# FIXME non va
# config_path = r"C:\Users\Marco\Desktop\università\Magistrale\software_and_computing\tests.json"
# # Opening the json file where the lists of names are stored.
# fd = open(config_path)
# config = json.load(fd)


#TODO trova un modo migliore
empty_folder = r"C:\Users\Marco\Desktop\università\Magistrale\software_and_computing\tests\test_is_empty\empty_folder"
non_empty_folder = r"C:\Users\Marco\Desktop\università\Magistrale\software_and_computing\tests\test_is_empty\non_empty_folder"
rtstruct_file_path = r"C:\Users\Marco\Desktop\università\Magistrale\software_and_computing\tests\test_patient_info\RTSTRUCT\RS1.2.752.243.1.1.20230123144246076.4000.75633.dcm"
ct_folder_path = r"C:\Users\Marco\Desktop\università\Magistrale\software_and_computing\tests\test_voxel_spacing\CT"

def test_is_empty_with_empty_folder():
    """
    This test checks if the function is_empty returns 1 when an empty folder
    is given as parameter.

    Returns
    -------
    None.

    """
    assert Hausdorff_Dice.is_empty(empty_folder) == 1
    
def test_is_empty_with_non_empty_folder():
    """
    This test checks if the function is_empty returns 0 when a non empty
    folder is given as parameter.

    Returns
    -------
    None.

    """
    assert Hausdorff_Dice.is_empty(non_empty_folder) == 0
    
def test_patient_info_with_patient_id():
    """
    This test checks that the function patient_info returns a string when
    information is equal to PatientID.
    Returns
    -------
    None.

    """
    info = Hausdorff_Dice.patient_info(rtstruct_file_path,
                                       "PatientID",
                                       )
    assert type(info) == str
    
def test_patient_info_with_frame_of_reference_uid():
    """
    This test checks that the function patient_info returns a uid object
    when information is equal to FrameOfReferenceUID.

    Returns
    -------
    None.

    """
    info = Hausdorff_Dice.patient_info(rtstruct_file_path,
                                       "FrameOfReferenceUID",
                                       )
    assert type(info) == pydicom.uid.UID
    
def test_voxel_spacing_has_three_elements():
    """
    This test checks that the function voxel_spacing returns a list of three
    elements.

    Returns
    -------
    None.

    """
    assert len(Hausdorff_Dice.voxel_spacing(ct_folder_path)) == 3

def test_extract_manual_segments_has_five_elements():
    """
    This test checks that the function voxel_spacing returns a list of five
    elements.

    Returns
    -------
    None.

    """
    patient_data = RTStructBuilder.create_from(ct_folder_path, 
                                               rtstruct_file_path,
                                               )
    alias_names = ["Prostate",
                   "Rectum",
                   "Bladder",
                   "Femoral head (left)",
                   "Femoral head right",
                   ]
    mbs_segments = ["Prostate_MBS",
                    "Rectum_MBS",
                    "Bladder_MBS",
                    "FemoralHead (Left)_MBS",
                    "FemoralHead (Right)_MBS",
                    ]
    dl_segments = ["Prostate_DL",
                   "Anorectum_DL",
                   "Bladder_DL",
                   "Femur_Head_L_DL",
                   "Femur_Head_R_DL",
                   ]
    config_path = r"C:\Users\Marco\Desktop\università\Magistrale\software_and_computing\project\config.json"
    fd = open(config_path)
    config = json.load(fd)
    
    manual_segments = Hausdorff_Dice.extract_manual_segments(patient_data,
                                                             alias_names,
                                                             mbs_segments,
                                                             dl_segments,
                                                             config,
                                                             )
    assert len(manual_segments) == 5
    
def test_compute_metrics_returns_float():
    """
    This funtion checks that the three values returned by compute_metrics are
    all of type float.

    Returns
    -------
    None.

    """
    patient_data = RTStructBuilder.create_from(ct_folder_path, 
                                               rtstruct_file_path,
                                               )
    reference_segment = "Bladder_MBS"
    segment_to_compare = "Bladder_DL"
    voxel_spacing_mm = [1, 1, 3]
    sdsc, dsc, hd = Hausdorff_Dice.compute_metrics(patient_data,
                                                   reference_segment,
                                                   segment_to_compare,
                                                   voxel_spacing_mm,
                                                   )
    assert type(sdsc) == np.float64
    assert type(dsc) == np.float64
    assert type(sdsc) == np.float64