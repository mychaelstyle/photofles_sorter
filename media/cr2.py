from struct import *

recognised_tags = {
    0x0100 : 'imageWidth',
    0x0101 : 'imageLength',
    0x0102 : 'bitsPerSample',
    0x0103 : 'compression',
    0x010f : 'make',
    0x0110 : 'model',
    0x0111 : 'stripOffset',
    0x0112 : 'orientation',
    0x0117 : 'stripByteCounts',
    0x011a : 'xResolution',
    0x011b : 'yResolution',
    0x0128 : 'resolutionUnit',
    0x0132 : 'dateTime',
    0x8769 : 'EXIF',
    0x8825 : 'GPS data'};

def get_header_from_cr2( buffer ):
    # Unpack the header into a tuple
    header = unpack_from('HHLHBBL', buffer)

#    print("\nbyte_order = 0x%04X"%header[0])
#    print("tiff_magic_word = %d"%header[1])
#    print("tiff_offset = 0x%08X"%header[2])
#    print("cr2_magic_word = %d"%header[3])
#    print("cr2_major_version = %d"%header[4])
#    print("cr2_minor_version = %d"%header[5])
#    print("raw_ifd_offset = 0x%08X\n"%header[6])

    return header

def find_datetime_offset_from_cr2( buffer, ifd_offset, endian_flag ):
    (num_of_entries,) = unpack_from(endian_flag+'H', buffer, ifd_offset)
    datetime_offset = -1

    for entry_num in range(0,num_of_entries):
        (tag_id, tag_type, num_of_value, value) = unpack_from(
                endian_flag+'HHLL', buffer, ifd_offset+2+entry_num*12)
        if tag_id == 0x0132:
            assert tag_type == 2
            assert num_of_value == 20
            datetime_offset = value

    return datetime_offset

def getCR2DateTime(path):
    with open(path, "rb") as f:
        buffer = f.read(1024) 
        (byte_order, tiff_magic_word, tiff_offset, cr2_magic_word,
                cr2_major_version, cr2_minor_version, raw_ifd_offset) = get_header_from_cr2(buffer)

        endian_flag = '@'
        if byte_order == 0x4D4D:
            endian_flag = '>'
        elif byte_order == 0x4949:
            endian_flag = '<'

        datetime_offset = find_datetime_offset_from_cr2(buffer, 0x10, endian_flag)
        datetime_strings = unpack_from(20*'c', buffer, datetime_offset)

        datetime_string = ""
        for str in datetime_strings:
            datetime_string += str.decode()
        return datetime_string

