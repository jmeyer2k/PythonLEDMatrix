import serial
import time
import letters
class Matrix:
    def __init__(self, port):
        self.__ser = serial.Serial(port, 9600)
        self.__rmap = [[False for x in range(8)] for x in range(8)]
        self.__bmap = [[False for x in range(8)] for x in range(8)]
        self.__gmap = [[False for x in range(8)] for x in range(8)]
    def mapAsHex(self):
        redRows=[]
        for x in self.__rmap:
            row = chr(int("".join(reversed([str(int(y)) for y in x])), 2))
            redRows.append(row)
        redHex  = "".join(reversed(redRows))
        blueRows=[]
        for x in self.__bmap:
            row = chr(int("".join(reversed([str(int(y)) for y in x])), 2))
            blueRows.append(row)
        blueHex  = "".join(reversed(blueRows))
        greenRows=[]
        for x in self.__gmap:
            row = chr(int("".join(reversed([str(int(y)) for y in x])), 2))
            greenRows.append(row)
        greenHex  = "".join(greenRows)
        assert len(redHex+greenHex+blueHex)==24
        return redHex+greenHex+blueHex
    def writeToArduino(self):
        self.__ser.write(self.mapAsHex())
    def set(self, x, y, color, value):
        if x<8 and x>=0 and y<8 and y>=0:
            assert x<8 and y<8
            if color=="r":
                self.__rmap[y][x]=value
            elif color=="g":
                self.__gmap[y][x]=value
                print y-1
            elif color=="b":
                self.__bmap[y][x]=value
    def display(self, disp, color, offx=0, offy=0):
        offx=8-offx
        offy=8-offy
        y=0
        for row in disp:
            rowbin = bin(int(row, 16))[2:].zfill(8)
            x=0
            for bit in rowbin:
                if bit=="1":
                    self.set(x-offx, y+offy, color, True)
                else:
                    self.set(x-offx, y+offy, color, False)
                x+=1
            y+=1
    def clear(self, color):
        if color=="r":
            self.__rmap=[[False for x in range(8)] for x in range(8)]
        elif color=="g":
            self.__gmap=[[False for x in range(8)] for x in range(8)]
        elif color=="b":
            self.__bmap=[[False for x in range(8)] for x in range(8)]
        elif color=="a":
            self.__rmap=[[False for x in range(8)] for x in range(8)]
            self.__gmap=[[False for x in range(8)] for x in range(8)]
            self.__bmap=[[False for x in range(8)] for x in range(8)]
    def close(self):
        self.__ser.close()
if __name__== '__main__':
    m = Matrix("/dev/tty.usbmodemfa131")
    i=0
    times = 10
    # m.clear("a")
    m.writeToArduino()
    for bla in range(times):
        tx=-6
        ty=6
        rx=0
        ry=6
        while tx<13:
            m.display(letters.j, "r", tx, ty)
            m.display(letters.m, "b", rx, ry)
            m.writeToArduino()
            time.sleep(0.09)
            tx+=1
            rx+=1
        time.sleep(0.1)
    m.close()
    # time.sleep(1)e
    # m.clear("a")
    # m.writeToArduino()
    # time.sleep(1)
    # m.set(5,5,"r", True)
    # m.set(5,4,"b", True)
    # m.set(4,5,"b", True)
    # m.set(5,6,"g", True)
    # m.set(6,5,"g", True)
    m.writeToArduino()