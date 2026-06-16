import os
import glob
import numpy as np
import torch
import warnings

from astropy.stats import sigma_clip
from astropy.io import ascii
from astropy import units as u

from specutils import Spectrum1D
from specutils.manipulation import box_smooth
from specutils.fitting import fit_generic_continuum

from spectres import spectres

from scale import scale_flux

warnings.filterwarnings("ignore")

def predict(path, final_model, regrid=None):
    if regrid is None:
        regrid = np.arange(4000, 8002, 2)

    resampled_arrays = []
    predictions = []
    filename_array = []

    for file in glob.glob(path):

        data = ascii.read(file, names=['wavelength','flux','error'])

        wavelength = data['wavelength']
        scale = scale_flux(data['flux'])
        flux = data['flux'] / scale

        spectrum = Spectrum1D(
            flux=flux * (u.erg/(u.cm**2)/u.s/u.AA),
            spectral_axis=wavelength * u.AA
        )

        spec1_bsmooth = box_smooth(spectrum, width=6)

        flux_masked = sigma_clip(flux, sigma=3, maxiters=2)
        mask = ~flux_masked.mask

        g1_fit = fit_generic_continuum(
            Spectrum1D(
                flux=spectrum.flux[mask],
                spectral_axis=spectrum.spectral_axis[mask]
            )
        )

        y_continuum_fitted = g1_fit(spectrum.spectral_axis)

        spec_normalized = spec1_bsmooth / y_continuum_fitted

        mm = np.ones_like(wavelength, dtype=bool)
        window = 10

        spec_resample, spec_errs_resample = spectres(
            regrid,
            wavelength[mm],
            spec_normalized.flux[mm],
            spec_errs=data['error'][mm] / scale
        )

        ## interpolate/extrapolate where resampled fluxes are NAN; not treating the resampled error bars though
        mask = np.isnan(spec_resample)
        spec_resample[mask] = np.interp(
            regrid[mask],
            regrid[~mask],
            spec_resample[~mask]
        )

        # edge handling
        mask_hi = regrid > max(wavelength)
        spec_resample[mask_hi] = np.median(spec_normalized.flux[-window:])

        mask_lo = regrid < min(wavelength)
        spec_resample[mask_lo] = np.median(spec_normalized.flux[:window])

        resampled_arrays.append(spec_resample)

        filename_array.append(os.path.basename(file))

        # normalize
        mean = np.mean(spec_resample)
        std = np.std(spec_resample)
        spec_resample = (spec_resample - mean) / std

        X = torch.tensor(spec_resample, dtype=torch.float32)

        with torch.no_grad():
            output = final_model(X)
            pred = int(torch.round(torch.sigmoid(output)).item())
            predictions.append(pred)

    return filename_array, resampled_arrays, predictions