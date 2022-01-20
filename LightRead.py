from LightTag import Tag

class LightRead(Tag):
    def __init__(self, path, print_warning=True):
        super().__init__()
        self.path = path
        self.print_warning = print_warning
        self.dtype = [b'CS', b'SH', b'LO', b'ST', b'LT', b'UT', b'AE', \
                      b'PN', b'UI', b'UID', b'DA', b'TM', b'DT', b'AS', \
                      b'IS', b'DS', b'SS', b'US', b'SL', b'UL', b'AT', \
                      b'FL', b'FD', b'OB', b'OW', b'OF', b'SQ', b'UN']
        self.isLittle = True
        self.isExplicit = True

    def __len__(self):
        return len(self.file)


    def lightRead(self, path:str = None) -> None:
        assert self.path is not None or path is not None, \
                "Input path argument should exist in either "+\
        "'LightDCMClass.path' or 'LightDCMClass.lightRead(path)'"
        if self.path is not None:
            if path is not None and self.print_warning is True:
                print("'LightDCMClass.path' precedes "+\
                      "'LightDCMClass.lightRead(path)'. Using "\
                      "LightDCMClass.path")
            file = open(self.path, 'rb').read()
            self._exam_file(file[:132], self.force)
        else:
            self.path = path
            file = open(self.path, 'rb').read()
            self._exam_file(file[:132], self.force)

        self.file = file

    def _exam_file(self, file, force):
        preamble = bytes([0])*128
        if file[:128] != preamble:
            if self.print_warning == True:
                print(f"For {self.path}, first 128 bytes are not zeros. "\
                      "This is not usual DICOM type. Handle this file "\
                      "carefully.")
            else:
                pass
        if file[128:132] != b'DICM':
            if force is False:
                raise LightError(f"For {self.path}, 129-th~133-th bytes "\
                      "should be 'DICM'. This is not valid DICOM file.\n"\
                      "If you want to read this file anyway, try "\
                      "'LightDCMClass(force=True)'")
            else:
                if self.print_warning is True:
                    print(f"For {self.path}, 129-th~133-th bytes are not "\
                      "'DICM'. This is not usual DICOM type. Handle this "\
                      "file carefully.")
                else:
                    pass