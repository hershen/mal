CXX=~/llvm/llvm-project/build/bin/clang++

LD=$(CXX)
AR=ar

DEBUG=-ggdb

FLAGS=-Wextra -Wpedantic -Wunused-variable

CXXFLAGS=-O3 $(FLAGS) $(DEBUG) $(INCPATHS) -std=c++20 -stdlib=libc++
LDFLAGS=-O3 $(DEBUG) $(LIBPATHS) -L. -stdlib=libc++

.PHONY:	clean all

TARGETS=$(basename $(wildcard step*.cpp))

all: $(TARGETS)

step0_repl: step0_repl.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
	
step1_read_pring: step1_read_pring.cpp types.h reader.h printer.h
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm  -f *.o $(TARGETS) 
