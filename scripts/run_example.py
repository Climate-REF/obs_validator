import xarray as xr
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from obs_validator import obs4MIPsDataset


#dset = xr.open_dataset()
test = obs4MIPsDataset(filename=sys.argv[1])
test.check_cf_compliance()
test.check_attrs()

test.check_var()
test.check_coords()

