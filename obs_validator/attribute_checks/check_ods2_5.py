import xarray as xr
import re
from datetime import datetime
import uuid
from ..utils.load_CVs import *

def check_attr_existence(ds: xr.Dataset) -> xr.Dataset:
    """Checks whether global attributes required by 
    ODS2.5 exist in the file.
    """
    # Check that the dataset has the required global attribute keys
    missing = set(
        [
                "activity_id",
                #"aux_variable_id",
                "contact",
                "Conventions",
                "creation_date",
                "dataset_contributor",
                "data_specs_version",
                "doi",
                "frequency",
                "grid",
                "grid_label", 
                "has_auxdata",
                "history",
                "institution",
                "institution_id",
                "license",
                "nominal_resolution",
                "processing_code_location",
                "product",
                "realm",
                "references",
                "region",
                "source",
                "source_id",
                #"source_data_retrieval_date",
                "source_data_url",
                "source_label",
                "source_type",
                "source_version_number",
                "title",
                "tracking_id",
                "variable_id",
                "variant_label",
                "variant_info"
            ]
    ) - set(ds.attrs.keys())
    if missing:
        raise ValueError(
            f"Dataset does not properly encode global attributes, {missing=}"
        )
    return ds
    
def check_tracking_id(ds: xr.Dataset) -> xr.Dataset:
    """Checks whether tracking_id format adheres to 
    CMIP and ODS2.5 standards.
    """
    print(ds.attrs['tracking_id'], len(ds.attrs['tracking_id']))
    #assert len(ds.attrs['tracking_id']) == 49
    assert uuid.UUID(ds.attrs['tracking_id'][-36:], version=4) 
    #assert ds.attrs['tracking_id'][:-36] == "hdl:21.14102/" 
    return ds


def check_source_id(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether source_id given in the file metadata
    matches a unique source_id given in the obs4MIPs-CMOR-tables.
    """
    source_id_cv = load_json_from_url(url + "obs4MIPs_source_id.json")
    assert ds.attrs['source_id'] in source_id_cv['source_id']
    assert ds.attrs['source_label'] == source_id_cv['source_id'][ds.attrs['source_id']]['source_label']
    return ds


def check_source_type(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks source type given in the file metadata
    matches a unique source type given in the obs4MIPs-CMOR-tables.
    """
    sourcet_cv = load_json_from_url(url + "obs4MIPs_source_type.json")
    assert ds.attrs['source_type'] in sourcet_cv['source_type']
    return ds


def check_activity_id(ds: xr.Dataset) -> xr.Dataset:
    """Checks activity_id is "obs4MIPs".
    """
    assert ds.attrs['activity_id'] == 'obs4MIPs'
    return ds
    
    
def check_creation_date(ds: xr.Dataset) -> xr.Dataset:
    """Check format of creation data follows the format 
    given in ODS2.5: YYYY-MM-DDTHH:MM:SSZ
    """
    assert datetime.strptime(ds.attrs['creation_date'], "%Y-%m-%dT%H:%M:%SZ")
    return ds


def check_institution_id(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether institution_id given in the file metadata
    matches a unique institution_id given in the obs4MIPs-CMOR-tables.
    """
    inst_id_cv = load_json_from_url(url + "obs4MIPs_institution_id.json")
    assert ds.attrs['institution_id'] in inst_id_cv['institution_id']
    assert ds.attrs['institution'] == inst_id_cv['institution_id'][ds.attrs['institution_id']]
    return ds


def check_region(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether region given in the file metadata
    matches a unique region given in the obs4MIPs-CMOR-tables.
    """
    reg_cv = load_json_from_url(url + "obs4MIPs_region.json")
    assert ds.attrs['region'] in reg_cv['region']
    return ds

def check_freq(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether frequency given in the file metadata
    matches a unique frequency given in the obs4MIPs-CMOR-tables.
    """
    freq_cv = load_json_from_url(url + "obs4MIPs_frequency.json")
    assert ds.attrs['frequency'] in freq_cv['frequency']['frequency']
    return ds


def check_nomres(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether nominal resolution given in the file metadata
    matches a unique nominal resolution given in the obs4MIPs-CMOR-tables.
    """
    nomres_cv = load_json_from_url(url + "obs4MIPs_nominal_resolution.json")
    assert ds.attrs['nominal_resolution'] in nomres_cv['nominal_resolution']['nominal_resolution']
    return ds


def check_grid(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks whether grid label given in the file metadata
    matches a unique grid label given in the obs4MIPs-CMOR-tables.
    """
    grid_cv = load_json_from_url(url + "obs4MIPs_grid_label.json")
    assert ds.attrs['grid_label'] in grid_cv['grid_label']['grid_label']
    return ds
    
    
def check_product(ds: xr.Dataset, url: str) -> xr.Dataset:
    """Checks product attribute given in the file metadata
    matches a unique product given in the obs4MIPs-CMOR-tables.
    """
    product_cv = load_json_from_url(url + "obs4MIPs_product.json")
    assert ds.attrs['product'] in product_cv['product']
    return ds
    

def check_doi(ds: xr.Dataset) -> xr.Dataset:
    """Checks whether doi is following a 
    """
    doi_pattern = r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$'
    assert re.match(doi_pattern, ds.attrs['doi'], re.IGNORECASE) is not None, f'"{ds.attrs['doi']}" does not match expected DOI pattern'
    return ds
