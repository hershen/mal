#pragma once

#include <string>

#include <types.h>

std::string pr_str(const std::unique_ptr<MalType> &malType) {
  malType->print();
}
