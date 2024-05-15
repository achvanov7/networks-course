#include "graph.hpp"
#include <sstream>

int main() {
  graph dvm;
  dvm.update_edge(0, 1, 1);
  dvm.update_edge(1, 2, 1);
  dvm.update_edge(0, 2, 3);
  dvm.update_edge(0, 3, 7);
  dvm.update_edge(2, 3, 2);
  dvm.print();
  std::cout << '\n';

  while (true) {
    std::cout << "Enter the new egde cost (u, v, cost) or end the program \"end\"\n";
    std::string input;
    std::getline(std::cin, input);
    if (input == "end") {
      break;
    }
    
    std::stringstream in(input);
    int u, v, cost;
    in >> u >> v >> cost;
    dvm.update_edge(u, v, cost);

    dvm.print();
    std::cout << '\n';
  }
}