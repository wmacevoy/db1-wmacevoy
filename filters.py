def dbInteger(value, nullable = False):
    return int(value) if not nullable or value != None else None

def dbReal(value, nullable = False):
    return float(value) if not nullable or value != None else None

def dbString(value, nullable = False):
    return str(value) if not nullable or value != None else None

def dbShift(value, nullable = False):
    strValue=dbString(value,nullable)
    if strValue in ['day','evening','night']:
        return strValue
    else:
        raise ValueError('value ' + strValue + ' is not day eveninig or night.')
    
def integerOrNull(value):
    return int(value) if value != None else None

def realOrNull(value):
    return float(value) if value != None else None
