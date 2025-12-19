CC = gcc
FILE = $(1)
ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

all: res

asm:
	echo $(ROOT_DIR)
	cd $(ROOT_DIR)
	$(CC) -O0 $(FILE).c -S -o $(FILE).s

compile: asm
	cd $(ROOT_DIR)
	$(CC) $(FILE).s -o $(FILE).exe

run: asm compile
	cd $(ROOT_DIR)
	./$(FILE).exe

res: asm compile run
	echo result: $?

clean:
	rm -rf *.exe *.s

redo: clean res
