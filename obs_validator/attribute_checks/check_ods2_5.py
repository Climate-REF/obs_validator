import xarray as xr
import uuid
from ..utils.load_CVs import *

def check_attr_existence(ds: xr.Dataset) -> xr.Dataset:
    """
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
    """
    """
    assert len(ds.attrs['tracking_id']) == 49
    assert uuid.UUID(ds.attrs['tracking_id'][-36:], version=4) 
    assert ds.attrs['tracking_id'][:-36] == "hdl:21.14102/" 
    return ds


def check_source_id(ds: xr.Dataset, url: str) -> xr.Dataset:
    """
    """
    source_id_cv = load_json_from_url(url + "obs4MIPs_source_id.json")
    if ds.attrs['source_id'] not in source_id_cv['source_id']:
        errors.append("source_id must match a key in obs4MIPs_source_id.json")
    return ds

#def check_activity_id(ds: xr.Dataset, url: str) -> xr.Dataset:


#def check_institution_id():
