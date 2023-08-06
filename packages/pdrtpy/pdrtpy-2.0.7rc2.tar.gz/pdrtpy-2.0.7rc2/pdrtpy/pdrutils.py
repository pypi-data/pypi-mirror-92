### Utility code for PDR Toolbox.

import datetime
import os.path
import sys
import numpy as np
from pathlib import Path
import warnings
from copy import deepcopy

import astropy.units as u
from astropy.constants import k_B
from astropy.table import Table

from pdrtpy import version

# Radiation Field Strength units in cgs
_RFS_UNIT_ = u.erg/(u.second*u.cm*u.cm)
_OBS_UNIT_ = u.erg/(u.second*u.cm*u.cm*u.sr)
_CM = u.Unit("cm")
_KKMS = u.Unit("K km s-1")

# ISRF in other units
#The wavelength of 1110 Ang is the longest wavelength for H2 excitation,
#but photoelectric heating can occur at longer wavelengths. 
#We use  6eV to 13.6 eV, or 912 - 2066 Ang. For this range
#Draine is 1.7G_0, and Mathis is 1.13 G_0.   
# See Weingartner and Draine 2001, ApJS, 134, 263, section 4.1

habing_unit = u.def_unit('Habing',1.60E-3*_RFS_UNIT_)
r"""The Habing radiation field unit 

   :math:`{\rm 1~Habing = 1.6\times 10^{-3}~erg~s^{-1}~cm^{-2}}`
"""
u.add_enabled_units(habing_unit)
draine_unit = u.def_unit('Draine',2.72E-3*_RFS_UNIT_)
r"""The Draine radiation field unit

    :math:`{\rm 1~Draine = 2.72\times10^{-3}~erg~s^{-1}~cm^{-2}}`
"""
u.add_enabled_units(draine_unit)
mathis_unit = u.def_unit('Mathis',1.81E-3*_RFS_UNIT_)
r"""The Mathis radiation field unit

    :math:`{\rm 1~Mathis = 1.81\times10^{-3}~erg~s^{-1}~cm^{-2}}`
"""
u.add_enabled_units(mathis_unit)

_rad_title = dict()
_rad_title['Habing'] = '$G_0$'
_rad_title['Draine'] = '$\chi$'
_rad_title['Mathis'] = 'FUV'

def get_rad(key):
    """Get radiation field symbol (LaTeX) given radiation field unit.
    If key is unrecognized, 'FUV Radiation Field' is returned.

    :param key: input field unit name, e.g. 'Habing', 'Draine' or an :class:`astropy.units.Unit`
    :returns: LaTeX string for the radiation field symbol e.g., :math:`G_0`, :math:`\chi`
    :type key: str or :class:`astropy.units.Unit`
    :rtype: str
    """
    skey = str(key) # in case the passed key was a Unit
    if skey in _rad_title:
        return _rad_title[skey]
    else:
        return "FUV"

# this didn't work
#density_unit = u.def_unit("1/cm3",1/(u.cm*u.cm*u.cm))
#u.add_enabled_units(density_unit)
    
#See https://stackoverflow.com/questions/880530/can-modules-have-properties-the-same-way-that-objects-can
# only works python 3.8+??
#def module_property(func):
#    """Decorator to turn module functions into properties.
#    Function names must be prefixed with an underscore."""
#    module = sys.modules[func.__module__]
#
#    def base_getattr(name):
#        raise AttributeError(
#            f"module '{module.__name__}' has no fucking attribute '{name}'")
#
#    old_getattr = getattr(module, '__getattr__', base_getattr)
#
#    def new_getattr(name):
#        if f'_{name}' == func.__name__:
#            return func()
#        else:
#            return old_getattr(name)
#

#    module.__getattr__ = new_getattr
#    return func

#@module_property
#def _version():

#@todo check_header_present(list) to return boolean array of keywwords
# present or not in a FITS header

#@module_property
#def _now():
def now():
    """
    :returns: a string representing the current date and time in ISO format
    """
    return datetime.datetime.now().isoformat()

#@module_property
#def _root_dir():

#@TODO  use setup.py and pkg_resources to do this properly
def root_dir():
    """Project root directory, including trailing slash

    :rtype: str
    """
    #return os.path.dirname(os.path.abspath(__file__)) + '/'
    return str(root_path())+'/'

def root_path():
    """Project root directory as path

    :rtype: :py:mod:`Path`
    """
    return Path(__file__).parent

def testdata_dir():
    """Project test data directory, including trailing slash

    :rtype: str
    """
    return os.path.join(root_dir(),'testdata/')

def get_testdata(filename):
    """Get fully qualified pathname to FITS test data file.

    :param filename: input filename, no path
    :type filename: str
    """
    return testdata_dir()+filename

def model_dir():
    """Project model directory, including trailing slash

    :rtype: str
    """
    return os.path.join(root_dir(),'models/')

def table_dir():
    """Project ancillary tables directory, including trailing slash

    :rtype: str
    """
    return os.path.join(root_dir(),'tables/')

def _tablename(filename):
    """Return fully qualified path of the input table.

    :param filename: input table file name
    :type filename: str
    :rtype: str
    """
    return table_dir()+filename


def get_table(filename,format='ipac',path=None):
    """Return an astropy Table read from the input filename.  

    :param filename: input filename, no path
    :type filename: str
    :param format:  file format, Default: "ipac"
    :type format: str
    :param  path: path to filename relative to models directory.  Default of None means look in "tables" directory 
    :type path: str
    :rtype: :class:`astropy.table.Table`
    """
    if path is None:
        return Table.read(_tablename(filename),format=format)
    else:
        return Table.read(model_dir()+path+filename,format=format)
    
#########################
# FITS KEYWORD utilities
#########################
def addkey(key,value,image):
    """Add a (FITS) keyword,value pair to the image header

       :param key:   The keyword to add to the header
       :type key:    str
       :param value: the value for the keyword
       :type value:  any native type
       :param image: The image which to add the key,val to.
       :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
    """
    if key in image.header and type(value) == str:    
        s =  str(image.header[key])
        # avoid concatenating duplicates
        if s != value:
            image.header[key] = str(image.header[key])+" "+value
    else:
        image.header[key]=value

def comment(value,image):
    """Add a comment to an image header

       :param value: the value for the comment
       :type value:  str
       :param image: The image which to add the comment to
       :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
    """
    # direct assignment will always make a new card for COMMENT
    # See https://docs.astropy.org/en/stable/io/fits/
    image.header["COMMENT"]=value
    
def history(value,image):
    """Add a history record to an image header

       :param value: the value for the history record
       :type value:  str
       :param image: The image which to add the HISTORY to
       :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
    """
    # direct assignment will always make a new card for HISTORY
    image.header["HISTORY"]=value

def setkey(key,value,image):
    """Set the value of an existing keyword in the image header

       :param key:   The keyword to set in the header
       :type key:    str
       :param value: the value for the keyword
       :type value:  any native type
       :param image: The image which to add the key,val to.
       :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
    """
    image.header[key]=value
    
def dataminmax(image):
    """Set the data maximum and minimum in image header

       :param image: The image which to add the key,val to.
       :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
    """
    setkey("DATAMIN",np.nanmin(image.data),image)
    setkey("DATAMAX",np.nanmax(image.data),image)
        
def signature(image):
    """Add AUTHOR and DATE keywords to the image header
       Author is 'PDR Toolbox', date as returned by now()

       :param image: The image which to add the key,val to.
       :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
    """
    setkey("AUTHOR","PDR Toolbox "+version(),image)
    setkey("DATE",now(),image)

def firstkey(d):
    """Return the "first" key in a dictionary

       :param d: the dictionary
       :type d: dict
    """
    return list(d)[0]

def warn(cls,msg):
    """Issue a warning

       :param cls:  The calling Class
       :type cls: Class
       :param msg:  The warning message
       :type msg: str
    """
    # use stacklevel=3 so we get a reference to the caller of
    # pdrutils.warn().
    warnings.warn(cls.__class__.__name__+": "+msg,stacklevel=3)

#@module_property
################################################################
# Conversions between various units of Radiation Field Strength
# See table on page 18 of 
# https://ism.obspm.fr/files/PDRDocumentation/PDRDoc.pdf
################################################################

def check_units(input_unit,compare_to):
    """Check if the input unit is equivalent to another.
       
       :param input_unit:  the unit to check.
       :type input_unit:  :class:`astropy.units.Unit`, :class:`astropy.units.Quantity` or str
       :param compare_unit:  the unit to check against
       :type compare_unit:  :class:`astropy.units.Unit`, :class:`astropy.units.Quantity` or str
       :return: `True` if the input unit is equivalent to compare unit, `False` otherwise 
    """
    if isinstance(input_unit,u.Unit):
        test_unit = input_unit
    if isinstance(input_unit,u.Quantity):
        test_unit = input_unit.unit
    else: # assume it is a string
        test_unit = u.Unit(input_unit)

    if isinstance(compare_to,u.Unit):
        compare_unit = compare_to
    if isinstance(compare_to,u.Quantity):
        compare_unit = compare_to.unit
    else: # assume it is a string
        compare_unit = u.Unit(compare_to)

    return test_unit.is_equivalent(compare_unit)


def to(unit,image):
  r"""Convert the image values to another unit.
     While generally this is intended for converting radiation field
     strength maps between Habing, Draine, cgs, etc, it will work for
     any image that has a unit member variable. So, e.g., it would work
     to convert density from :math:`{\rm cm ^{-3}}` to :math:`{\rm m^{-3}}`.
     If the input image is a :class:`~pdrtpy.measurement.Measurement`, its
     uncertainty will also be converted.

     :param unit: identifying the unit to convert to 
     :type unit: string or `astropy.units.Unit` 
     :param image: the image to convert. It must have a :class:`numpy.ndarray`
        data member and :class:`astropy.units.Unit` unit member.
     :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
     :return: an image with converted values and units
  """
  #print("converting [%s] in %s to [%s]"%(image.unit,image.header["TITLE"],unit))
  value = image.unit.to(unit)
  newmap = deepcopy(image)
  newmap.data = newmap.data * value
  newmap.unit = u.Unit(unit)
  # deal with uncertainty in Measurements.
  if getattr(newmap,"_uncertainty") is not None:
     newmap._uncertainty.array = newmap.uncertainty.array * value
     newmap._uncertainty.unit = u.Unit(unit)
  return newmap

def toHabing(image):
  r"""Convert a radiation field strength image to Habing units :math:`(G_0)`.

     :math:`{\rm G_0 \equiv 1~Habing = 1.6\times10^{-3}~erg~s^{-1}~cm^{-2}}`

     between 6eV and 13.6eV (912-2066 :math:`\unicode{xC5}`).  See `Weingartner and Draine 2001, ApJS, 134, 263 <https://ui.adsabs.harvard.edu/abs/2001ApJS..134..263W/abstract>`_, section 4.1 

     :param image: the image to convert. It must have a :class:`numpy.ndarray`
        data member and :class:`astropy.units.Unit` unit member.
     :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
     :return: an image with converted values and units
  """
  return to('Habing',image)
   
def toDraine(image):
  r"""Convert a radiation field strength image to Draine units (\chi).

     :math:`{\rm 1~Draine = 2.72\times10^{-3}~erg~s^{-1}~cm^{-2}}`

     between 6eV and 13.6eV (912-2066 :math:`\unicode{xC5}`).  See `Weingartner and Draine 2001, ApJS, 134, 263 <https://ui.adsabs.harvard.edu/abs/2001ApJS..134..263W/abstract>`_, section 4.1 

     :param image: the image to convert. It must have a :class:`numpy.ndarray`
        data member and :class:`astropy.units.Unit` unit member.
     :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
     :return: an image with converted values and units
  """
  return to('Draine',image)

def toMathis(image):
  r"""Convert a radiation field strength image to Mathis units

     :math:`{\rm 1~Mathis = 1.81\times10^{-3}~erg~s^{-1}~cm^{-2}}`

     between 6eV and 13.6eV (912-2066 :math:`\unicode{xC5}`).  See `Weingartner and Draine 2001, ApJS, 134, 263 <https://ui.adsabs.harvard.edu/abs/2001ApJS..134..263W/abstract>`_, section 4.1 

     :param image: the image to convert. It must have a :class:`numpy.ndarray`
        data member and :class:`astropy.units.Unit` unit member.
     :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
     :return: an image with converted values and units
  """
  return to('Mathis',image)

def tocgs(image):
  r"""Convert a radiation field strength image to :math:`{\rm erg~s^{-1}~cm^{-2}}`.

     :param image: the image to convert. It must have a :class:`numpy.ndarray` data member and :class:`astropy.units.Unit` unit member.
     :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
     :return: an image with converted values and units
  """
  return to(_RFS_UNIT_,image)

def convert_integrated_intensity(image,wavelength=None):
  # cute. Put r in front of docstring to prevent python interpreter from 
  # processing \.  Otherwise \times gets interpreted as tab imes
  #https://stackoverflow.com/questions/8385538/how-to-enable-math-in-sphinx
  r"""Convert integrated intensity from :math:`{\rm K~km~s}^{-1}` to 
  :math:`{\rm erg~s^{-1}~cm^{-2}~sr^{-1}}`, assuming
  :math:`B_\lambda d\lambda = 2kT/\lambda^3 dV` where :math:`T dV` is the integrated intensity in K km/s and :math:`\lambda` is the wavelength.  The derivation:

  .. math::

     B_\lambda = 2 h c^2/\lambda^5  {1\over{exp[hc/\lambda k T] - 1}} 

  The integrated line is :math:`B_\lambda d\lambda` and for :math:`hc/\lambda k T << 1`:

  .. math::

     B_\lambda d\lambda = 2c^2/\lambda^5  \times (\lambda kT/hc)~d\lambda 

  The relationship between velocity and wavelength, :math:`dV = \lambda/c~d\lambda`, giving 

  .. math::

     B_\lambda d\lambda = 2\times10^5~kT/\lambda^3~dV,  

  with :math:`\lambda`  in cm, the factor :math:`10^5` is to convert :math:`dV` in :math:`{\rm km~s}^{-1}` to :math:`{\rm cm~s}^{-1}`.

  :param image: the image to convert. It must have a :class:`numpy.ndarray` data member and :class:`astropy.units.Unit` unit member or header BUNIT keyword. It's units must be K km/s
  :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
  :param wavelength: the wavelength of the observation. The default is to determine wavelength from the image header RESTFREQ keyword
  :type wavelength: :class:`astropy.units.Quantity`
  :return: an image with converted values and units
  """
  f = image.header.get("RESTFREQ",None)
  if f is None and wavelength is None:
     raise Exception("Image header has no RESTFREQ. You must supply wavelength")
  if f is not None and wavelength is None:
     # FITS restfreq's are in Hz
     wavelength = u.Quantity(f,"Hz").to(_CM,equivalencies=u.spectral())
  if image.header.get("BUNIT",None) is None:
     raise Exception("Image BUNIT must be present and equal to 'K km/s'")
  if u.Unit(image.header.get("BUNIT")) != _KKMS:
     raise Exception("Image BUNIT must be 'K km/s'")
  factor = 2E5*k_B/wavelength**3
  print("Converting K km/s to %s using Factor = %s"%(_OBS_UNIT_, "{0:+0.3E}".format(factor.decompose(u.cgs.bases))))
  newmap = deepcopy(image)
  value = factor.decompose(u.cgs.bases).value
  newmap.data = newmap.data * value
  newmap.unit = _OBS_UNIT_
  # deal with uncertainty in Measurements.
  if getattr(newmap,"_uncertainty") is not None:
     newmap._uncertainty.array = newmap.uncertainty.array * value
     newmap._uncertainty.unit = _OBS_UNIT_
  return newmap

def convert_if_necessary(image):
    r"""Helper method to convert integrated intensity units in an
    image or Measurement from :math:`{\rm K~km~s}^{-1}` to :math:`{\rm
    erg~s^{-1}~cm^{-2}~sr^{-1}}`. If a conversion is necessary, the
    :meth:`convert_integrated_intensity` is called.  If not, the image
    is returned unchanged.

    :param image: the image to convert. It must have a :class:`numpy.ndarray` data member and :class:`astropy.units.Unit` unit member or a header BUNIT keyword. It's units must be :math:`{\rm K~km~s}^{-1}`. It must also have a header RESTFREQ keyword.
    :type image: :class:`astropy.io.fits.ImageHDU`, :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.

    :return: an image with converted values and units
    """
    _u1 = u.Unit(image.header["BUNIT"])
    _u2 = u.Unit("K km s-1")
    if _u1 == _u2:
        return convert_integrated_intensity(image)
    else:
        return image

def mask_union(arrays):
    """Return the union mask (logical OR) of the input masked arrays.
    This is useful when doing arithmetic on images that don't have identical masks
    and you want the most restrictive mask.

    :param arrays: masked arrays to unionize
    :type arrays: :class:`numpy.ma.masked_array`
    :rtype: mask
    """
    z = list()
    for m in arrays:
       z.append(m.mask)
    return np.any(z,axis=0)
   
def dropaxis(w):
    """ Drop the first single dimension axis from a World Coordiante System.  Returns the modified WCS if it had a single dimension axis or the original WCS if not.
 
    :param w: a WCS
    :type w: :class:`astropy.wcs.WCS`
    :rtype: :class:`astropy.wcs.WCS`
    """
    for i in range(len(w._naxis)):
        if w._naxis[i] == 1:
            return w.dropaxis(i)
    return w

def has_single_axis(w):
    """Check if the input WCS has any single dimension axes

    :param w: a WCS
    :type w: :class:`astropy.wcs.WCS`
    :return: True if the input WCS has any single dimension axes, False otherwise
    :rtype: bool
    """
    for i in range(len(w._naxis)):
        if w._naxis[i] == 1: return True
    return False

def squeeze(image):
  """Remove single-dimensional entries from image data and WCS.

  :param image: the image to convert. It must have a :class:`numpy.ndarray` data member and :class:`astropy.units.Unit` unit member. 
  :type image: :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement`.
 
  :return: an image with single axes removed
  :rtype: :class:`astropy.nddata.CCDData`, or :class:`~pdrtpy.measurement.Measurement` as input
  """
  while has_single_axis(image.wcs):
    image.wcs = dropaxis(image.wcs)

  # np.squeeze is a no-op if there are no dimensions to squeeze
  if image.data is not None:
      image.data = np.squeeze(image.data)
  if image.uncertainty is not None:
      image.uncertainty._array = np.squeeze(image.uncertainty._array)
  if image.mask is not None:
      image.mask = np.squeeze(image.mask)

  # update the header which can be independent of WCS
  image.header["NAXIS"] = image.wcs.wcs.naxis
  i =  image.wcs.wcs.naxis+1
  nax = "NAXIS"+str(i)
  while image.header.pop(nax,None) is not None:
    i=i+1
    nax = "NAXIS"+str(i)
  
  return image

def fliplabel(label):
    """Given a label that has a numerator and a denominator separated by a '/', return the 
    reciprocal label.  For example, if the input label is '(x+y)/z' return 'z/(x+y)'.  This 
    method simply looks for the '/' and swaps the substrings before and after it.
    
    :param label: the label to flip
    :type label: str
    :return: the reciprocal label
    :rtype: str
    :raises ValueError: if the input label has no '/'
    """
    ii = label.index('/')
    return label[ii+1:]+'/'+label[0:ii]
