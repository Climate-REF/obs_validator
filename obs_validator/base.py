"""
A script that checks an input dataset (netCDF file) for adherence to obs4MIPs standards.
"""

import sys
from typing import Literal

import cftime
import numpy as np
import xarray as xr
from pydantic import BaseModel, ConfigDict, field_validator
from .attribute_checks.check_ods2_5 import *
from .variable_checks.check_vars import *
from .coordinate_checks.check_spatial import *
from .cf_checks.check_cf_compliance import *
from compliance_checker.runner import CheckSuite


# spatial validator
class obs4MIPsDataset:
    def __init__(self, filename):
        self.filename = filename
        self.dataset = self.read_dataset()
        self.base_url = "https://raw.githubusercontent.com/PCMDI/obs4MIPs-cmor-tables/master/"

    def read_dataset(self):
        """
        """
        ds = xr.open_dataset(self.filename)
        return ds
    
    def check_cf_compliance(self):
        """
        """
        run_cf_check(self.filename, self.dataset)
        return
        
    def check_attrs(self):
        """
        """
        check_attr_existence(self.dataset)
        check_tracking_id(self.dataset)
        check_source_id(self.dataset, self.base_url)
        check_source_type(self.dataset, self.base_url)
        check_activity_id(self.dataset)
        check_creation_date(self.dataset)
        check_institution_id(self.dataset, self.base_url)
        check_region(self.dataset, self.base_url)
        check_freq(self.dataset, self.base_url)
        check_nomres(self.dataset, self.base_url)
        check_grid(self.dataset, self.base_url)
        check_product(self.dataset, self.base_url)
        #check_doi(self.dataset)
        return 
        
    def check_var(self):
        """
        """
        check_var_existence(self.dataset)
        check_unit_existence(self.dataset)
        check_units(self.dataset, self.base_url)
        check_var_attrs(self.dataset, self.base_url)
        check_var_dims(self.dataset, self.base_url)
        check_var_freq(self.dataset, self.base_url)
        check_var_realm(self.dataset, self.base_url)
        check_anc_var(self.dataset)
        check_fillvalue(self.dataset)
        return 

    def check_coords(self):
        """
        """
        check_dims(self.dataset, self.base_url)
