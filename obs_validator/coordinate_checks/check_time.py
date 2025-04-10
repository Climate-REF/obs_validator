import xarray as xr
import numpy as np


### Need to split this up (placeholder function from ILAMB)
def time_dim(ds: xr.Dataset) -> xr.Dataset:
        """
        """
        # Check that the dataset has a properly set-up time dimension
        dimensions = ds.dims
        time_dim_present = "time" in dimensions
        time_var = ds["time"]
        time_attrs = time_var.attrs

        # Check if the time dimension is present
        if not time_dim_present:
            raise ValueError(
                f"Dataset does not have a time dimension, {dimensions=}. Expected a dimension called 'time'."
            )

        # Check if time values are decoded as datetime objects
        time_dtype = type(time_var.values[0])
        if not (
            np.issubdtype(time_var.values.dtype, np.datetime64)
            or isinstance(time_var.values[0], cftime.datetime)
        ):
            raise TypeError(
                f"Time values are not properly decoded as datetime objects: {time_dtype=}"
            )

        # Check time attributes: axis, long_name, standard_name
        missing = set(["axis", "long_name", "standard_name"]) - set(time_attrs)
        if missing:
            raise ValueError(
                f"Dataset is missing time-specific attributes, {missing=}."
            )
        else:
            # Check the axis and standard_name to ensure they're correct; long_name can vary.
            correct_axis_name = time_attrs["axis"] == "T"
            if not correct_axis_name:
                raise TypeError(
                    f"The time dimension's axis attribute is {time_attrs['axis']}. Expected 'T'."
                )
            correct_std_name = time_attrs["standard_name"] == "time"
            if not correct_std_name:
                raise TypeError(
                    f"The time dimension's standard_name attribute is {time_attrs['standard_name']}. Expected 'time'."
                )

        # Check time units encoding and formatting
        time_encoding = time_var.encoding
        if "units" not in time_encoding or "since" not in time_encoding["units"]:
            raise ValueError(
                f"Time encoding is missing or incorrect, {time_encoding=}. Expected 'days since YYYY:MM:DD'"
            )

        # Check time calendar encoding
        if "calendar" in time_encoding:
            valid_calendars = [
                "standard",
                "gregorian",
                "proleptic_gregorian",
                "noleap",
                "all_leap",
                "360_day",
                "julian",
            ]

            if time_encoding["calendar"] not in valid_calendars:
                # Check for explicitly defined calendar attributes
                if "month_lengths" in time_attrs:
                    # Validate month_lengths
                    month_lengths = time_attrs["month_lengths"]
                    if len(month_lengths) != 12 or not all(
                        isinstance(m, (int, np.integer)) for m in month_lengths
                    ):
                        raise ValueError(
                            "month_lengths must be a list of 12 integer values."
                        )

                    # Validate leap year settings if present
                    if "leap_year" in time_attrs:
                        leap_year = time_attrs["leap_year"]
                        if not isinstance(leap_year, (int, np.integer)):
                            raise ValueError("leap_year must be an integer.")

                        if "leap_month" in time_attrs:
                            leap_month = time_attrs["leap_month"]
                            if not (1 <= leap_month <= 12):
                                raise ValueError("leap_month must be between 1 and 12.")
                else:
                    raise ValueError(
                        f"Unrecognized calendar '{time_encoding['calendar']}' and no explicit month_lengths provided."
                    )
        else:
            raise ValueError("Calendar attribute is missing from the time encoding.")

        # Some could be climatologies, no check for now
        if "climatology" in time_attrs:
            return ds

        # Check bounds encoding
        time_bounds_name = time_attrs["bounds"]
        if time_bounds_name not in ds:
            raise ValueError(
                f"Time bounds variable '{time_bounds_name=}' is missing from dataset. Expected 'time_bounds'"
            )

        # Check time_bounds structure
        time_bounds = ds[time_bounds_name]
        if len(time_bounds.dims) != 2 or time_bounds.dims[0] != "time":
            raise ValueError(
                f"Time bounds, '{time_bounds_name=}', has incorrect dimensions, {time_bounds.dims}."
                "Expected two dimensions: ('time', <second_dimension>)."
            )

        # Check that the second dimension length is 2 (indicating time bounds)
        if time_bounds.shape[1] != 2:
            raise ValueError(
                f"Time bounds '{time_bounds_name}' has incorrect shape {time_bounds.shape}. "
                "The second dimension should have length 2 to represent time bounds."
            )

        # Check for the correct 'long_name' attribute for time_bounds
        if (
            "long_name" not in time_bounds.attrs
            or time_bounds.attrs["long_name"] != "time_bounds"
        ):
            raise ValueError(
                f"Time bounds '{time_bounds_name}' is missing its 'long_name':'time_bounds' attribute."
            )

        return ds
