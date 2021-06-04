# LightDICOM

_**LightDICOM**_ is a _**fast as light, light as feather**_ Python3 package for managing [DICOM](https://www.dicomstandard.org/) files.  
The only 3rd party dependency is `numpy`, thus **fast** and **light**.

- **Source Code**: [Github](https://github.com/jryoungw/lightdicom)
- **Korean version**: [한국어 README](https://github.com/jryoungw/lightdicom/blob/main/README_KOR.md)
- **Bug report/Feature request**: Open a Github [Issue](https://github.com/jryoungw/lightdicom/issues/new/choose) or contact me at `ryoungwoo.jang@vuno.co`
- Benchmarks: WIP
- DEMO: WIP
- Documentation: WIP

## Basic Usage

```
from LightClass import LightDCMClass

lc = LightDCMClass()
lc.path = path_to_dicom
d = lc.get_data('0010,0010') # Read tag (0010, 0010), which is "Patient's Name"
npy = lc.read_pixel() # Read pixel values
```

Or

```
from LightClass import LightDCMClass

lc = LightDCMClass(path=path_to_dicom)
d = lc.get_data('0010,0010') # Read tag (0010, 0010), which is "Patient's Name"
npy = lc.read_pixel() # Read pixel values
```

## How to read all headers and their values?

```
lc = LightDCMClass()
lc.path = path_to_dicom 
# Equivalent code : lc = LightDCMClass(path=path_to_dicom)
all_headers = lc.read_all(with_pixel=True)
```

In **.read_all** method, there are two arguments:
- with_pixel : If **True**, read header information with pixel values. Else, **.read_all** will not read pixel values. There will be no significant time difference, yet memory efficiency will be different. **False** uses less memory. That's the difference.
- resize_pixel : If **True**, pixel value will be reshaped according to width (0028,0010) and height (0028,0011) information. I guess that in most situations, setting **.resize_pixel** to **False** will not be required.

## Dependencies
```
- Python 3.x
- Numpy
```
## Installation

If `numpy` is not installed, first install it by `pip`, `conda` or other method of your choice.
- install from source
`git clone https://github.com/jryoungw/lightdicom`
- pypi, conda, etc. are not yet supported. (WIP)
## Notes

This is a prototype version, so do remember that bugs or unexpected behaviors may exist.  
Whenever bugs are found, please contact via the aforementioned methods. PRs are welcome!
