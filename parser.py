import struct
from numpy import *
import Image

class AFMParser(object):

    def __init__(self, filename):
        self.filename = filename
        self.header = self.get_header()
        self.type_format = "h"

    def get_header(self):
        file = open(self.filename, "r")
        res = []
        for line in file:
            trimmed = line.rstrip().replace("\\", "")
            res.append(trimmed)
            if "*File list end" in trimmed:
                break
        file.close()
        return res

    def find_in_header(self, key):
        return [line for line in self.header if key in line]

    def between(self, left, right, s):
        before,_,a = s.partition(left)
        a, _, after = a.partition(right)
        return a

    def get_scale(self, str):
        return float(self.between("(", " V/LSB)", str))

    def read(self, layer=0):

        scal_data= self.find_in_header("@2:Z scale: V [Sens.")
        pos_spl = self.find_in_header("Samps")
        pos_data = self.find_in_header("Data offset")
        file_type_data = self.find_in_header("Image Data")

        spl = linno = int(pos_spl[layer].split(": ")[1])
        offsets = [int(offset.split(": ")[1]) for offset in pos_data]
        data = [self.read_at_offset(i, spl, linno) for i in offsets]

        try:
            scale = self.get_scale(scal_data[layer])
        except IndexError:
            scale=1.0

        rot_and_scaled = rot90(data[layer]*scale)

        print file_type_data[layer]
        img = Image.fromarray(rot_and_scaled, mode='L')
        img.show()

    def read_at_offset(self, offset, rows, cols):
        data_size = struct.calcsize(self.type_format)

        f = open(self.filename, "rb")
        f.seek(offset)
        #data = []
        data = zeros((rows, cols))
        num_elements = rows * cols
        try:
            index = col = row = 0
            while index < num_elements:
                value = f.read(data_size)
                try:
                    data[row][col] = struct.unpack(self.type_format, value)[0]
                except Exception:
                    pass

                if row == rows - 1:
                    col+=1
                    row=0
                else:
                    row+=1
                index += 1

        finally:
            f.close()
        return data

parser = AFMParser("data/POPC.193")
parser.read(layer=0)