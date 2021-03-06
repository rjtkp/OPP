#!/usr/bin/env python

from ctypes import *
testlib = CDLL('./py_shared.so')
natoms = 108
class Data(Structure):
    _fields_ = [("natoms",c_int),("nfi", c_int),("nsteps", c_int),("dt",c_double),("mass",c_double),("epsilon",c_double),
               ("sigma",c_double),("box",c_double),("rcut",c_double),
               ("ekin",c_double),("epot",c_double),("temp",c_double),
               ("rx",POINTER(c_double)),("ry",POINTER(c_double)),("rz",POINTER(c_double)),
               ("vx",POINTER(c_double)),("vy",POINTER(c_double)),("vz",POINTER(c_double)),
               ("fx",POINTER(c_double)),("fy",POINTER(c_double)),("fz",POINTER(c_double))]



def output( system, erg, traj):
    print(system.nfi, system.temp, system.ekin, system.epot, system.ekin+system.epot)
    erg.write("% 8d % 20.8f % 20.8f % 20.8f % 20.8f\n" % (system.nfi, system.temp, system.ekin, system.epot, system.ekin+system.epot))
    traj.write("%d\n nfi=%d etot=%20.8f\n" % (system.natoms, system.nfi, system.ekin+system.epot))
    for i in range(system.natoms):
        traj.write("Ar  %20.8f %20.8f %20.8f\n" % (system.rx[i], system.ry[i], system.rz[i]))

rx=(c_double * natoms)()
ry=(c_double * natoms)()
rz=(c_double * natoms)()
vx=(c_double * natoms)()
vy=(c_double * natoms)()
vz=(c_double * natoms)()
fx=(c_double * natoms)()
fy=(c_double * natoms)()
fz=(c_double * natoms)()

fh = open( "../examples/argon_108.inp" );

x = []
for line in fh.readlines():
    x.append( line.split()[0] )
fh.close()

system = Data()
system = Data( natoms = int(x[0]), mass = float(x[1]), nsteps = int(x[9]),epsilon = float(x[2]), sigma = float(x[3]),\
 dt = float(x[10]), box = float(x[5]), rcut = float(x[4]), rx=rx, ry=ry, rz=rz, vx=vx, vy=vy, vz=vz, fx=fx, fy=fy, fz=fz)

system.natoms = 10;
system.mass = 39.948;
system.epsilon = 0.2379;
system.sigma = 3.405;
system.rcut = 8.5;
system.box = 17.158;
system.nsteps = 1;
system.dt  = 5.0;


nprint = int(x[11])

fh = open( "../unit_test/force/argon_3.rest" );


for i in range(system.natoms):
    line=fh.readline()
    y = line.split()
    system.rx[i]=float(y[0])
    system.ry[i]=float(y[1])
    system.rz[i]=float(y[2])

for i in range(system.natoms):
    line=fh.readline()
    y = line.split()
    system.vx[i]=float(y[0])
    system.vy[i]=float(y[1])
    system.vz[i]=float(y[2])
fh.close()



for i in range(system.natoms):
	system.fx[i] = 0.0
	system.fy[i] = 0.0
	system.fz[i] = 0.0

testlib.velverlet1(byref(system)) 
testlib.velverlet2(byref(system)) 

print ("Starting simulation with ",system.natoms," atoms for ",system.nsteps," steps.")
print("\tVx \t\tVy \t\tvz")
fp = open("time_test.dat","w")
for i in range(system.natoms):
    print ("\t%f \t%f \t%f \n" % (system.rx[i], system.ry[i], system.rz[i]))
    fp.write("\t%f \t%f \t%f \n" % (system.vx[i], system.vy[i], system.vz[i]))

fp.close()
print("Simulation Done")
