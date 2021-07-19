#include <iostream>
#include <string>


const std::string prompt="user> ";

std::string READ(const std::string& input) {
  return input;
}

std::string EVAL(const std::string& input) {
  return input;
}

std::string PRINT(const std::string& input) {
  return input;
}

std::string rep(const std::string& input) {
  return PRINT(EVAL(READ(input)));
}

int main(int argc, char *argv[]) {

  std::cout << prompt << "\n";

  std::string line;
  while(std::getline(std::cin, line)) {
    std::cout << prompt << rep(line) << "\n";
  }

  std::cout << std::endl;
  return 0;
}

