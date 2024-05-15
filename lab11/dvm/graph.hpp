#include <vector>
#include <iostream>

struct graph {
  std::vector<std::vector<int>> dist, edge;
  int n = 4;

  bool edge_exists(int u, int v) {
    return edge[u][v] != -1;
  }

  void recalc(int v, std::vector<int>& d, int edge_cost) {
    bool change = false;  

    for (int i = 0; i < n; ++i) {
      if (d[i] == -1) {
        continue;
      }

      if (dist[v][i] == -1 || dist[v][i] > d[i] + edge_cost) {
        dist[v][i] = d[i] + edge_cost; 
        change = true;
      }
    }

    if (change) {
      for (int i = 0; i < n; ++i) {
        if (edge_exists(v, i)) {
          recalc(i, dist[v], edge[v][i]);
        }
      }
    }
  }

public:

  graph() {
    dist.resize(n, std::vector(n, -1));
    for (int i = 0; i < n; ++i) {
      dist[i][i] = 0;
    }
    edge.resize(n, std::vector(n, -1));
  }

  void update_edge(int u, int v, int new_cost) {
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
        if (i == j) {
          dist[i][j] = 0;
        } else {
          dist[i][j] = -1;
        }
      }
    }

    edge[u][v] = edge[v][u] = new_cost;
    recalc(u, dist[v], new_cost);
    recalc(v, dist[u], new_cost);
  }

  void print() {
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
        std::cout << dist[i][j] << ' ';
      }
      std::cout << '\n';
    }
  }
};