all: test.o interface.o
	gcc -lz3 api.o test.o -o test

test.o: test.c 
	gcc -c test.c -I ../api/ -o test.o

interface.o: ../api/api.c ../api/api.h
	gcc -c ../api/api.c -o api.o

clean: 
	rm  *.o
	rm test
