from struct import *

def read_data_1byte(fname):
    infile = open(fname, 'rb')
    buffersize = 1
    buffer = infile.read(buffersize)
    data = []
    frm = "B"                   # unsigned char
    while len(buffer):
        value = unpack(frm, buffer)
        data.append(value[0])
        buffer = infile.read(buffersize)
    infile.close()
    return data


def write_data_1byte_text(fname, data):
    outfile = open(fname, 'wb')
    frm = "B"
    i = 0
    while i < len(data):
        data1 = pack(frm, ord(data[i]))
        outfile.write(data1)
        i += 1
    outfile.close()

def write_data_1byte(fname, data):
    outfile = open(fname, 'wb')
    frm = "B"
    i = 0
    while i < len(data):
        data1 = pack(frm, int(data[i]))
        outfile.write(data1)
        i += 1
    outfile.close()


def read_data_2byte(fname):
    infile = open(fname, 'rb')
    buffersize = 2
    buffer = infile.read(buffersize)
    frm = "H"                   # one integer
    data = []
    while len(buffer):
        value = unpack(frm, buffer)
        data.append(value[0])
        buffer = infile.read(buffersize)
    infile.close()
    infile.close()
    return data


def write_data_2byte(fname, data):
    outfile = open(fname, 'wb')
    frm = "H"
    i = 0
    while i < len(data):
        data1 = pack(frm, int(data[i]))
        outfile.write(data1)
        i += 1
    outfile.close()


def write_numbers(fname, numbers):
    fo = open(fname, 'w')
    for i in numbers:
        fo.write(str(i)+' ')
    fo.close()


def read_numbers(fname):
    cypher_data = read_data_1byte(fname)
    # form string
    s = ''
    for i in cypher_data:
        s += (str(chr(i)))
    s = s.split()

    # form list of large numbers
    encrypt_nums = []
    for i in s:
        encrypt_nums.append(int(i))
    return encrypt_nums


def main():
    fname = 'data_c.txt'
    data = read_data_1byte(fname)
    fname1 = 'data_2.png'
    write_data_1byte(fname1, data)

if __name__ == '__main__':
    main()
