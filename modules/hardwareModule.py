import hashlib

__all__ = ['getHardwareID']

def _hash(input_string):
    sha512_hash = hashlib.sha512()
    sha512_hash.update(input_string.encode('utf-8'))
    return sha512_hash.hexdigest()

def _get_cpu_serial():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.strip().split(": ")[1]
    except FileNotFoundError:
        return None

def _get_ram_size():
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal'):
                    mem_total_kb = int(line.split()[1])
                    mem_total_mb = mem_total_kb / 1024
                    return f"{mem_total_mb:.2f}"
    except FileNotFoundError:
        return None

def _get_sd_card_id():
    try:
        with open('/sys/block/mmcblk0/device/cid', 'r') as f:
            cid = f.readline().strip()
            return cid
    except FileNotFoundError:
        return None

#def _get_wifi_mac_address():


def getHardwareID():
    serial = _get_cpu_serial()
    ram_size = _get_ram_size()
    sd_id = _get_sd_card_id()

    hardwareID = ''

    if serial!=None and ram_size!=None and sd_id!=None   :
        hardwareID = serial+ram_size+sd_id 
        hardwareIDHashed = _hash(hardwareID)
        return hardwareIDHashed
    else:
        return 'Error: The Hardware ID was not generated.'




