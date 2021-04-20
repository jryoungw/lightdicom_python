from Errors import LightError
from UID import UID_dictionary

class LightDCMClass():
    def __init__(self, **kwargs):
        self.path = None
        self.Little_Endian=True
        self.print_warning=True
        self.force=False
        self.endian='Little'
        self.dtype = [b'CS', b'SH', b'LO', b'ST', b'LT', b'UT', b'AE', b'PN', b'UI', b'UID', b'DA', \
                      b'TM', b'DT', b'AS', b'IS', b'DS', b'SS', b'US', b'SL', b'UL', b'AT', \
                      b'FL', b'FD', b'OB', b'OW', b'OF', b'SQ', b'UN']
        for k, v in kwargs.items():
            exec(f'self.{k}=v')

    def lightRead(self, path=None):
        assert self.path is not None or path is not None, \
                "Input path argument should exist in either 'LightDCMClass.path' or 'LightDCMClass.lightRead(path)'"
        if self.path is not None:
            if path is not None and self.print_warning is True:
                print("'LightDCMClass.path' precedes 'LightDCMClass.lightRead(path)'. Using LightDCMClass.path")
            file = open(self.path, 'rb').read()
            self._exam_file(file[:132], self.force)
        else:
            self.path = path
            file = open(self.path, 'rb').read()
            self._exam_file(file[:132], self.force)

        self.file = file

    def __len__(self):
        return len(self.file)

    def _exam_file(self, file, force):
        preamble = b'\x00'*128
        if file[:128] is not preamble:
            if self.print_warning is True:
                print(f"For {self.path}, first 128 bytes are not zeros. This is not usual DICOM type. Handle this file carefully.")
            else:
                pass
        if file[128:132] != b'DICM':
            if force is False:
                raise LightError(f"For {self.path}, 129-th~133-th bytes should be 'DICM'. This is not valid DICOM file.\n"\
                                +"If you want to read this file anyway, try 'LightDCMClass(force=True)'")
            else:
                if self.print_warning is True:
                    print(f"For {self.path}, 129-th~133-th bytes are not 'DICM'. This is not usual DICOM type. Handle this file carefully.")
                else:
                    pass
    def _maketag(self, binary, idx):
        ret = []
        converted = list(binary)
        for l in converted:
            l = str(hex(l))[2:]
            if len(str(l))==1:
                ret.append('0'+str(l))
            elif len(str(l))==2:
                ret.append(str(l))
            else:
                ret.append()
        if self.endian=='Little':
            return f'{ret[1]}{ret[0]},{ret[3]}{ret[2]}'
        if self.endian=='Big':
            return f'{ret[0]}{ret[1]},{ret[2]}{ret[3]}'

    def _check_endian(self, file):
        if b'1.2.840.10008.1.2.1' in string:
            self.endian = 'Explicit VR Little Endian'
        elif b'1.2.840.10008.1.2.2' in string:
            self.endian = 'Explicit VR Big Endian'
        elif b'1.2.840.10008.1.2' in string:
            self.endian = 'Implicit VR Endian'
        elif b'1.2.840.10008.1.2.1.99' in string:
            self.endian = 'Deflated Explicit VR Little Endian'

    def _get_vr_length(self, binary):
        li = list(binary)
        s = 0
        for l in li:
            s = s + l
        return s
    
    def _integer(self, string):
        try:
            return int(string)
        except:
            alphabet = {'a':10, 'b':11, 'c':12, 'd':13, 'e':14, 'f':15}
            return alphabet[string]

    def _OBOW_vr(self, bytestring):
        a, b = str(bytestring[0:2]), str(bytestring[2:4])
        backslash = a[2]
        a = a[2:-1].split('\\x')
        b = b[2:-1].split('\\x')
        if a[0] == '' and len(a) == 2:
            x, y = a[1][-1], a[1][:2]
        elif a[0] == '' and len(a) == 3:
            _, y, x = a
        else:
            assert len(a) == 2
            y, x = a

        if b[0] == '' and len(b) == 2:
            z, w = b[1][-1], b[1][:2]
        elif b[0] == '' and len(b) == 3:
            _, w, z = b
        else:
            assert len(b) == 2
            w, z = a
        if x == '00':
            x = ''
        elif x[0] == '0':
            x = x[1]
        if y == '00':
            y = ''
        elif y[0] == '0':
            y = y[1]
        if z == '00':
            z = ''
        elif z[0] == '0':
            z = z[1]
        if w == '00':
            w = ''
        elif w[0] == '0':
            w = w[1]
        xyzw = [x,y,z,w]
        for i in range(len(xyzw)):
            elem = xyzw[i]
            if len(elem)>1:
                xyzw[i] = b'\\x'+bytes(xyzw[i], 'utf-8')
            else:
                xyzw[i] = bytes(xyzw[i], 'utf-8')
        print(xyzw)
        merged = xyzw[0] + xyzw[1] + xyzw[2] + xyzw[3]
        merged = merged.decode('unicode-escape').encode('ISO-8859-1')
        print(merged)
        if len(merged)==1:
            merged = str(int(merged))
        else:
            merged = merged.hex()
        print(merged)
        sum = 0
        for i in (range(len(merged))):
            sum += (16**(len(merged)-i-1)) * self._integer(merged[i])
        return sum

    def get_data(self, tag):
        idx = 132
        while True:
            find_tag = self._maketag(self.file[idx:idx+4], idx)
            dtype = self.file[idx+4:idx+6]
            if find_tag == '0008,1140':
                if tag == '0008,1140':
                    vl = self.file[idx+8:idx+12]
                    return {'tag': tag, 'dtype': dtype, 'length': vl, 'value': self.file[idx+12:idx+12+8]}
                else:
                    idx = idx+20
            else:
                if dtype in [b'OB', b'OW', b'SQ', b'UN']:
                    reserved = self.file[idx+6:idx+8]
                    vl = self.file[idx+8:idx+12]
                    
                    if dtype in [b'OB', b'OW']:
                        vl = self._OBOW_vr(vl)
                    else:
                        vl = self._get_vr_length(vl)
                    if find_tag==tag:
                        return {'tag': tag, 'dtype': dtype, 'reserved': reserved, 'length': vl, 'value': self.file[idx+12:idx+12+vl]}
                    else:
                        idx = idx+12+vl
                else:
                    vl = self.file[idx+6:idx+8]
                    vl = self._get_vr_length(vl)
                    if find_tag==tag:
                        return {'tag': tag, 'dtype': dtype, 'length': vl, 'value': self.file[idx+8 :idx+8+vl]}
                    else:
                        idx = idx+8+vl

            if idx>=len(self.file)-4:
                raise LightError(f"No matching tag was founded for tag ({tag}) in file {self.path}.")