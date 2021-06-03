# LightDICOM

## 기본 사용법

```
from LightClass import LightDCMClass

lc = LightDCMClass()
lc.path = path_to_dicom
d = lc.get_data('0010,0010') # Read tag (0010, 0010), which is "Patient's Name"
npy = lc.read_pixel() # Read pixel values
```

혹은

```
from LightClass import LightDCMClass

lc = LightDCMClass(path=path_to_dicom)
d = lc.get_data('0010,0010') # Read tag (0010, 0010), which is "Patient's Name"
npy = lc.read_pixel() # Read pixel values
```

## 한 번에 모든 DICOM header를 읽는 방법은?

```
lc = LightDCMClass()
lc.path = path_to_dicom 
# Equivalent code : lc = LightDCMClass(path=path_to_dicom)
all_headers = lc.read_all(with_pixel=True)
```

**.read_all** 메서드에는 두 가지 인자가 있습니다.
- with_pixel : **True**로 설정하면, 픽셀 정보를 함께 리턴합니다(0fe0,0010). **False**로 설정하는 것과 속도면에서는 큰 차이가 없습니다. **True**로 두냐 **False**로 두냐의 차이는 메모리를 더 사용하냐 덜 사용하냐입니다.
- resize_pixel : **True**로 두면, width (0028,0010)와 height (0028,0011) 정보에 따라 이미지를 resize해줍니다. 대부분의 상황에서 이 값을 **True**로 놓으면 마음이 편안해질 것입니다.


## Notes

이 repository는 프로토타입 버전입니다. 더 발전된 버전은 향후 릴리즈 예정입니다 ... (아마도?)
