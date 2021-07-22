#pragma once

#include <algorithm>
#include <cctype>
#include <vector>
#include <iterator>
#include <memory>
#include <string>

#include "types.h"

const std::string specialChars = "[]{}()'`~^@";
const std::string extraSpecialChars = ",\";";

class Reader {

private:
  std::vector<Token> tokens;
  std::vector<Token>::const_iterator iterator;

public:
  Reader(const std::vector<Token>& tokens) :
    tokens(tokens) {
      iterator = tokens.begin();
    };
  
  std::string next() {
    return *iterator++;
  }
  
  std::string peek() const {
    return *iterator;
  }
};

std::unique_ptr<MalType> read_atom(Reader &reader);
std::unique_ptr<MalType> read_form(Reader &reader);
std::unique_ptr<MalList> read_list(Reader &reader);


//From cppreference documentation of isspace
bool safe_isspace(char ch)
{
    return std::isspace(static_cast<unsigned char>(ch));
}


std::vector<Token> tokenize(std::string line) {
  std::vector<Token> tokens;
  tokens.reserve(line.size());

  const auto notAtDoubleQuote = [](const auto& string, const auto& idx) {
    return string[idx] != '\"';
  };
  const auto atSlashDoubleQuote = [](const auto& string, const auto& idx) {
    return (string[idx] == '\"' and string[idx-1] == '\\');
  };

  size_t idx = 0;
  //Ignore leading whitespace and commas
  while(safe_isspace(line[idx]) or line[idx] == ',') {
    idx++;
  }

  for(; idx < line.size(); idx++) {
    // ~@
    if (idx + 1 < line.size() and line[idx] == '~' and line[idx+1] == '@') {
      tokens.push_back("~@");
      idx++;
    }

    //Special charecters
    else if (specialChars.find(line[idx]) != std::string::npos) {
      tokens.push_back(line.substr(idx, idx+1));
    }

    // ;
    else if (line[idx] == ';') {
      tokens.push_back( line.substr(idx));
      break;
    }

    // Enclosed in double quotes
    else if(line[idx] == '\"') {
      size_t endIdx = idx+1;
      while (endIdx < line.size() and (notAtDoubleQuote(line, endIdx) or atSlashDoubleQuote(line, endIdx))) {
        endIdx++;
      }

      if (line[endIdx] != '\"') {
        //report Error
      }

      if (endIdx != line.size()) {
        tokens.push_back( line.substr(idx, endIdx));
      } 
      
      idx = endIdx + 1;
    }

    //Non special charecters
    else {
      size_t endIdx = idx;
      while(endIdx < line.size() and specialChars.find(line[endIdx]) != std::string::npos and extraSpecialChars.find(line[endIdx]) != std::string::npos) {
        endIdx++;
      }

      if(endIdx > idx) {
        tokens.push_back(line.substr(idx, endIdx));
        idx = endIdx;
      }
    }
  }

  /* std::cout << line.substr(idx) << std::endl; */
  return tokens;
}

std::unique_ptr<MalType> read_atom(Reader &reader) {
  const auto token = reader.next();

  //Numbers
  if(!token.empty() && std::isdigit(token[0])) {
    return std::make_unique<MalInteger>(token);
  } else if(specialChars.find(token[0]) != std::string::npos) {
    return std::make_unique<MalSymbol>(token);
  } else {
    //return error
  }
}

std::unique_ptr<MalList> read_list(Reader &reader) {
	return std::make_unique<MalList>();
  MalList list;
  auto malThing = MalType();
  /* MalSymbol closeParensSymbol(")"); */
  /* do { */
  /*   malThing = read_form(reader); */
  /*   list.push_back(malThing); */
  /* } while (malThing != closeParensSymbol); */
}

std::unique_ptr<MalType> read_form(Reader &reader) {
  if(reader.peek() == "(") {
		return read_list(reader);
  }
  else {
    return read_atom(reader);
  }
}

std::unique_ptr<MalType> read_str(const std::string& line) {
  const auto tokens = tokenize(line);
  Reader reader(tokens);
  return read_form(reader);
}

