#!/usr/bin/env python3
"""THE WORLD TODAY — entry runner for news-image-20261123 (b176 front-page-dense).

Stdlib only (no PIL). Validates the bundled entry.png by parsing its PNG
header and chunks manually with struct/zlib, then copies the exact bytes to
os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
Never writes next to main.py: the output dir must be outside this repo.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "dd46e04ba11bbd5ac91c0b951d091682de27f96782e8de7707e5ea75ed703865"
EXPECTED_SIZE = 142321
MAX_SIZE = 1024 * 1024
MIN_SIZE = 10000
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print("error:", msg, file=sys.stderr)
    return 1


def read_source():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as f:
        return f.read()


def validate(data):
    if len(data) < MIN_SIZE:
        return "entry.png too small (%d bytes)" % len(data)
    if len(data) > MAX_SIZE:
        return "entry.png exceeds 1 MiB (%d bytes)" % len(data)
    if data[:8] != PNG_SIG:
        return "bad PNG signature"
    # First chunk must be a 13-byte IHDR for a 1024x1024 image.
    if len(data) < 33:
        return "truncated PNG (no IHDR)"
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        return "first chunk is not a 13-byte IHDR"
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        return "unexpected dimensions %dx%d (want 1024x1024)" % (w, h)
    bit_depth, colour_type, comp, filt, interlace = data[24:29]
    if bit_depth != 8 or colour_type not in (2, 6):
        return "unexpected IHDR pixel format (depth %d, colour %d)" % (
            bit_depth, colour_type)
    if comp != 0 or filt != 0 or interlace != 0:
        return "unexpected IHDR compression/filter/interlace flags"
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != ihdr_crc:
        return "IHDR CRC mismatch"
    # Walk every chunk: check CRCs, require non-empty IDAT payload, and
    # require a 0-byte IEND as the final chunk with no trailing data.
    pos = 8
    idat_total = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return "truncated chunk header"
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + clen
        if end > len(data):
            return "truncated chunk %r" % ctype
        crc_stored = struct.unpack(">I", data[end - 4:end])[0]
        # PNG chunk CRC covers the 4-byte type plus the data, not the length.
        crc_calc = zlib.crc32(ctype + data[pos + 8:end - 4]) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            return "CRC mismatch in chunk %r" % ctype
        if ctype == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                return "IEND chunk is not 0 bytes"
            if end != len(data):
                return "trailing data after IEND"
            saw_iend = True
            break
        pos = end
    if not saw_iend:
        return "missing IEND chunk"
    if idat_total < 1000:
        return "IDAT payload too small (%d bytes)" % idat_total
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    here = os.path.dirname(os.path.abspath(__file__))
    out_abs = os.path.abspath(out_dir)
    if out_abs == os.path.abspath(here) or out_abs.startswith(
            os.path.abspath(here) + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the entry repo")
    if os.path.exists(out_abs) and not os.path.isdir(out_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    data = read_source()
    err = validate(data)
    if err:
        return fail(err)
    if len(data) != EXPECTED_SIZE:
        return fail("size mismatch: got %d, want %d" % (len(data), EXPECTED_SIZE))
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        return fail("sha256 mismatch: got %s" % sha)
    out_path = os.path.join(out_abs, "entry.png")
    if os.path.abspath(out_path) == os.path.abspath(
            os.path.join(here, "entry.png")):
        return fail("refusing to overwrite the source entry.png")
    os.makedirs(out_abs, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    # Re-read the output and confirm it is byte-identical to the source.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        return fail("output differs from source after write")
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
