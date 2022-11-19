from LightTag import Tag
from Errors import LightError
from Tags import DicomDictionary

import numpy as np

def getTag(binary:bin, isLittle:bool) -> int:
    ret = []
    converted = list(binary)
    for l in converted:
        l = str(hex(l))[2:]
        if len(str(l))==1:
            ret.append('0'+str(l))
        else:
            ret.append(str(l))
    if isLittle:
        return int(f'{ret[1]}{ret[0]}{ret[3]}{ret[2]}', 16)
    else:
        return int(f'{ret[0]}{ret[1]},{ret[2]}{ret[3]}', 16)


dtypeString = ["CS", "SH", "LO", "ST", "LT", "UT", "AE', 'PN", "UI", "DA", "TM", "DT", "AS", "IS", "DS"]
dtypeInt    = ["SL", "SS", "US", "UL"]
dtypeFloat  = ["AT", "FL", "FD", "OF"]
dtypeOB     = ["OB"]
dtypeOW     = ["OW"]
dtypeSQ     = ["SQ"]
dtypeUN     = ["UN"]

def ifContainsString(vr:str) -> bool:
    if vr in dtypeString:
        return True
    else:
        return False

def ifContainsInt(vr:str) -> bool:
    if vr in dtypeInt:
        return True
    else:
        return False

def ifContainsOB(vr:str) -> bool:
    if vr in dtypeOB:
        return True
    else:
        return False

def ifContainsOW(vr:str) -> bool:
    if vr in dtypeOW:
        return True
    else:
        return False

def ifContainsSQ(vr:str) -> bool:
    if vr in dtypeSQ:
        return True
    else:
        return False
def ifContainsUN(vr:str) -> bool:
    if vr in dtypeUN:
        return True
    else:
        return False

def ifGroupLengthTag(tag:str) -> bool:
    if tag % (16**4) == 0:
        return True
    else:
        return False

def parseUL(value:bin, isLittle:bool) -> int:
    toInt = list(value)
    retInt = sum(toInt)

    return retInt

def _OBOW_vr(bytestring:bytes, tag:int, isLittle) -> int:
    slices = []
    bytestring = bytes(bytestring)
    for i in range(len(bytestring)//2):
        if tag==0x7fe00010:
            if isLittle:
                converted = int.from_bytes(bytestring, byteorder='little', signed = False)
            else:
                converted = int.from_bytes(bytestring, byteorder='big', signed = False)
            return converted
        else:
            slices.append(np.frombuffer(bytes((bytestring[2*i:2*(i+1)])), np.uint16))
            return np.sum(slices)

def _get_vr_length(binary:bin, isLittle:bool) -> int:
    li = list(binary)
    s = 0
    if isLittle:
        for idx, l in enumerate(li):
            s = s + l * 16**idx
    else:
        for idx, ldx in enuerate(range(len(li))):
            s = s + li[2*((ldx)//2) + ((ldx+1)%2)] * \
                16**idx
    return s

def parseUntilUID(tagClass:Tag, \
                 file:bin,     \
                 idx=132) -> Tag:
    UID = None
    while True:
        idx = int(idx)
        _tag = getTag(file[idx:idx+4], isLittle=True)

        isGroupLengthTag = ifGroupLengthTag(_tag)
        idx = idx + 4
        vr = file[idx:idx+2]

        # Refer "https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_7.html" for more details.
        if vr in [b'OB', b'OW', b'OF', b'SQ', b'UT', b'UN']:
            idx = idx + 2 + 2 # Last 2 is for reserved 2 bytes.
            vl = file[idx:idx+4]
            idx = idx + 4
            vl = _OBOW_vr(vl, _tag, isLittle=True)
        else:
            idx = idx + 2     # There are no reseved bytes.
            vl = file[idx:idx+2]
            vl = _get_vr_length(vl, isLittle=True)
            idx = idx + 2
        value = file[idx:idx + vl]

        if isGroupLengthTag:
            assert vr == b'UL', "Value Representation (VR) should be type of UL (Unsigned Long) for Group Length Tag."+\
                                f"Current VR : {vr}. Check your DICOM sanity."
            value = parseUL(value, isLittle=True)

        idx = idx + vl
        tagClass[_tag] = [vr, vl, value]
        if _tag == 131088:
            UID = hex(_tag)

        print(hex(_tag), vr, vl, value)
        if UID is not None:
            return tagClass, idx, UID

        if idx > len(file):
            raise LightError("This file does not follow DICOM standard protocol. Check your DICOM sanity.")

def parseExplicitVRLittleEndian(tagClass:Tag, \
                                file:bin,     \
                                isLittle:bool,\
                                idx=132) -> Tag:
    while True:
        idx = int(idx)
        _tag = getTag(file[idx:idx+4], isLittle=isLittle)

        isGroupLengthTag = ifGroupLengthTag(_tag)
        idx = idx + 4
        vr = file[idx:idx+2]

        # Refer "https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_7.html" for more details.
        if vr in [b'OB', b'OW', b'OF', b'SQ', b'UT', b'UN']:
            idx = idx + 2 + 2 # Last 2 is for reserved 2 bytes.
            vl = file[idx:idx+4]
            idx = idx + 4
            vl = _OBOW_vr(vl, _tag, isLittle=isLittle)
        else:
            idx = idx + 2     # There are no reseved bytes.
            vl = file[idx:idx+2]
            vl = _get_vr_length(vl, isLittle=isLittle)
            idx = idx + 2
        value = file[idx:idx + vl]

        if isGroupLengthTag:
            assert vr == b'UL', "Value Representation (VR) should be type of UL (Unsigned Long) for Group Length Tag."+\
                                f"Current VR : {vr}. Check your DICOM sanity."
            value = parseUL(value, isLittle=isLittle)

        idx = idx + vl
        tagClass[_tag] = [vr, vl, value]

        print(hex(_tag), vr, vl, value)
        if idx == len(file):
            return tagClass
        if idx > len(file):
            raise LightError("This file does not follow DICOM standard protocol. Check your DICOM sanity.")
        # return tagClass

def parseImplicitVRLittleEndian(tagClass:Tag, \
                                file:bin,     \
                                isLittle:bool,\
                                idx=132) -> Tag:
    while True:
        idx = int(idx)
        _tag = getTag(file[idx:idx+4], isLittle=isLittle)

        isGroupLengthTag = ifGroupLengthTag(_tag)
        idx = idx + 4

        # Refer "https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_7.html" for more details.
        print(hex(_tag))
        vr = DicomDictionary[_tag][0]

        vl = file[idx:idx+4]
        idx = idx + 4
        vl = _get_vr_length(vl, isLittle=isLittle)

        value = file[idx:idx + vl]

        if isGroupLengthTag:
            assert vr == b'UL', "Value Representation (VR) should be type of UL (Unsigned Long) for Group Length Tag."+\
                                f"Current VR : {vr}. Check your DICOM sanity."
            value = parseUL(value, isLittle=isLittle)

        idx = idx + vl
        tagClass[_tag] = [vr, vl, value]

        print(hex(_tag), vr, vl, value)
        if idx == len(file):
            return tagClass
        if idx > len(file):
            raise LightError("This file does not follow DICOM standard protocol. Check your DICOM sanity.")
        # return tagClass
