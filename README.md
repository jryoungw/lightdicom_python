# LightDICOM

If you are native Korean, read ![한국어 README.md](https://github.com/jryoungw/lightdicom/blob/main/README_KOR.md)

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

In **.read_all** method, there are two arguments
- with_pixel : If **True**, read header information with pixel values. Else, **.read_all** will not read pixel values. There will be no significant time difference, yet memory efficiency will be different. **False** uses less memory. That's the difference.
- resize_pixel : If **True**, pixel value will be reshaped according to width (0028,0010) and height (0028,0011) information. I guess that in almost situation, setting **.resize_pixel** to **False** will not be required.


## Notes

This is prototype version. Other advanced version will be released soon ... (maybe?)
