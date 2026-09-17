"""
========================================================================================
F.R.I.D.A.Y. OS 10.0: AgentShield Security Audit Engine (ECC Enterprise Standard)
Pre-commit & Post-generation code defense and automated compliance scanner.
Maps to MITRE ATT&CK and NIST CSF 2.0 security controls:
1. Multi-Vendor Secret & Credential Leak Detection (AWS, OpenAI, Anthropic, Stripe, etc.)
2. Hazardous AST Dynamic Executions (eval, exec, pickle, shell injections)
3. Dangerous Filesystem Destructions & Path Traversal Guards
4. Ponytail YAGNI & Code Bloat Auditing
========================================================================================
"""

import os
import re
import ast
import subprocess
from typing import Dict, Any, List, Optional, Tuple


class AgentShieldAuditor:
    """Enterprise-grade code security, secret detection, and architectural compliance auditor."""

    # 1. Comprehensive Multi-Vendor Credential Signatures (AgentShield Core)
    SECRET_CATALOG: List[Tuple[str, str]] = [
        # Cloud Providers & AI Model Keys
        (r"sk-[A-Za-z0-9]{32,}", "Exposed OpenAI / DeepSeek API Key"),
        (r"sk-proj-[A-Za-z0-9_\-]{40,}", "Exposed OpenAI Project Key"),
        (r"sk-ant-api[0-9]{2}-[A-Za-z0-9_\-]{80,}", "Exposed Anthropic Claude API Key"),
        (r"AIza[0-9A-Za-z_\-]{35}", "Exposed Google Gemini / Cloud API Key"),
        (r"gsk_[A-Za-z0-9]{48,}", "Exposed Groq Cloud LPU API Key"),
        (r"hf_[A-Za-z0-9]{34,}", "Exposed HuggingFace User Access Token"),
        (r"AKIA[0-9A-Z]{16}", "Exposed AWS Access Key ID"),
        
        # Payment & Financial Gateways
        (r"(?:sk|rk)_live_[0-9a-zA-Z]{24,}", "CRITICAL: Live Production Stripe API Secret Key"),
        (r"sq0atp-[0-9A-Za-z\-_]{22}", "Exposed Square Access Token"),
        
        # VCS & Platform Tokens
        (r"ghp_[A-Za-z0-9]{36}", "Exposed GitHub Personal Access Token"),
        (r"github_pat_[A-Za-z0-9_]{82}", "Exposed Fine-Grained GitHub PAT"),
        (r"gho_[A-Za-z0-9]{36}", "Exposed GitHub OAuth Token"),
        (r"xox[baprs]-[0-9A-Za-z]{10,}", "Exposed Slack Workspace Bot/User Token"),
        (r"glpat-[0-9a-zA-Z\-_]{20}", "Exposed GitLab Personal Access Token"),
        
        # Cryptographic Private Keys
        (r"-----BEGIN (?:RSA|DSA|EC|OPENSSH|PGP|PRIVATE) KEY-----", "CRITICAL: Exposed Private Cryptographic Key"),
        
        # Database Connection Strings with Credentials
        (r"(?:postgres|postgresql|mysql|mongodb(?:\+srv)?|redis):\/\/[^:\s]+:[^@\s]+@[^\s]+", "Hardcoded Database Connection String with Credentials"),
        
        # Generic Secret Assignments with High Entropy
        (r"(?i)(?:api[_-]?key|secret|password|access[_-]?token|auth[_-]?token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High-Entropy Hardcoded Credential Assignment"),
    ]

    # Safe placeholder markers to prevent false positives in tests and examples
    SAFE_PLACEHOLDERS = [
        "your_", "example", "placeholder", "os.environ", "env.", "process.env",
        "dummy", "test_key", "xxx", "00000", "my_secret", "changeme", "sk-...",
        "akiaiosfodnn7example"
    ]

    def __init__(self, repo_dir: Optional[str] = None):
        if repo_dir is None:
            repo_dir = os.path.dirname(os.path.dirname(__file__))
        self.repo_dir = repo_dir

    def is_safe_placeholder(self, matched_text: str) -> bool:
        """Determines if a matched pattern is an intentional documentation placeholder."""
        lower_val = matched_text.lower()
        return any(placeholder in lower_val for placeholder in self.SAFE_PLACEHOLDERS)

    def scan_secrets(self, text: str) -> List[str]:
        """Scans code or text content for hardcoded secrets, tokens, and credentials."""
        issues = []
        for pat, desc in self.SECRET_CATALOG:
            for m in re.finditer(pat, text):
                matched_val = m.group(0)
                if not self.is_safe_placeholder(matched_val):
                    snippet = matched_val[:12] + "..." + matched_val[-4:] if len(matched_val) > 18 else matched_val
                    issues.append(f"SECURITY HAZARD: {desc} detected ('{snippet}')")
        return issues

    def audit_python_file(self, filepath: str) -> Dict[str, Any]:
        """Audits a Python file for AST syntax, execution hazards, and credential leaks."""
        issues: List[str] = []
        if not os.path.exists(filepath):
            return {"passed": False, "issues": [f"File does not exist: {filepath}"]}

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                code = f.read()
        except Exception as e:
            return {"passed": False, "issues": [f"Could not read file: {e}"]}

        # 1. AST Syntax Validation
        try:
            tree = ast.parse(code, filename=filepath)
        except SyntaxError as se:
            return {
                "passed": False,
                "issues": [f"SYNTAX ERROR [Line {se.lineno}]: {se.msg}"]
            }

        # 2. Secret & Credential Scanning
        issues.extend(self.scan_secrets(code))

        # 3. AST-Level Hazardous Code Execution Detection
        for node in ast.walk(tree):
            # Flag dangerous dynamic evaluation: eval(), exec()
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in ["eval", "exec"]:
                    issues.append(f"EXECUTION HAZARD [Line {node.lineno}]: Dangerous use of `{func_name}()` dynamic code execution.")
                elif func_name in ["loads"] and hasattr(node.func, "value") and getattr(node.func.value, "id", "") in ["pickle", "marshal"]:
                    issues.append(f"DESERIALIZATION HAZARD [Line {node.lineno}]: Insecure `{getattr(node.func.value, 'id')}.loads()` can execute arbitrary code.")

            # Flag Ponytail YAGNI bloat (functions over 300 lines)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                length = (node.end_lineno or 0) - node.lineno
                if length > 300:
                    issues.append(f"PONYTAIL WARNING: Function `{node.name}` is {length} lines long. Consider breaking it down or using standard libraries.")

        # 4. Dangerous Shell Command Injections
        shell_patterns = [
            (r"(?i)subprocess\.(?:Popen|run|call)\(\s*f?['\"].*?(?:rmdir|del|format|mkfs|rm\s+-rf).*?['\"].*?shell\s*=\s*True\)", "Dangerous shell=True execution with system destruction command"),
            (r"(?i)os\.system\(\s*f?['\"].*?(?:rmdir|del|format|rm\s+-rf).*?['\"]\)", "Unsanitized destructive os.system invocation"),
            (r"(?i)subprocess\.(?:Popen|run|call)\([^)]*shell\s*=\s*True[^)]*(?:f['\"]|format\(|%s)", "CRITICAL: Unsanitized dynamic shell=True string interpolation (Command Injection Risk)")
        ]
        for pat, desc in shell_patterns:
            if re.search(pat, code):
                issues.append(f"INJECTION HAZARD: {desc}")

        # 5. Path Traversal Hazard
        if re.search(r"(\.\.[/\\]){3,}", code):
            issues.append("PATH TRAVERSAL HAZARD: Excessive parent directory traversal ('../../..') detected.")

        passed = len([i for i in issues if not i.startswith("PONYTAIL")]) == 0
        return {
            "passed": passed,
            "filepath": filepath,
            "issues": issues,
            "summary": "APPROVED" if passed else f"BLOCKED: {len(issues)} issue(s) detected"
        }

    def audit_text_file(self, filepath: str) -> Dict[str, Any]:
        """Audits non-python source files (.html, .js, .json, .env, .md) for credential leaks."""
        if not os.path.exists(filepath):
            return {"passed": False, "issues": [f"File does not exist: {filepath}"]}

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            return {"passed": False, "issues": [f"Could not read file: {e}"]}

        issues = self.scan_secrets(content)
        passed = len(issues) == 0
        return {
            "passed": passed,
            "filepath": filepath,
            "issues": issues,
            "summary": "APPROVED" if passed else f"BLOCKED: {len(issues)} issue(s) detected"
        }

    def audit_file(self, filepath: str) -> Dict[str, Any]:
        """Polymorphic file audit dispatcher."""
        if filepath.endswith(".py"):
            return self.audit_python_file(filepath)
        return self.audit_text_file(filepath)

    def audit_git_diff(self) -> Dict[str, Any]:
        """Audits all modified files in the working directory before commit."""
        try:
            res = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            files = [f.strip() for f in res.stdout.strip().split("\n") if f.strip()]
        except Exception:
            files = []

        all_results = []
        overall_passed = True
        for rel_path in files:
            full_path = os.path.join(self.repo_dir, rel_path)
            res = self.audit_file(full_path)
            all_results.append(res)
            if not res["passed"]:
                overall_passed = False

        return {
            "overall_passed": overall_passed,
            "audited_files": len(files),
            "results": all_results
        }


# Compatibility alias for existing codebase integrations
CodeRabbitReviewer = AgentShieldAuditor
code_reviewer = AgentShieldAuditor()
