"""
F.R.I.D.A.Y. OS 10.0: Ralph Flow Autonomous Execution Loop
Implements the autonomous self-referential loop for multi-step feature development:
1. Parse PRD/Task Queue.
2. Select next incomplete task.
3. Dispatch to Coding Engine (Claude Bridge / OpenCode / DeepSeek Harness).
4. Run CodeRabbit verification & syntax test.
5. If failure, inject error log and re-attempt.
6. If success, commit step and advance.
7. Repeat until 100% complete.
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from core.code_reviewer import code_reviewer
from core.design_blueprint import design_blueprint


class RalphFlowEngine:
    """Autonomous goal-completion loop that runs until all milestone tasks pass."""

    def __init__(self, task_file: Optional[str] = None):
        if task_file is None:
            task_file = os.path.join(os.path.dirname(__file__), "memory_vault", "ralph_tasks.json")
        self.task_file = task_file
        self.max_iterations = 25

    def init_task_queue(self, project_name: str, tasks: List[str]) -> Dict[str, Any]:
        """Initializes a new Ralph task queue from a feature specification."""
        task_data = {
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "status": "in_progress",
            "current_index": 0,
            "tasks": [{"id": idx, "description": t, "status": "pending", "attempts": 0, "logs": []} for idx, t in enumerate(tasks)]
        }
        os.makedirs(os.path.dirname(self.task_file), exist_ok=True)
        with open(self.task_file, "w", encoding="utf-8") as f:
            json.dump(task_data, f, indent=2)
        return task_data

    def load_queue(self) -> Optional[Dict[str, Any]]:
        """Loads active Ralph tasks."""
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Finds the next incomplete task."""
        data = self.load_queue()
        if not data:
            return None
        for task in data.get("tasks", []):
            if task["status"] in ["pending", "failed"]:
                return task
        return None

    def mark_task_success(self, task_id: int, commit_message: Optional[str] = None):
        """Marks a task complete and advances the loop."""
        data = self.load_queue()
        if not data:
            return
        for task in data.get("tasks", []):
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                if commit_message:
                    task["commit"] = commit_message
                break

        # Check if all completed
        all_done = all(t["status"] == "completed" for t in data.get("tasks", []))
        if all_done:
            data["status"] = "completed"
            data["finished_at"] = datetime.now().isoformat()

        with open(self.task_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def mark_task_failure(self, task_id: int, error_log: str):
        """Records failure and increments attempt counter."""
        data = self.load_queue()
        if not data:
            return
        for task in data.get("tasks", []):
            if task["id"] == task_id:
                task["attempts"] += 1
                task["logs"].append(f"Attempt {task['attempts']} Failed: {error_log[:200]}")
                if task["attempts"] >= 5:
                    task["status"] = "blocked"
                else:
                    task["status"] = "failed"
                break
        with open(self.task_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def run_spec_verification(self, project_dir: str, prd_content: str, generated_files: List[str]) -> Dict[str, Any]:
        """
        Autonomous Critic Gatekeeper (Ralph Review Loop):
        Audits generated codebase against the PRD requirements, AST syntax, and Stitch-UX completeness.
        Returns: { "passed": bool, "issues": List[str], "surgical_instruction": str }
        """
        issues = []
        if not generated_files:
            return {
                "passed": False,
                "issues": ["Zero output files were produced by the builder."],
                "surgical_instruction": "Generate the complete index.html with all Stitch-UX sections immediately."
            }

        html_files = [f for f in generated_files if f.endswith(".html")]
        py_files = [f for f in generated_files if f.endswith(".py")]

        # 1. Python CodeRabbit AST Audit
        for py_path in py_files:
            if os.path.exists(py_path):
                res = code_reviewer.audit_python_file(py_path)
                if not res.get("passed", True):
                    issues.extend(res.get("issues", []))

        # 2. HTML/DOM Stitch-UX Structural Completeness Audit
        for html_path in html_files:
            if not os.path.exists(html_path):
                issues.append(f"Missing HTML artifact: {os.path.basename(html_path)}")
                continue

            try:
                with open(html_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as read_err:
                issues.append(f"Cannot read {os.path.basename(html_path)}: {read_err}")
                continue

            if len(content.strip()) < 400:
                issues.append(f"{os.path.basename(html_path)} is truncated or nearly empty ({len(content)} bytes).")

            # AgentShield security scan on HTML/JS
            sec_res = code_reviewer.audit_text_file(html_path)
            if not sec_res.get("passed", True):
                issues.extend(sec_res.get("issues", []))

            # Check for lazy placeholder omissions
            lazy_markers = ["// TODO", "/* TODO", "<!-- TODO", "// implement rest", "/* rest of code */"]
            for marker in lazy_markers:
                if marker.lower() in content.lower():
                    issues.append(f"Lazy placeholder detected in {os.path.basename(html_path)}: '{marker}'")

            # Detect archetype from PRD header or content
            archetype = "utility_tool"
            prd_lower = prd_content.lower()
            if "archetype: utility_tool" in prd_lower or "archetype: utility" in prd_lower:
                archetype = "utility_tool"
            elif "archetype: commerce_store" in prd_lower or "archetype: store" in prd_lower:
                archetype = "commerce_store"
            elif "archetype: data_dashboard" in prd_lower or "archetype: dashboard" in prd_lower:
                archetype = "data_dashboard"
            elif "utility_tool" in prd_lower or "converter" in prd_lower or "calculator" in prd_lower or "timer" in prd_lower:
                archetype = "utility_tool"
            elif "commerce_store" in prd_lower:
                archetype = "commerce_store"
            else:
                archetype = design_blueprint.detect_archetype(prd_content)

            content_lower = content.lower()

            # Archetype-Specific Specification Checks
            if archetype == "utility_tool":
                # 1. Require ergonomic inputs & reactive calculation engine
                has_inputs = "<input" in content_lower or "<select" in content_lower or "textarea" in content_lower
                if not has_inputs:
                    issues.append("Missing interactive input controls (input/select) for utility tool.")
                
                has_logic = any(w in content_lower for w in ["addeventlistener", "oninput", "onchange", "onclick", "convert", "calculate", "swap", "math."])
                if not has_logic:
                    issues.append("Missing reactive calculation/conversion logic in JavaScript.")

                # 2. Strict Ponytail YAGNI Check — Reject unrequested e-commerce bloat on utility tools
                bloat_triggers = ["addtocart", "add to cart", "cart-drawer", "cartdrawer", "shopping cart", "proceed to checkout", "drone", "backpack", "order drawer"]
                detected_bloat = [b for b in bloat_triggers if b in content_lower]
                if detected_bloat:
                    issues.append(f"CRITICAL SCOPE CREEP: Unrequested e-commerce feature(s) detected in a utility tool ({', '.join(detected_bloat[:3])}). Remove all shopping carts, catalogs, and checkout modals.")

                # 3. Google Stitch & UI/UX Pro Zero-AI-Tropes Audit
                ai_tropes = []
                if ".bg-grid" in content_lower or "bg-[linear-gradient(to_right,#1f2937_1px" in content_lower or "background-image: linear-gradient(to right" in content_lower:
                    ai_tropes.append("Matrix grid background (.bg-grid)")
                if ".glow-a" in content_lower or ".glow-b" in content_lower or "animate-blob" in content_lower:
                    ai_tropes.append("Floating neon background blur spheres (.glow-a/.glow-b)")
                if "text-emerald-400" in content_lower and "font-mono" in content_lower and "text-3xl" in content_lower:
                    ai_tropes.append("Radioactive neon green numbers (must be crisp high-contrast pure white)")
                if ai_tropes:
                    issues.append(f"AI TROPES DETECTED: {', '.join(ai_tropes)}. Replace with Google Stitch / UI-UX Pro clean solid dark luxury canvas and high-contrast white typography.")

            elif archetype == "commerce_store":
                if "<nav" not in content_lower and "header" not in content_lower:
                    issues.append("Missing Navigation/Header section.")
                if "catalog" not in content_lower and "grid" not in content_lower and "menu" not in content_lower:
                    issues.append("Missing dynamic product/data catalog grid.")
                if "cart" not in content_lower and "order" not in content_lower and "drawer" not in content_lower:
                    issues.append("Missing interactive Order Bag / Cart drawer component.")

            elif archetype == "data_dashboard":
                if "metric" not in content_lower and "kpi" not in content_lower and "card" not in content_lower:
                    issues.append("Missing KPI metric cards.")
                if "table" not in content_lower and "chart" not in content_lower and "grid" not in content_lower:
                    issues.append("Missing telemetry chart or data table.")

            # Universal icon check
            if "lucide" in content_lower and "createicons" not in content_lower:
                issues.append("Lucide icons imported but `lucide.createIcons()` was never called.")

        # 3. Formulate Surgical Patch Prompt if issues detected
        if issues:
            surgical_instruction = (
                "CRITICAL SPECIFICATION DEFECTS DETECTED DURING RALPH AUDIT:\n"
                + "\n".join(f"- {iss}" for iss in issues[:5])
                + "\n\nMISSION: Surgically update and patch the existing files to resolve ONLY these issues. "
                "Ensure all missing components are fully implemented in complete, runnable code with zero placeholders."
            )
            return {
                "passed": False,
                "issues": issues,
                "surgical_instruction": surgical_instruction
            }

        return {
            "passed": True,
            "issues": [],
            "surgical_instruction": ""
        }


ralph_engine = RalphFlowEngine()

