

## Need to remove the factors making the flux values very small -- leads to numerical instability when continuum fitting 
def scale_flux(flux):
    scale_factors = [1.0E-21,1.0E-20,1.0E-19,1.0E-18,1.0E-17,1.0E-16,1.0E-15,1.0E-14,1.0E-13,1.0E-12,1.0E-11,1.0E-10]
    # for file in glob.glob(path):
    #     data = ascii.read(file, names=['wavelength','flux','error'])
    #     flux = data['flux']
    #     if max(flux) < 1.0E-3:
    #         print (file, max(flux))
    #         for i,F in enumerate(scale_factors[1:]):
    #             if max(flux) < F:
    #                 print (f"Use factor {scale_factors[i]}")
    #                 break

    if max(flux) < 1.0E-3:
        for i,F in enumerate(scale_factors[1:]):
            if max(flux) < F:
                return scale_factors[i]
    return 1.0