from typing import List


class Graph(object):
    def __init__(self, edges: List[tuple], directed: bool):
        self.g = dict()
        self.ns = set()

        if directed:
            self.es = edges + [edge[::-1] for edge in edges]
        else:
            self.es = edges

        for e in self.es:
            self.ns.add(e[0])
            self.ns.add(e[1])

            try:
                self.g[e[0]].add(e[1])
            except KeyError:
                self.g[e[0]] = {e[1]}

        self.num_nodes = len(self.ns)

        for i in range(self.num_nodes):
            if i not in self.g:
                self.g[i] = set()

    def breadth_first_search(self, start_idx: int) -> List[tuple]:
        v = [False] * self.num_nodes
        v[start_idx] = True

        q = [start_idx]

        path = []

        while len(q) > 0:
            curr = q.pop(0)

            for n in self.g[curr]:
                if v[n] is False:
                    q.append(n)
                    path.append((curr, n))
                    v[n] = True

        return path
