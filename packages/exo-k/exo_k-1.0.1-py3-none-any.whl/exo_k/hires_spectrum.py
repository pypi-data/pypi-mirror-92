# -*- coding: utf-8 -*-
"""
@author: jeremy leconte
"""
import os.path
import numpy as np
import h5py
from exo_k.util.interp import rm_molec,unit_convert
from exo_k.settings import Settings
from exo_k.util.filenames import select_kwargs
from .util.spectral_object import Spectral_object
from .util.cst import KBOLTZ, N_A

class Hires_spectrum(Spectral_object):
    """A class defining a Hires_spectrum object.
    """

    def __init__(self, filename, file_kdata_unit='unspecified', kdata_unit='unspecified',
        mult_factor=None, binary=False, **kwargs):
        """Reads a high-resolution spectrum from a file (either hdf5 or ascii).

        Parameters
        ----------
            filename: str
                Full pathname to the file. Extension defines the format used.
            file_kdata_unit: str
                Specifies the unit for the opacity data in the file. This is needed
                for ascii formats as the units are not known.
                The type of quantity may differ whether we are handling cross sections (surface)
                or absorption coefficients (inverse length)
            kdata_unit: str
                Unit to convert to.
            mult_factor: float
                A multiplicative factor that can be applied to kdata (for example to correct for
                any dilution effect, or specific conversion).
        
        see :func:`read_ascii` for additional arguments to use with ascii files
        """
        
        self.filename=None
        self.kdata=None
        self.kdata_unit='unspecified'
        self.wns=None
        self.wn_unit='cm^-1'
        self.data_type=None # 'xsec' or 'abs_coeff'

        if filename.lower().endswith(('.hdf5', '.h5')):
            self.read_hdf5(filename)
        elif binary:
            self.read_binary(filename,  **select_kwargs(kwargs,['mass_amu']))
        else:
            self.read_ascii(filename, **select_kwargs(kwargs,['skiprows','wn_column',
                'kdata_column','data_type']))

        if mult_factor is not None: self.kdata=self.kdata*mult_factor

        if self.data_type=='xsec':
            if (Settings()._convert_to_mks) and (kdata_unit is 'unspecified'):
                    kdata_unit='m^2/molecule'
        elif self.data_type=='abs_coeff':
            if (Settings()._convert_to_mks) and (kdata_unit is 'unspecified'):
                    kdata_unit='m^-1'
        else:
            raise RuntimeError("""Data type (xsec or abs_coeff) not recognized.
                You should specify it with the data_type keyword
                (and probably the file_kdata_unit as well).""")

        self.convert_kdata_unit(kdata_unit=kdata_unit,file_kdata_unit=file_kdata_unit)
       
    def read_ascii(self, filename, data_type=None, skiprows=0, wn_column=None,
        kdata_column=None):
        """Read native kspectrum format

        Parameters
        ----------
            filename: str
                Initial hires-spectrum filename.
            data_type: 'xsec' or 'abs_coeff'
                Whether the data read are cross-sections or absorption coefficients.
            skiprows: int, optional
                Number of header lines to skip. For the latest Kspectrum format,
                the header is skipped automatically.
            wn_column/kdata_column: int, optional
                Number of column to be read for wavenumber and kdata in python convention
                (0 is first, 1 is second, etc.)
        """
        if data_type is None:
            raise RuntimeError("You did not provide a data_type ('xsec' or 'abs_coeff')")
        self.data_type=data_type
        self.filename=filename
        with open(filename, 'r') as file:
            tmp = file.readline().split()
            if tmp[0]=='Pressure':
                #File treated as a Kspectrum like format, implying P in atm, Kdata in m^-1
                for _ in range(4):
                    file.readline()
                nb_mol = int(file.readline().split()[0])
                skiprows=skiprows+9+5*nb_mol
                if kdata_column is None:
                    kdata_column=2
            else:
                if kdata_column is None: kdata_column=1

        if wn_column is None: wn_column=0
        raw=np.genfromtxt(filename, skip_header=skiprows,
            usecols=(wn_column,kdata_column), names=('wns','kdata')) 
        self.kdata=raw['kdata']
        self.wns=raw['wns']

    def write_hdf5(self, filename):
        """Writes kspectrum file to hdf5
        """
        if not filename.lower().endswith(('.hdf5', '.h5')):
            filename=filename+'.h5'
        f = h5py.File(filename, 'w')
        f.attrs["data_type"] = self.data_type
        f.create_dataset("wns", data=self.wns,compression="gzip")
        f["wns"].attrs["units"]=self.wn_unit
        f.create_dataset("kdata", data=self.kdata,compression="gzip")
        f["kdata"].attrs["units"]=self.kdata_unit
        f.close()    

    def read_hdf5(self, filename):
        """Reads kspectrum file from hdf5
        """
        self.filename=filename
        f = h5py.File(filename, 'r')
        self.data_type=f.attrs['data_type']
        self.wns=f['wns'][...]
        if 'units' in f['wns'].attrs.keys():
            self.wn_unit=f['wns'].attrs['units']
        self.kdata=f['kdata'][...]
        self.kdata_unit=f['kdata'].attrs['units']
        f.close()

    def read_binary(self, filename, mass_amu=None):
        """Reads spectra file in binary format (petitRADTRANS style)
        
        Assumed to be in cm^2/g with wavelength in cm.

        Will be automatically converted to cm^2/molecule and wns in cm^-1
        (unless conversion to mks is requested).
        """
        if mass_amu is None:
            raise RuntimeError('Need atomic mass in amu to read petitRADTRANS binary files')
        self.filename=filename
        dirname=os.path.dirname(self.filename)
        self.data_type='xsec'
        wls_cm=np.fromfile(os.path.join(dirname,'wlen.dat'))
        self.wns=1./wls_cm[::-1]
        self.kdata=np.fromfile(self.filename)[::-1]*mass_amu/N_A
        self.kdata_unit='cm^2/molecule'


    def convert_kdata_unit(self, kdata_unit='unspecified', file_kdata_unit='unspecified'):
        """Converts kdata to a new unit (inplace)

        Parameters
        ----------
            kdata_unit: str
                String to identify the units to convert to. Accepts 'cm^2', 'm^2'
                or any surface unit recognized by the astropy.units library.
                If ='unspecified', no conversion is done.
                In general, kdata should be kept in 'per number' or 'per volume'
                units (as opposed to 'per mass' units) as composition will
                always be assumed to be a number or volume mixing ratio.
                Opacities per unit mass are not supported yet.
                Note that you do not need to specify the '/molec' or
                '/molecule' in the unit.
            file_kdata_unit : str
                String to specify the current kdata unit if it is unspecified or if 
                you have reasons to believe it is wrong (e.g. you just read a file where
                you know that the kdata grid and the kdata unit do not correspond)
        """
        #if kdata_unit==file_kdata_unit and self.kdata_unit != 'unspecified': return
        tmp_k_u_in=rm_molec(file_kdata_unit)
        tmp_k_u_out=rm_molec(kdata_unit)
        tmp_k_u_file=rm_molec(self.kdata_unit)
        self.kdata_unit, conversion_factor=unit_convert(  \
            'kdata_unit',unit_file=tmp_k_u_file,unit_in=tmp_k_u_in,unit_out=tmp_k_u_out)
        if self.data_type=='xsec':
            self.kdata_unit=self.kdata_unit+'/molecule'
        else:
            self.kdata_unit=self.kdata_unit
        self.kdata=self.kdata*conversion_factor

    def __repr__(self):
        """Method to output header
        """
        output="""
        file         : {file}
        data type    : {dtype}
        data unit    : {ku}
        size         : {size}
        wns          : {wns}
        wn units     : {wnu}
        """.format(file=self.filename, ku=self.kdata_unit,
        wns=self.wns, wnu=self.wn_unit, dtype=self.data_type, size= self.wns.size)
        return output

    def plot_spectrum(self, ax, x_axis='wls',
            xscale=None, yscale=None, x=1., **kwarg):
        """Plot the spectrum
        
        Parameters
        ----------
            ax : :class:`pyplot.Axes`
                A pyplot axes instance where to put the plot.
            x_axis: str, optional
                If 'wls', x axis is wavelength. Wavenumber otherwise.
            x/yscale: str, optional
                If 'log' log axes are used.
        """
        toplot=self.kdata*x
        if x_axis == 'wls':
            ax.plot(self.wls,toplot,**kwarg)
            ax.set_xlabel('Wavelength (micron)')
        else:
            ax.plot(self.wns,toplot,**kwarg)
            ax.set_xlabel('Wavenumber (cm$^{-1}$)')
        if self.data_type=='xsec':
            ax.set_ylabel('Cross section ('+self.kdata_unit+')')
        else:
            ax.set_ylabel('Abs. Coefficient ('+self.kdata_unit+')')
        if xscale is not None: ax.set_xscale(xscale)
        if yscale is not None: ax.set_yscale(yscale)

    def convert_data_type(self, pressure, temperature, kdata_unit=None,
            convert_to=None):
        """Converts from one data_type (cross sections or absorption coefficents)
        to the other (inplace).

        Conversion to mks is done by default if a conversion takes place
        and no kdata_unit is specified. 

        Parameters
        ----------
            pressure: float
                Pressure used for the conversion (in Pa)
            temperature: float
                Temperature used for the conversion (in K)
            kdata_unit: str (optional)
                Unit to use for the output
            convert_to: str ('xsec' or 'abs_coeff', optional)
                Data type to convert to. Nothing is done if
                convert_to is equal to self.data_type.
                If None, converts to the other type.
        """
        if convert_to==self.data_type:
            return
        if self.data_type=='xsec':
            self.convert_kdata_unit(kdata_unit='m^2') #back to mks
            self.kdata=self.kdata*pressure/(KBOLTZ*temperature)
            self.data_type='abs_coeff'
            self.kdata_unit='m^-1'
        else:
            self.convert_kdata_unit(kdata_unit='m^-1') #back to mks
            self.kdata=self.kdata*KBOLTZ*temperature/pressure
            self.data_type='xsec'
            self.kdata_unit='m^2/molecule'
        if kdata_unit is not None:
            try:
                self.convert_kdata_unit(kdata_unit=kdata_unit)
            except:
                print("""If you have an error here,
                it's probably because the units specified are
                inconsistent with the final data_type.""")
                raise RuntimeError()

    def clip_spectral_range(self, wn_range=None, wl_range=None):
        """Limits the data to the provided spectral range (inplace):

           * Wavenumber in cm^-1 if using wn_range argument
           * Wavelength in micron if using wl_range
        """
        if (wn_range is None) and (wl_range is None): return
        if wl_range is not None:
            if wn_range is not None:
                raise RuntimeError('Should provide either wn_range or wl_range, not both!')
            _wn_range=np.sort(10000./np.array(wl_range))
        else:
            _wn_range=np.sort(np.array(wn_range))
        iw_min, iw_max=np.searchsorted(self.wns, _wn_range, side='left')
        self.wns=self.wns[iw_min:iw_max]
        self.Nw=self.wns.size
        self.kdata=self.kdata[iw_min:iw_max]

