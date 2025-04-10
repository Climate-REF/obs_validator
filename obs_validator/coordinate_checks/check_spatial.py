import xarray as xr


### Need to split this up (placeholder function from ILAMB)
def lat_dim(ds: xr.Dataset) -> xr.Dataset:
        """
        """
        # Check that the dataset has a properly set-up latitude dimension
        lat_names = {"lat", "latitude", "y"}
        dims = ds.dims
        dims_lower = {
            dim.lower(): dim for dim in dims
        }  # Map lowercased dims to original names
        lat_names_found = [
            dims_lower[name.lower()] for name in lat_names if name.lower() in dims_lower
        ]

        # Ensure there is only one latitude dimension
        if len(lat_names_found) != 1:
            raise ValueError(
                f"Dataset has {len(lat_names_found)} latitude dimensions, expected exactly one. Found: {lat_names_found}"
            )

        lat_name = lat_names_found[0]

        # Check that one of the accepted latitude long_names exists
        lat_var = ds[lat_name]
        lat_attrs = lat_var.attrs

        # Check for missing latitude attributes
        missing = set(["axis", "long_name", "standard_name", "units"]) - set(lat_attrs)
        if missing:
            raise ValueError(
                f"Dataset is missing latitude-specific attributes, {missing=}"
            )
        else:
            # Check axis
            if lat_attrs["axis"] != "Y":
                raise ValueError(
                    f"Incorrect latitude axis attribute: {lat_attrs['axis']}. Expected 'Y' (case sensitive)."
                )
            # Check standard_name
            if lat_attrs["standard_name"] != "latitude":
                raise ValueError(
                    f"Incorrect latitude standard_name attribute: {lat_attrs['standard_name']}. Expected 'latitude' (case sensitive)."
                )
            # Check units
            valid_lat_units = {
                "degrees_north",
                "degree_north",
                "degree_N",
                "degrees_N",
                "degreeN",
                "degreesN",
            }
            lat_units = lat_attrs.get("units")
            if lat_units not in valid_lat_units:
                raise ValueError(
                    f"Invalid 'units' attribute for latitude dimension. Found: {lat_units}. Expected one of {valid_lat_units}."
                )

        return ds


### Need to split this up (placeholder function from ILAMB)     
def lon_dim(ds: xr.Dataset) -> xr.Dataset:
        """
        """
        # Check that the dataset has a properly set-up longitude dimension
        lon_names = {"lon", "longitude", "x"}
        dims = ds.dims
        dims_lower = {
            dim.lower(): dim for dim in dims
        }  # Map lowercased dims to original names
        lon_names_found = [
            dims_lower[name.lower()] for name in lon_names if name.lower() in dims_lower
        ]

        # Ensure there is only one longitude dimension
        if len(lon_names_found) != 1:
            raise ValueError(
                f"Dataset has {len(lon_names_found)} longitude dimensions, expected exactly one. Found: {lon_names_found}"
            )

        lon_name = lon_names_found[0]

        # Check that one of the accepted longitude long_names exists
        lon_var = ds[lon_name]
        lon_attrs = lon_var.attrs

        # Check for missing longitude attributes
        missing = set(["axis", "long_name", "standard_name", "units"]) - set(lon_attrs)
        if missing:
            raise ValueError(
                f"Dataset is missing longitude-specific attributes, {missing=}"
            )
        else:
            # Check axis
            if lon_attrs["axis"] != "X":
                raise ValueError(
                    f"Incorrect latitude axis attribute: {lon_attrs['axis']}. Expected 'X' (case sensitive)"
                )
            # Check standard_name
            if lon_attrs["standard_name"] != "longitude":
                raise ValueError(
                    f"Incorrect latitude standard_name attribute: {lon_attrs['standard_name']}. Expected 'longitude' (case sensitive)"
                )

            # Check units
            valid_lon_units = {
                "degrees_east",
                "degree_east",
                "degree_E",
                "degrees_E",
                "degreeE",
                "degreesE",
            }
            lon_units = lon_attrs.get("units")
            if lon_units not in valid_lon_units:
                raise ValueError(
                    f"Invalid 'units' attribute for longitude dimension. Found: {lon_units}. Expected one of {valid_lon_units}."
                )

        return ds
