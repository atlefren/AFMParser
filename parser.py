import struct
from numpy import *

def between(left, right, s):
    before,_,a = s.partition(left)
    a, _, after = a.partition(right)
    return a

class AFMParser(object):

    def __init__(self, filename):
        self.filename = filename
        self.header = self._get_header()
        self.type_format = "h"
        self.scans = self.get_scans()

    def get_scans(self):
        scans = []
        scan_counter = -1
        for line in self.header:
            if line == "*Ciao image list":
                scan_counter += 1
                scans.append({})
            if scan_counter >= 0 and not line.startswith('*'):
                split = line.split(": ")
                try:
                    scans[scan_counter][split[0]] = split[1]
                except IndexError:
                    scans[scan_counter][split[0]] = None
        return scans

    def get_scale(self, layer):
        scal_data= self._find_in_header("@2:Z scale: V [Sens.")
        try:
            return float(between("(", " V/LSB)", scal_data[layer]))
        except IndexError:
            return 1.0

    def get_layer_name(self, layer=0):
        file_type_data = self.scans[layer]["@2:Image Data"]
        return between("\"", "\"", file_type_data[layer])

    def read_layer(self, layer=0):
        offset = int(self.scans[layer]["Data offset"])
        rows = int(self.scans[layer]["Number of lines"])
        cols = int(self.scans[layer]["Samps/line"])
        return rot90(self._read_at_offset(offset, rows, cols) * self.get_scale(layer))

    def get_size_and_unit(self):
        pass

    def _get_header(self):
        """
        Read the header into an array for easy lookup
        """
        file = open(self.filename, "r")
        res = []
        for line in file:
            trimmed = line.rstrip().replace("\\", "")
            res.append(trimmed)
            if "*File list end" in trimmed:
                break
        file.close()
        return res

    def _find_in_header(self, key):
        return [line for line in self.header if key in line]

    def _read_at_offset(self, offset, rows, cols):
        data_size = struct.calcsize(self.type_format)

        f = open(self.filename, "rb")
        f.seek(offset)
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