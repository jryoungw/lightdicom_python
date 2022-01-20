from LightTag import Tag

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
    # if isLittle:
    #     for idx in range(len(toInt)):
    #         retInt += (16**idx) * toInt[2*((idx)//2) + ((idx+1)%2)]
    # else:
    #     for idx in range(len(toInt)):
    #         retInt += (16**idx) * toInt[idx]

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
        for l in li:
            s = s + l
    else:
        for ldx in range(len(li)):
            s = s + li[2*((ldx)//2) + ((ldx+1)%2)]
    return s

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

        if isGroupLengthTag:
            value = file[idx:idx+vl]
            assert vr == b'UL', "Value Representation (VR) should be type of UL (Unsigned Long). " + \
                                f"Current VR : {vr}. Check your DICOM sanity."
            value = parseUL(value, isLittle=isLittle)
            idx = idx + vl
        else:
            value = file[idx:idx+vl]
            idx = idx + vl
        print("Tag :", _tag)
        tagClass[_tag] = [vr, vl, value]

        return tagClass
