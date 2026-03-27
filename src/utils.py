from enum import Enum

class ClassMask(Enum):
    CLASS_A = "255.0.0.0"
    CLASS_B = "255.255.0.0"
    CLASS_C = "255.255.255.0"
    CLASS_D = "N/A"
    CLASS_E = "N/A"
    ERROR = "error"



def isIp(ip):
    if not isinstance(ip, str):
        return False
    
    if ip.count(".") != 3:
        return False

    numbers = ip.split(".")
    for number in numbers:
        if not number.isdigit():
            return False
        
        value = int(number)
        if value < 0 or value > 255:
            return False

    return True

def isClassFull(mask):
    if (not isIp(mask)): return "error"
    maskParts = [int(x) for x in mask.split(".")]

    for part in maskParts:
        if part != 255 and part != 0:
            return False
        
    return True


def getIPClass(ip):
    if (not isIp(ip)): return ClassMask.ERROR

    firstNum = int(ip.split(".")[0])

    if firstNum >= 0 and firstNum <= 127:
        return ClassMask.CLASS_A
    elif firstNum >= 128 and firstNum <= 191:
        return ClassMask.CLASS_B
    elif firstNum >= 192 and firstNum <= 223:
        return ClassMask.CLASS_C
    elif firstNum >= 224 and firstNum <= 239:
        return ClassMask.CLASS_D
    elif firstNum >= 240 and firstNum <= 255:
        return ClassMask.CLASS_E
    

def getIPClassMask(ip):
    if (not isIp(ip)): return ClassMask.ERROR.value

    ipClasse = getIPClass(ip)

    if ipClasse == ClassMask.CLASS_A:
        return ClassMask.CLASS_A.value
    elif ipClasse == ClassMask.CLASS_B:
        return ClassMask.CLASS_B.value
    elif ipClasse == ClassMask.CLASS_C:
        return ClassMask.CLASS_C.value
    elif ipClasse == ClassMask.CLASS_D:
        return ClassMask.CLASS_D.value
    elif ipClasse == ClassMask.CLASS_E:
        return ClassMask.CLASS_E.value
    else:
        return ClassMask.ERROR.value


def getSubnet(ip, mask):
    if (not isIp(ip) or not isIp(mask)): return ClassMask.ERROR.value

    ipParts = [int(x) for x in ip.split(".")]
    maskParts = [int(x) for x in mask.split(".")]

    subnet = []
    for i in range(4):
        subnetPart = ipParts[i] & maskParts[i]
        subnet.append(str(subnetPart))

    return ".".join(subnet)




def genererTableauCIDR():
    # CIDR
    tableResult = []
    for cidr in range(8, 31):
        line = []
       
        # Binaire
        binaires = "1" * cidr + "0" * (32 - cidr)
        octets_binaires = [binaires[i:i+8] for i in range (0, 32, 8)]
        binaire_pointe = ".".join(octets_binaires)

        #Décimal
        decimal = [str(int(octet, 2)) for octet in octets_binaires]
        decimal_pointe = ".".join(decimal)


        #liste pour récupérer la valeur
        line.append(f'{cidr}')
        line.append(binaire_pointe)
        line.append(decimal_pointe)

        tableResult.append(line)

    return tableResult
