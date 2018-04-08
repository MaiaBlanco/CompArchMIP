all: matrix_inverse_cpu_GJE.cpp
	g++ -std=c++11 matrix_inverse_cpu_GJE.cpp -o cpu_par.exe -fopenmp -O3

allgp: matrix_inverse_cpu_GJE.cpp
	g++ -std=c++11 matrix_inverse_cpu_GJE.cpp -o cpu_par.exe -fopenmp -g -pg -O3


test: matrix_inverse_cpu_GJE.cpp
	g++ -std=c++11 matrix_inverse_cpu_GJE.cpp -DTEST -o test.exe -fopenmp -O3
	./test.exe
