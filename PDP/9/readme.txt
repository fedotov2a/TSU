python tspg_init.py
mpicc tsp.c -std=c99 -o ./tsp
mpirun -np 10 ./tsp
python tspg_out.py

OR

python run_tsp.py

!!!
Must be installed Linux, Python 2.7, Tkinter, MPI.
!!!
