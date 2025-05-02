import subprocess
import re
import xarray as xr

def run_cf_check(filename: str, ds: xr.Dataset, standard='cf:1.8'):
    match = re.search(r'cf-1\.\d{1,2}', ds.attrs['Conventions'].lower())
    if match and float(match.group()[5:])<=9:
        standard = match.group()[3:]
        print(f"Found CF version: {standard}")
    else:
        print(f'CF version ({match.group()}) either not found or >1.9 (not yet implemented in compliance checker)') 
    result = subprocess.run(
        ['compliance-checker', '--test=' + standard, filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
