# LightDICOM

## Basic Usage

```
from LightClass import LightDCMClass

lc = LightDCMClass()
lc.path = path_to_dicom
d = lc.get_data('0010,0010') # Read tag (0010, 0010)
npy = lc.read_pixel() # Read pixel values
```

## Notes

This is prototype version. Other advanced version will be released soon ... (maybe?)
