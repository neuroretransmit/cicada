# Makefile

CC = nvcc
CFLAGS = -arch=sm_60

all: primesieve

primesieve: primesieve.cu
	$(CC) $(CFLAGS) -lgmp $< -o $@

clean:
	rm -f primesieve