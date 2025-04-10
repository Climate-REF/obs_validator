import xarray as xr
from cfunits import Units
from ..utils.load_CVs import *


def check_var_existence(ds: xr.Dataset) -> xr.Dataset:
    """Checks whether any data variables exist and 
    that only one data variable (excluding ancillary 
    and boundary variables) exists in the file"""
    # Check that there are data variables
    if not ds.data_vars:
        raise ValueError(
            "Dataset does not have any data variables."
        )
    # Check that the dataset has at least one variable but not more than 2
    if len([var for var in ds.data_vars if '_' not in var]) >= 2:
        raise ValueError(
            f"Dataset has too many data variables {ds.data_vars}. There should be one netCDF file per data variable if a dataset has multiple data variables."
        )
    return ds


def check_unit_existence(ds: xr.Dataset) -> xr.Dataset:
    """Checks that the data variable has a units attribute"""
    if not ds[ds.attrs['variable_id']].attrs['units']:
        raise KeyError(
                f"Dataset has no units associated with the data variables."
            )
    return ds

      
def check_units(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether the units for the data variable
    match the units given in the obs4MIPs MIP table
    for the variable"""
    mip_table = select_MIP_table(url, ds)
    varattrs = get_nested_dict(mip_table, ["variable_entry"])[ds.attrs['variable_id']]
    assert Units(varattrs['units']).equals(Units(ds[ds.attrs['variable_id']].attrs['units']))
    return ds


def check_var_attrs(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether the variable attributes 'standard_name', 
    'long_name', 'units', 'comment', 'cell_methods', 
    'cell_measures' match those given in the obs4MIPs MIP table.
    Additonal check for 'positive' attribute if relevant"""
    mip_table = select_MIP_table(url, ds)
    varattrs = get_nested_dict(mip_table, ["variable_entry"])[ds.attrs['variable_id']]
    if varattrs['positive']:
        assert ds[ds.attrs['variable_id']].attrs['positive'] == varattrs['positive']
        assert ds[ds.attrs['variable_id']].attrs['positive']
    for attr in ['standard_name', 'long_name', 'units', 'comment', 'cell_methods', 'cell_measures']:  
        assert attr in ds[ds.attrs['variable_id']].attrs 
    return ds
  
    
def check_var_dims(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether the dimensions of the data variable
    match those given in the obs4MIPs MIP table."""
    mip_table = select_MIP_table(url, ds)
    varattrs = get_nested_dict(mip_table, ["variable_entry"])[ds.attrs['variable_id']]
    dim_entries = varattrs['dimensions'].split (' ')
    mip_coord = select_coord_table(url, ds)
    for dim in dim_entries:
        if not mip_coord[dim]['out_name'] in list(ds[ds.attrs['variable_id']].dims):
            raise KeyError(
                f"Dataset variable is missing dimension /'{mip_coord[dim]['out_name']}/'"
            )
    return ds


def check_var_freq(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether the frequency attribute
    match that given in the obs4MIPs MIP table."""
    mip_table = select_MIP_table(url, ds)
    varattrs = get_nested_dict(mip_table, ["variable_entry"])[ds.attrs['variable_id']]
    freq = varattrs['frequency']
    if freq != ds.attrs['frequency']:
        raise KeyError(
            f"Frequency associated with MIP variable /'{freq}/' does not match dataset frequency attribute /'{ds.attrs['frequency']}/'"
        )
    return ds


def check_var_realm(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether the realm attribute
    match one of the realms given in the obs4MIPs MIP table."""
    mip_table = select_MIP_table(url, ds)
    varattrs = get_nested_dict(mip_table, ["variable_entry"])[ds.attrs['variable_id']]
    realm_entries = varattrs['modeling_realm'].split (' ')
    if not ds.attrs['realm'] in realm_entries:
            raise KeyError(
                f"Realms associated with MIP variable /'{realm_entries}/' does not match dataset frequency attribute /'{ds.attrs['realm']}/'"
            )
    return ds
    
    
def check_anc_var(ds: xr.Dataset) -> xr.Dataset:
    """Checks whether the ancillary variables for 
    CMOR-like datasets follow CF standards and 
    have an "ancillary_variables" attribute for 
    if uncertainty information is provided. """
    if ds.attrs['has_auxdata']== True:
        anc_vars = ds.attrs['aux_variable_id'].split(' ')
        if not ds.attrs['cmor_version']:
            assert ds[ds.attrs['variable_id']].attrs['ancillary_variables']
            assert ds[ds.attrs['variable_id']].attrs['ancillary_variables'] == anc_vars
            for var in anc_var:
                assert ds[var] in ds.data_vars
    return ds


def check_fillvalue(ds: xr.Dataset) -> xr.Dataset:
    """Checks whether the fill value attirbtue exists."""
    assert '_FillValue' in ds[ds.attrs['variable_id']].encoding
    return ds
