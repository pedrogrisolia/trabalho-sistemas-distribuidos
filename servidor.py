import xmlrpc.server
import os
import logging
import sys
sys.path.append('pyDF')
from pyDF import *
from PIL import Image



logging.basicConfig(level=logging.INFO)

server = xmlrpc.server.SimpleXMLRPCServer(
    ('localhost', 9000),
    logRequests=True,
    allow_none=True
)

inputFolder = "inputImages"
outputFolder = 'outputImages'


def server_receive_file(self,directory):
        with open("inputImages/"+directory, "wb") as handle:
            handle.write(self.data)
            return True


server.register_function(server_receive_file)

def listFiles(rootdir):
    fnames = []

    for current, directories, files in os.walk(rootdir):
        for f in files:
            fnames.append(current + '/' + f)
    fnames.sort()

    return fnames

def rgb2gray(args):
    
        fname = args[0]

        imgRGB=Image.open(fname)

        img = Image.open(fname).convert('LA')
        data = imgRGB.getdata()

        grayname = fname.split('/')[-1]    
        img.save(outputFolder + '/' +  grayname.split('.')[0]  + '-gray.png')

        red = [(d[0], 0, 0) for d in data]
        green = [(0, d[1], 0) for d in data]
        blue = [(0, 0, d[2]) for d in data]

        imgRGB.putdata(red)
        redname = outputFolder + '/' + grayname.split('.')[0]  + '-red.png'
        imgRGB.save(redname)

        imgRGB.putdata(green)
        greenname = outputFolder + '/' + grayname.split('.')[0]  + '-green.png'
        imgRGB.save(greenname)

        imgRGB.putdata(blue)
        bluename = outputFolder + '/' + grayname.split('.')[0]  + '-blue.png'    
        imgRGB.save(bluename)


        return grayname


def print_name(args):
    faces = args[0]

def sucuri(nprocs):
    nprocs = nprocs
    inputPath = listFiles(inputFolder)

    graph = DFGraph()
    sched = Scheduler(graph, nprocs, mpi_enabled = False)

    feed_files = Source(inputPath)
    convert_file = FilterTagged(rgb2gray, 1) 

    pname = Serializer(print_name, 1)


    graph.add(feed_files)
    graph.add(convert_file)
    graph.add(pname)


    feed_files.add_edge(convert_file, 0)
    convert_file.add_edge(pname, 0)

    sched.start()

server.register_function(sucuri)

if __name__ == '__main__':
    try:
        print('Use Control-C to exit')
        server.serve_forever()
    except KeyboardInterrupt:
       print('Exiting')