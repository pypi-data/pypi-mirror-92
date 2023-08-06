
from enum import Enum
import os
import time
import sys

from select import epoll, EPOLLET, EPOLLPRI, EPOLLOUT, EPOLLIN
from threading import Thread

class Gpio:
    attrib = ('value', 'direction', 'active_low', 'edge')

    IN = 'in\n'
    OUT = 'out\n'

    NONE = 'none\n'
    RISING = 'rising\n'
    FALLING = 'falling\n'
    BOTH = 'both\n'

    def __init__(self, num):
        self.num = num
        self._file = {}

        self.basepath = f'/sys/class/gpio/gpio{num}'

        if os.path.isdir(self.basepath) == False:
            with open('/sys/class/gpio/export', 'w') as exp:
                exp.write(f'{num}')

        time.sleep(0.1)

        for name in self.attrib:
            self._file[name] = open(os.path.join(self.basepath, name), 'w+b', buffering=0)

    def __del__(self):
        fdexp = os.open('/sys/class/gpio/unexport', os.O_WRONLY)
        os.write(fdexp, bytes(f'{self.num}\n'.encode()))
        os.close(fdexp)

    def _write(self, name, val):
        fd = self._file[name]
        fd.seek(0)
        fd.write(val.encode('ascii'))

    def _read(self, name):
        fd = self._file[name]
        fd.seek(0)
        return fd.read()
        
    def direction(self, dir):
        self._write('direction', dir)
    def edge(self, edge):
        self._write('edge', edge)
    def input(self):
        return self._read('value')
    def output(self, value):
        self._write('value', value)

    def setisr(self, isr):
        if callable(isr):
            self.po = epoll()
            self.po.register(self._file['value'],  EPOLLIN | EPOLLET )
            self.isr = isr
            def isrproc():
                while True:
                    events = self.po.poll()
                    for fileno, evt in events:
                        if fileno == self._file['value'].fileno():
                            self.isr()
            
            t = Thread(target=isrproc)
            t.start()
        else:
            print('cannot call')

if __name__ == "__main__":
    iotest = [Gpio(504), Gpio(505),Gpio(506),Gpio(508)]
    func = [
        lambda:print(f'iotest{0} isr'),
        lambda:print(f'iotest{1} isr'),
        lambda:print(f'iotest{2} isr'),
        lambda:print(f'iotest{3} isr')
    ]
    for i, io in enumerate(iotest):
        print(i,io)
        io.direction(Gpio.IN)
        io.edge(Gpio.RISING)
        
        io.setisr(func[i])
        
    print('poll start')
    cnt = 0
    while True:
        print(f'poll {cnt}')
        cnt += 1
        time.sleep(0.5)
        
    