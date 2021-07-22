#include <iostream>
#include <memory>
#include <string>

#include <reader.h>
#include <printer.h>
#include <types.h>

const std::string prompt="user> ";

std::unique_ptr<MalType> READ(const std::string& input) {
  return read_str(input);
}

std::unique_ptr<MalType> EVAL(std::unique_ptr<MalType> malType) {
  return malType;
}

std::string PRINT(std::unique_ptr<MalType> malType) {
  return pr_str(malType);
}

std::string rep(const std::string& input) {

	std::cout << "line = " << __LINE__ << std::endl;
	auto re = READ(input);
	std::cout << "line = " << __LINE__ << std::endl;
	auto ev = EVAL(std::unique_ptr<MalType>(std::move(re)));
	/* std::cout << "line = " << __LINE__ << std::endl; */
	/* auto pr = PRINT(std::unique_ptr<MalType>(std::move(ev))); */

ev->print();
	std::cout << "line = " << __LINE__ << std::endl;
return "jfdkls";
  /* return PRINT(EVAL(READ(input))); */
}

int main() {

  std::cout << prompt;

  std::string line;
  while(std::getline(std::cin, line)) {
	std::cout << "line = " << __LINE__ << std::endl;
    std::cout << rep(line) << "\n";
	std::cout << "line = " << __LINE__ << std::endl;
    std::cout << prompt;
	std::cout << "line = " << __LINE__ << std::endl;
  }

	std::cout << "line = " << __LINE__ << std::endl;
  return 0;
}

