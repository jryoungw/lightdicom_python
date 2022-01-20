def getTag(binary:bin, isLittle=True, isExplicit=True) -> int:
    ret = []
    converted = list(binary)
    for l in converted:
        l = str(hex(l))[2:]
        if len(str(l))==1:
            ret.append('0'+str(l))
        elif len(str(l))==2:
            ret.append(str(l))
    if isLittle:
        return int(f'{ret[1]}{ret[0]}{ret[3]}{ret[2]}')
    else:
        return int(f'{ret[0]}{ret[1]},{ret[2]}{ret[3]}')




# def paseDCM(isLittle=True, isExplicit=True):
