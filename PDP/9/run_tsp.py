import os

np = int(raw_input("np: "))

os.system("python tspg_init.py")
os.system("mpicc tsp.c -std=c99 -o ./tsp")
os.system("mpirun -np " + str(np) + " ./tsp")
os.system("python tspg_out.py")