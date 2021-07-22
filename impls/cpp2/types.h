#pragma once

#include <vector>
#include <iostream>
#include <string>

using Token= std::string;

class MalType {
public:
	virtual void print() const {
		std::cout << "Not implemented";
	}
};

class MalInteger : public MalType {
private:
  long integer;
public:
  MalInteger(const Token &token):
    integer(std::stol(token)) {
  }

	void print() const override {
		std::cout << integer;
	}
};

class MalString : public MalType {
private:
  std::string string;
public:
  MalString(const Token &token):
    string(token) {
  }

	void print() const override {
		std::cout << string;
	}
};

class MalSymbol: public MalType {
private:
  std::string symbol;
public:
  MalSymbol (const Token &token):
    symbol(token) {
  } 

	void print() const override {
		std::cout << symbol;
	}
};

class MalList : public MalType, public std::vector<std::unique_ptr<MalType>> {
private:
    std::vector<std::unique_ptr<MalType>> list;
};

