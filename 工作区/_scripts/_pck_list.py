# -*- coding: utf-8 -*-
"""List Godot 4.4+ .pck entries (dir offset at header +32)."""
import struct, sys

p = sys.argv[1]
d = open(p, 'rb').read()
magic, ver, vmaj, vmin, vpatch, flags = struct.unpack_from('<IIIIII', d, 0)
file_base, dir_off = struct.unpack_from('<QQ', d, 24)
print(f"magic={magic:#x} pack={ver} engine={vmaj}.{vmin}.{vpatch} flags={flags:#x} file_base={file_base} dir={dir_off} size={len(d)}")
assert magic == 0x43504447
count = struct.unpack_from('<I', d, dir_off)[0]
off = dir_off + 4
print("file_count", count)
hits = []
ok = 0
for i in range(count):
    plen = struct.unpack_from('<I', d, off)[0]; off += 4
    path = d[off:off + plen].decode('utf-8', 'replace').rstrip('\x00'); off += plen
    ofs, size = struct.unpack_from('<QQ', d, off); off += 16
    md5 = d[off:off + 16]; off += 16
    eflags = struct.unpack_from('<I', d, off)[0]; off += 4
    ok += 1
    if 'characters/cue' in path:
        hits.append((path, ofs, size, eflags))
for h in sorted(hits):
    print(f"{h[0]:70s} off={h[1]:9d} size={h[2]:7d} flags={h[3]}")
print("parsed", ok, "cue entries", len(hits))
