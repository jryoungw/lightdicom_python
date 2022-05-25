# LightDICOM

_**LightDICOM**_ 은 _**빠르고(fast) 가벼운(light)**_ [DICOM](https://www.dicomstandard.org/) 처리 Python3 패키지입니다.  
기본 내장 패키지 이외에는 `numpy`만 사용하는 덕분에 **빠르고** and **가벼운** 독립성 높은 DICOM 패키지입니다.

- **소스 코드**: [Github](https://github.com/jryoungw/lightdicom)
- **영문 버전**: [English README](https://github.com/jryoungw/lightdicom/blob/main/README.md)
- **버그 제보/기능 제안**: Github에 [이슈](https://github.com/jryoungw/lightdicom/issues/new/choose)를 열거나 `ryoungwoo.jang@vuno.co`로 문의주세요.
- 벤치마크: WIP
- 데모: WIP
- Documentation: WIP

## 기본 사용법

```python
from LightClass import LightDCMClass

lc = LightDCMClass()
lc.path = path_to_dicom
d = lc.get_data('0010,0010') # Read tag (0010, 0010), which is "Patient's Name"
npy = lc.read_pixel() # Read pixel values
```

혹은

```python
from LightClass import LightDCMClass

lc = LightDCMClass(path=path_to_dicom)
d = lc.get_data('0010,0010') # Read tag (0010, 0010), which is "Patient's Name"
npy = lc.read_pixel() # Read pixel values
```

## 한 번에 모든 DICOM header를 읽는 방법은?

```python
lc = LightDCMClass()
lc.path = path_to_dicom 
# Equivalent code : lc = LightDCMClass(path=path_to_dicom)
all_headers = lc.read_all(with_pixel=True)
```

**.read_all** 메서드에는 두 가지 인자가 있습니다:
- with_pixel : **True**로 두면, 픽셀 정보도 함께 읽어 리턴합니다(7fe0,0010). 그렇지 않다면, **.read_all** 는 픽셀 정보를 읽어들이지 않을 것입니다. 두 가지 경우는 속도 면에선 큰 차이가 없으며, True일때 메모리 사용량이 더 크다는 차이가 있습니다.
- resize_pixel : **True**로 두면, 픽셀 값은 width(폭; 0028,0010)와 height(높이;0028,0011) 정보에 맞게 크기가 재조정됩니다. 대부분의 상황에서 이 값을 True로 놓으면 마음이 편안해질 것입니다.

## 의존성
```
- Python 3.x
- Numpy
```
## 설치 가이드

아직 `numpy`를 설치하지 않았다면, `pip`, `conda` 또는 기타 선호하는 방법으로 설치하십시오.
- source로부터 설치하기
`git clone https://github.com/jryoungw/lightdicom`
- 추후 pypi, conda 등의 지원이 추가될 계획입니다. (WIP)
## Notes

이 패키지는 아직 프로토타입 버전이기에, 버그나 의도하지 않은 결과를 보여줄 가능성이 분명히 존재함을 알려드립니다.  
버그를 찾으신다면, 언제든지 위에 적혀 있는 연락처로 문의주시기 바랍니다. PR으로 해결책을 보내주시는 것도 환영합니다
