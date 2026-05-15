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

    parts = ip.split(".")
    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False

        value = int(part)
        if value < 0 or value > 255:
            return False

    return True


def isSubnetMask(mask):
    normalized = parse_mask(mask)
    if not normalized:
        return False

    bits = []
    for part in normalized.split("."):
        bits.append(f"{int(part):08b}")

    return "01" not in "".join(bits)


def _ip_to_int(ip):
    parts = [int(part) for part in ip.split(".")]
    return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]


def _int_to_ip(value):
    return ".".join(str((value >> shift) & 255) for shift in (24, 16, 8, 0))


def parse_mask(mask):
    if not isinstance(mask, str):
        return None

    cleaned = mask.strip()
    if cleaned.startswith("/"):
        cleaned = cleaned[1:]

    if cleaned.isdigit():
        cidr = int(cleaned)
        if cidr < 0 or cidr > 32:
            return None
        return cidr_to_mask(cidr)

    if isIp(cleaned):
        return cleaned

    return None


def cidr_to_mask(cidr):
    bits = "1" * cidr + "0" * (32 - cidr)
    octets = []

    for i in range(0, 32, 8):
        octets.append(str(int(bits[i:i + 8], 2)))

    return ".".join(octets)

def isClassFull(mask):
    normalized = parse_mask(mask)
    if not normalized:
        return "error"

    return normalized in {
        ClassMask.CLASS_A.value,
        ClassMask.CLASS_B.value,
        ClassMask.CLASS_C.value,
    }


def isPrivateIp(ip):
    if not isIp(ip):
        return False

    parts = ip.split(".")
    first = int(parts[0])
    second = int(parts[1])

    if first == 10:
        return True

    if first == 172 and 16 <= second <= 31:
        return True

    if first == 192 and second == 168:
        return True

    return False


def isReservedIp(ip):
    if not isIp(ip):
        return False

    first = int(ip.split(".")[0])

    if first == 0:
        return True

    if first == 127:
        return True

    if 224 <= first <= 239:
        return True

    if 240 <= first <= 255:
        return True

    return False


def getIPClass(ip):
    if not isIp(ip):
        return ClassMask.ERROR

    firstNum = int(ip.split(".")[0])

    if 0 <= firstNum <= 127:
        return ClassMask.CLASS_A
    elif 128 <= firstNum <= 191:
        return ClassMask.CLASS_B
    elif 192 <= firstNum <= 223:
        return ClassMask.CLASS_C
    elif 224 <= firstNum <= 239:
        return ClassMask.CLASS_D
    elif 240 <= firstNum <= 255:
        return ClassMask.CLASS_E

    return ClassMask.ERROR
    

def getIPClassMask(ip):
    if not isIp(ip):
        return ClassMask.ERROR.value

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
    normalized = parse_mask(mask)
    if not isIp(ip) or not normalized:
        return ClassMask.ERROR.value

    if isClassFull(normalized) != True:
        return ClassMask.ERROR.value

    return getNetworkAddress(ip, normalized)


def getNetworkAddress(ip, mask):
    normalized = parse_mask(mask)
    if not isIp(ip) or not normalized:
        return ClassMask.ERROR.value

    ip_value = _ip_to_int(ip)
    mask_value = _ip_to_int(normalized)
    return _int_to_ip(ip_value & mask_value)


def areIpsInSameNetwork(ip1, mask1, ip2, mask2):
    if not isIp(ip1) or not isIp(ip2):
        return False

    normalized_1 = parse_mask(mask1)
    normalized_2 = parse_mask(mask2)
    if not normalized_1 or not normalized_2:
        return False

    if not isSubnetMask(normalized_1) or not isSubnetMask(normalized_2):
        return False

    network_from_1 = getNetworkAddress(ip1, normalized_1)
    network_from_2 = getNetworkAddress(ip2, normalized_2)

    if network_from_1 == ClassMask.ERROR.value or network_from_2 == ClassMask.ERROR.value:
        return False

    return (
        getNetworkAddress(ip1, normalized_1) == getNetworkAddress(ip2, normalized_1)
        and getNetworkAddress(ip2, normalized_2) == getNetworkAddress(ip1, normalized_2)
    )




def genererTableauCIDR():
    tableResult = []
    for cidr in range(8, 31):
        line = []

        binaires = "1" * cidr + "0" * (32 - cidr)
        octets_binaires = []

        for i in range(0, 32, 8):
            octets_binaires.append(binaires[i:i + 8])

        binaire_pointe = ".".join(octets_binaires)

        decimal = []
        for octet in octets_binaires:
            decimal.append(str(int(octet, 2)))

        decimal_pointe = ".".join(decimal)

        line.append(f'{cidr}')
        line.append(binaire_pointe)
        line.append(decimal_pointe)

        tableResult.append(line)

    return tableResult
