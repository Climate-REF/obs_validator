import urllib.request
import json
import xarray as xr


def load_json_from_url(url:str) -> dict:
    """
    """
    with urllib.request.urlopen(url) as response:
        return json.load(response)
 
            
def get_nested_dict(data: dict, path: str, default=None) -> dict:
    """
    """
    for key in path:
        try:
            if isinstance(data, dict):
                    data = data.get(key, default)
            elif isinstance(data, list) and isinstance(key, int):
                    data = data[key]
            else:
                return default
        except (IndexError, TypeError):
            return default
    return data


def select_MIP_table(url:str, ds: xr.Dataset) -> xr.Dataset:
    """
    """
    if ds.attrs['frequency'] == 'mon':
        if ds.attrs['realm'] == 'atmos':
            mip_table = 'Tables/obs4MIPs_Amon.json'
        elif ds.attrs['realm'] == 'land':
            mip_table = 'Tables/obs4MIPs_Lmon.json'
        elif ds.attrs['realm'] == 'ocean':
            mip_table = 'Tables/obs4MIPs_Omon.json'
        elif ds.attrs['realm'] == 'seaIce':
            mip_table = 'Tables/obs4MIPs_SImon.json'

    assert ds.attrs['variable_id'] in get_nested_dict(load_json_from_url(url + mip_table), ["variable_entry"])
    return load_json_from_url(url + mip_table)


def select_coord_table(url:str, ds: xr.Dataset) -> xr.Dataset:
    """
    """
    return load_json_from_url(url + 'Tables/obs4MIPs_coordinate.json')['axis_entry']
