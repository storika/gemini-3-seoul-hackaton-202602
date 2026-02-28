"""NetworkX-based knowledge graph store for KG triplet relationship traversal."""

from __future__ import annotations

from typing import Any

import networkx as nx

from .schema import KGTriplet


class BrandGraphStore:
    """Per-brand directed graph for relationship exploration.

    Nodes represent entities (subjects/objects).
    Edges carry the predicate, attributes, and triplet metadata.
    """

    def __init__(self) -> None:
        self._graphs: dict[str, nx.DiGraph] = {}
        self._triplets: dict[str, dict[str, KGTriplet]] = {}  # brand -> {id: triplet}

    def _get_graph(self, brand_namespace: str) -> nx.DiGraph:
        if brand_namespace not in self._graphs:
            self._graphs[brand_namespace] = nx.DiGraph()
            self._triplets[brand_namespace] = {}
        return self._graphs[brand_namespace]

    def add_triplet(self, triplet: KGTriplet) -> None:
        g = self._get_graph(triplet.brand_namespace)
        self._triplets[triplet.brand_namespace][triplet.id] = triplet

        g.add_node(triplet.subject, entity=True)
        g.add_node(triplet.object, entity=True)
        g.add_edge(
            triplet.subject,
            triplet.object,
            triplet_id=triplet.id,
            predicate=triplet.predicate,
            **triplet.attributes,
        )

    def get_triplet(self, brand_namespace: str, triplet_id: str) -> KGTriplet | None:
        return self._triplets.get(brand_namespace, {}).get(triplet_id)

    def get_neighbors(
        self,
        brand_namespace: str,
        entity: str,
        max_hops: int = 1,
    ) -> list[KGTriplet]:
        """Return triplets reachable from entity within max_hops."""
        g = self._get_graph(brand_namespace)
        if entity not in g:
            return []

        visited_edges: set[str] = set()
        frontier = {entity}
        results: list[KGTriplet] = []

        for _ in range(max_hops):
            next_frontier: set[str] = set()
            for node in frontier:
                # outgoing
                for _, target, data in g.out_edges(node, data=True):
                    tid = data.get("triplet_id", "")
                    if tid and tid not in visited_edges:
                        visited_edges.add(tid)
                        t = self._triplets[brand_namespace].get(tid)
                        if t:
                            results.append(t)
                        next_frontier.add(target)
                # incoming
                for source, _, data in g.in_edges(node, data=True):
                    tid = data.get("triplet_id", "")
                    if tid and tid not in visited_edges:
                        visited_edges.add(tid)
                        t = self._triplets[brand_namespace].get(tid)
                        if t:
                            results.append(t)
                        next_frontier.add(source)
            frontier = next_frontier

        return results

    def find_paths(
        self,
        brand_namespace: str,
        source: str,
        target: str,
        max_length: int = 3,
    ) -> list[list[KGTriplet]]:
        """Find all simple paths between two entities up to max_length edges."""
        g = self._get_graph(brand_namespace)
        if source not in g or target not in g:
            return []

        paths: list[list[KGTriplet]] = []
        for path_nodes in nx.all_simple_paths(g, source, target, cutoff=max_length):
            path_triplets: list[KGTriplet] = []
            for i in range(len(path_nodes) - 1):
                edge_data = g.get_edge_data(path_nodes[i], path_nodes[i + 1])
                if edge_data:
                    tid = edge_data.get("triplet_id", "")
                    t = self._triplets[brand_namespace].get(tid)
                    if t:
                        path_triplets.append(t)
            if path_triplets:
                paths.append(path_triplets)
        return paths

    def get_all_triplets(self, brand_namespace: str) -> list[KGTriplet]:
        return list(self._triplets.get(brand_namespace, {}).values())

    def get_entities(self, brand_namespace: str) -> list[str]:
        g = self._get_graph(brand_namespace)
        return list(g.nodes())

    def get_predicates(self, brand_namespace: str) -> list[str]:
        """Return unique predicate types used in the brand graph."""
        return list({
            t.predicate for t in self._triplets.get(brand_namespace, {}).values()
        })

    def entity_count(self, brand_namespace: str) -> int:
        return self._get_graph(brand_namespace).number_of_nodes()

    def triplet_count(self, brand_namespace: str) -> int:
        return len(self._triplets.get(brand_namespace, {}))
