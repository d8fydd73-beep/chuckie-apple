"""Assemble CHUCKIE APPLE v2 and wrap it as a BBC tape image (UEF) and a
disc image (SSD).   Usage: python3 build.py <path-to-beebasm>"""
import re, struct, subprocess, sys

def crc(data):
    c = 0
    for b in data:
        c ^= b << 8
        for _ in range(8):
            if c & 0x8000: c = (((c ^ 0x0810) << 1) | 1) & 0xFFFF
            else: c = (c << 1) & 0xFFFF
    return c

def chunk(cid, data): return struct.pack('<HI', cid, len(data)) + data

def make_uef(name, data, load=0xFFFF0E00, exe=0xFFFF8023):
    out = bytearray(b'UEF File!\x00\x0A\x00')
    blocks = [data[i:i+256] for i in range(0, len(data), 256)]
    for n, blk in enumerate(blocks):
        last = n == len(blocks)-1
        hdr = name.encode() + b'\x00' + struct.pack('<IIHHB', load, exe, n, len(blk), 0x80 if last else 0) + b'\x00'*4
        body = b'\x2A' + hdr + struct.pack('>H', crc(hdr)) + blk + struct.pack('>H', crc(blk))
        out += chunk(0x0110, struct.pack('<H', 12000 if n == 0 else 1500))
        out += chunk(0x0100, body)
    out += chunk(0x0110, struct.pack('<H', 1500))
    return bytes(out)



if __name__ == "__main__":
    bb = sys.argv[1]
    subprocess.run([sys.executable, "gen_data.py"], stdout=open("data.6502", "w"), check=True)
    out = subprocess.run([bb, "-i", "apple.6502", "-o", "APPLE.bin", "-v"],
                         check=True, capture_output=True, text=True).stdout
    for l in out.splitlines():
        if l.startswith(("Zero", "Program", "EXEC")): print(l)
    exe = int(re.search(r"^EXEC\s*(?:&)?([0-9A-Fa-f]+)", out, re.M).group(1), 16)
    code = open("APPLE.bin", "rb").read()
    # &FFFF in the top half of the address keeps it in the BBC itself,
    # even with a second processor attached
    open("APPLE.uef", "wb").write(make_uef("APPLE", code, load=0xFFFF1900, exe=0xFFFF0000 | exe))
    subprocess.run([bb, "-i", "apple.6502", "-o", "APPLE", "-do", "APPLE.ssd",
                    "-boot", "APPLE", "-title", "APPLE"], check=True, stdout=subprocess.DEVNULL)
    print("APPLE.uef: %d bytes, load &1900, exec &%04X, length &%X" % (len(code), exe, len(code)))
