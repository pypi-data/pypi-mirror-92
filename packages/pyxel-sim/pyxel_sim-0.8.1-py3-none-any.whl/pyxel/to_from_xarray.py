import xarray as xr

detector = None


xr.Dataset({"row": xr.DataArray(450, attrs={"unit": "prout"})})


foo = xr.Dataset(
    data_vars={
        # 'geometry': xr.Dataset({'row': xr.DataArray(450, attrs={'unit': 'prout'})}),
        "photon": xr.DataArray(
            detector.photon.array,
            attrs={"unit": "photon"},
            dims=["y", "x"],
        ),
        "charge": xr.DataArray(
            detector.charge.frame,
            attrs={"unit": "electron"},
            dims=["idx_charge", "type_charge"],
        ),
        "pixel": xr.DataArray(
            detector.pixel.array, attrs={"unit": "adu"}, dims=["row", "col"]
        ),
        "signal": xr.DataArray(
            detector.signal.array, attrs={"unit": None}, dims=["row", "col"]
        ),
        "image": xr.DataArray(
            detector.image.array, attrs={"unit": None}, dims=["row", "col"]
        ),
    }
)

detector
