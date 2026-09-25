"""Reference loops among the entries an importer reads. An importer drops
an entry whose references lead back to itself and names the loop; the
DTCG and Figma importers find those loops here."""
from __future__ import annotations

from collections import deque
from typing import Callable, Dict, List, Optional, Set


def cycles(order: List[str], succ: Callable[[str], List[str]]) -> Dict[str, List[str]]:
    """Each node on a reference loop, with the loop from it back to it
    (Tarjan's strongly connected components, iterative). `succ` gives the
    nodes a node references; a node that references itself is a loop."""
    index: Dict[str, int] = {}
    low: Dict[str, int] = {}
    stack: List[str] = []
    on: Set[str] = set()
    loops: Dict[str, List[str]] = {}
    for start in order:
        if start in index:
            continue
        index[start] = low[start] = len(index)
        stack.append(start)
        on.add(start)
        work = [(start, iter(succ(start)))]
        while work:
            v, it = work[-1]
            for w in it:
                if w not in index:
                    index[w] = low[w] = len(index)
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(succ(w))))
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp: List[str] = []
                    while True:
                        w = stack.pop()
                        on.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    if len(comp) > 1 or v in succ(v):
                        members = set(comp)
                        for m in comp:
                            loops[m] = loop(m, members, succ)
    return loops


def loop(m: str, members: Set[str], succ: Callable[[str], List[str]]) -> List[str]:
    """The shortest path from m back to m inside one loop."""
    parent: Dict[str, Optional[str]] = {m: None}
    queue = deque([m])
    while queue:
        x = queue.popleft()
        for y in succ(x):
            if y == m:
                path = [x]
                while parent[path[-1]] is not None:
                    path.append(parent[path[-1]])
                return path[::-1] + [m]
            if y in members and y not in parent:
                parent[y] = x
                queue.append(y)
    return [m, m]
