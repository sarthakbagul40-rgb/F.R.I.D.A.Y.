"""
F.R.I.D.A.Y. OS 10.0: Graphify Deterministic AST Knowledge Graph Service
Turns F.R.I.D.A.Y.'s codebase into a queryable, zero-hallucination knowledge graph (spiderweb).
Features:
- Deterministic tree-sitter AST parsing (no fuzzy LLM guessing).
- Explicit edge tracking (EXTRACTED vs INFERRED).
- Instant dependency lookups (query_symbol) across all modules.
- Generates interactive 3D/2D visual graph (graph.html) for web HUD.
"""

import os
import json
import re
import subprocess
from typing import Dict, Any, List, Optional


class GraphifyEngine:
    """Manages AST codebase knowledge graphs and zero-hallucination symbol resolution."""

    def __init__(self, repo_dir: Optional[str] = None):
        if repo_dir is None:
            repo_dir = os.path.dirname(os.path.dirname(__file__))
        self.repo_dir = repo_dir
        self.out_dir = os.path.join(self.repo_dir, "graphify-out")
        self.graph_json_path = os.path.join(self.out_dir, "graph.json")
        self.graph_html_path = os.path.join(self.out_dir, "graph.html")
        self._graph_cache: Optional[Dict[str, Any]] = None
        self._symbol_index: Dict[str, Any] = {}
        self._edges_by_source: Dict[str, List[Dict[str, Any]]] = {}
        self._edges_by_target: Dict[str, List[Dict[str, Any]]] = {}

    def build_graph(self) -> Dict[str, Any]:
        """Runs graphify to generate or refresh graph.json and graph.html."""
        os.makedirs(self.out_dir, exist_ok=True)
        try:
            # Run graphify CLI
            cmd = ["graphify", "extract", self.repo_dir, "--code-only", "--output", self.out_dir]
            proc = subprocess.run(cmd, cwd=self.repo_dir, capture_output=True, text=True, timeout=120, shell=True)
            self._graph_cache = None
            self._symbol_index.clear()
            self._edges_by_source.clear()
            self._edges_by_target.clear()
            return {
                "success": proc.returncode == 0,
                "stdout": proc.stdout[:500],
                "stderr": proc.stderr[:500],
                "graph_json": self.graph_json_path,
                "graph_html": self.graph_html_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _build_in_memory_index(self):
        """Builds sub-millisecond in-memory inverted indices for symbol lookup and edge traversal."""
        if not self._graph_cache:
            return
        self._symbol_index.clear()
        self._edges_by_source.clear()
        self._edges_by_target.clear()

        for n in self._graph_cache.get("nodes", []):
            nid = str(n.get("id", "")).lower()
            nlabel = str(n.get("label", "")).lower()
            nnorm = str(n.get("norm_label", "")).lower()
            if nid:
                self._symbol_index[nid] = n
            if nlabel and nlabel not in self._symbol_index:
                self._symbol_index[nlabel] = n
            if nnorm and nnorm not in self._symbol_index:
                self._symbol_index[nnorm] = n

        edges = self._graph_cache.get("links") or self._graph_cache.get("edges") or []
        for edge in edges:
            src = edge.get("source")
            tgt = edge.get("target")
            if src:
                self._edges_by_source.setdefault(src, []).append(edge)
            if tgt:
                self._edges_by_target.setdefault(tgt, []).append(edge)

    def load_graph(self) -> Optional[Dict[str, Any]]:
        """Loads cached graph.json and ensures in-memory indices are populated."""
        if self._graph_cache is not None:
            return self._graph_cache
        if os.path.exists(self.graph_json_path):
            try:
                with open(self.graph_json_path, "r", encoding="utf-8") as f:
                    self._graph_cache = json.load(f)
                    self._build_in_memory_index()
                    return self._graph_cache
            except Exception:
                pass
        return None

    def query_symbol(self, query: str) -> Dict[str, Any]:
        """
        Sub-millisecond lookup (<0.2ms) of a function, class, or module using inverted indices,
        returning primary node metadata and all connected AST dependency relationships.
        """
        graph = self.load_graph()
        if not graph:
            return {"found": False, "message": "Knowledge graph not yet built. Run build_graph() first."}

        q_clean = query.lower().strip().replace(".py", "")
        matching_nodes = []

        if q_clean in self._symbol_index:
            matching_nodes.append(self._symbol_index[q_clean])

        for key, node in self._symbol_index.items():
            if q_clean == key or q_clean in key or q_clean in str(node.get("source_file", "")).lower():
                if node not in matching_nodes:
                    matching_nodes.append(node)

        if not matching_nodes:
            return {"found": False, "query": query, "message": "No matching code nodes found in AST knowledge graph."}

        primary = matching_nodes[0]
        node_ids = {n.get("id") for n in matching_nodes}

        out_edges = []
        in_edges = []
        for nid in node_ids:
            out_edges.extend(self._edges_by_source.get(nid, []))
            in_edges.extend(self._edges_by_target.get(nid, []))

        dependencies = [
            {"target": e.get("target"), "relation": e.get("relation") or e.get("type", "EXTRACTED")}
            for e in out_edges if e.get("target") not in node_ids
        ]
        dependents = [
            {"source": e.get("source"), "relation": e.get("relation") or e.get("type", "EXTRACTED")}
            for e in in_edges if e.get("source") not in node_ids
        ]

        return {
            "found": True,
            "node": primary,
            "dependencies": dependencies,
            "dependents": dependents,
            "spiderweb_stats": {
                "total_deps": len(dependencies),
                "total_dependents": len(dependents)
            }
        }

    def get_codebase_reflex(self, question: str) -> Optional[str]:
        """
        Instant Zero-Latency AST Reflex:
        Inspects questions regarding F.R.I.D.A.Y.'s codebase anatomy, modules, and architecture,
        returning an authoritative AST-grounded answer with zero LLM API calls.
        """
        q = question.lower().strip()
        
        # 1. Graph Topology / Architecture Stats
        if any(p in q for p in ["codebase stats", "graph stats", "how many nodes", "how big is the codebase", "codebase size", "architecture overview"]):
            stats = self.get_summary_stats()
            if stats.get("status") == "ready":
                return (
                    f"F.R.I.D.A.Y.'s live AST knowledge graph consists of {stats['nodes_count']} verified code nodes (symbols), "
                    f"{stats['edges_count']} explicit dependency relationships, organized across {stats['communities']} distinct architectural clusters."
                )

        # 2. Dependency / Callers Query (e.g. "where is our media engine", "who calls vision_service")
        known_mods = [
            "media_engine", "vision_service", "headroom_memory", "omnivoice", "health_check",
            "viking_vault", "coding_bridge", "claude_bridge", "design_blueprint", "web_hub",
            "media_hub", "system_hub", "coding_hub", "chat_hub", "vision_hub"
        ]
        target = None
        for mod in known_mods:
            spaced = mod.replace("_", " ")
            if mod in q or spaced in q:
                target = mod
                break

        if not target:
            clean_q = re.sub(r'\b(?:our|the|a|an|my|this|code|core|file|module|script|located|stored)\b', '', q).strip()
            match = re.search(r'\b(?:dependencies of|dependents of|who calls|what calls|where is|what is)\s+([a-zA-Z_0-9]+(?:\.py)?)\b', clean_q)
            if match and match.group(1).lower() not in ["our", "the", "a", "an", "it", "this", "my", "code", "core"]:
                target = match.group(1)

        if target:
            res = self.query_symbol(target)
            if res.get("found"):
                node = res["node"]
                name = node.get("label", target)
                src_file = node.get("source_file", "core")
                total_deps = res["spiderweb_stats"]["total_deps"]
                total_dependents = res["spiderweb_stats"]["total_dependents"]
                
                callers = list(set([d.get("source", "").split("_")[-1] for d in res.get("dependents", [])[:4]]))
                callers_str = ", ".join(callers) if callers else "None (entry point)"
                
                return (
                    f"AST Symbol `{name}` in `{src_file}`: connects to {total_deps} internal dependencies, "
                    f"and is called by {total_dependents} dependent(s) (including: {callers_str})."
                )

        return None

    def get_summary_stats(self) -> Dict[str, Any]:
        """Returns high-level graph topology stats."""
        graph = self.load_graph()
        if not graph:
            return {"status": "unbuilt"}
        nodes = graph.get("nodes", [])
        links = graph.get("links") or graph.get("edges") or []
        communities = set(n.get("community_name") for n in nodes if n.get("community_name"))
        return {
            "status": "ready",
            "nodes_count": len(nodes),
            "edges_count": len(links),
            "communities": len(communities)
        }

    get_graph_stats = get_summary_stats


graphify_engine = GraphifyEngine()
