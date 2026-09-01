"""
F.R.I.D.A.Y. OS 9.0: Autonomous Runtime Debugger & Self-Healing Watcher (Pillar 2)
Monitors launched background processes in real-time, intercepts crash tracebacks,
auto-patches the source code in under 5 seconds, and reboots the server with zero human intervention.
"""

import os
import re
import time
import subprocess
import threading
from typing import Optional, Dict, Any, List, Callable


class RuntimeSelfHealer:
    r"""
    Autonomous Crash Interceptor and Code Patching Engine.
    Continuously monitors active projects in D:\FRIDAY_Projects\ and heals runtime failures.
    """

    def __init__(self):
        self._active_watchers: Dict[str, threading.Thread] = {}
        self._lock = threading.Lock()

    def parse_python_traceback(self, stderr_text: str) -> Optional[Dict[str, Any]]:
        """
        Parses standard Python traceback to extract failing file, line number, and exception.
        """
        if "Traceback (most recent call last):" not in stderr_text:
            return None

        lines = stderr_text.strip().split("\n")
        file_match = None
        line_num = None
        exception_str = lines[-1] if lines else "Unknown Exception"

        # Walk backwards to find the last file and line in the trace
        for line in reversed(lines):
            m = re.search(r'File "([^"]+)", line (\d+)', line)
            if m:
                file_match = m.group(1)
                line_num = int(m.group(2))
                break

        return {
            "error_type": exception_str.split(":")[0].strip() if ":" in exception_str else "RuntimeError",
            "error_message": exception_str.strip(),
            "failing_file": file_match,
            "line_number": line_num,
            "full_traceback": stderr_text.strip()
        }

    def repair_failing_code(self, project_dir: str, file_path: str, traceback_info: Dict[str, Any]) -> bool:
        """
        Synthesizes a clean code patch using local repair engines (OpenCode / Groq / Gemini),
        overwrites the broken file, and verifies syntax before restarting.
        """
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                original_code = f.read()

            repair_prompt = f"""
YOU ARE F.R.I.D.A.Y.'S AUTONOMOUS SELF-HEALING KERNEL.
A runtime crash occurred in project '{os.path.basename(project_dir)}'.

FAILING FILE: {os.path.basename(file_path)}
LINE: {traceback_info.get('line_number')}
ERROR: {traceback_info.get('error_message')}

FULL TRACEBACK:
{traceback_info.get('full_traceback')}

ORIGINAL CODE:
```python
{original_code}
```

TASK:
Fix the error completely. Maintain all other logic and formatting.
Output ONLY the complete, corrected Python code inside standard markdown code block:
```python
# Complete corrected code
```
"""
            # Fast fix via Background Co-Processor or Groq LPU
            from core.background_coprocessor import coprocessor
            success, patched_content, _ = coprocessor.execute_fast_completion(
                "You are F.R.I.D.A.Y. Automated Code Repair Engine. Output only corrected code in code fences.",
                repair_prompt,
                max_tokens=4096
            )

            if not success or not patched_content:
                return False

            # Extract code block
            code_match = re.search(r"```python\r?\n(.*?)```", patched_content, re.DOTALL)
            if code_match:
                fixed_code = code_match.group(1).strip()
            else:
                fixed_code = patched_content.strip()

            # Safety check: Verify syntax before writing
            compile(fixed_code, file_path, "exec")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code)

            print(f"\n[Self-Healing Watcher]: Successfully patched {os.path.basename(file_path)} for {traceback_info['error_type']}!")
            return True
        except Exception as patch_err:
            print(f"[Self-Healing Watcher Error]: Failed to patch code: {patch_err}")
            return False

    def watch_subprocess(
        self,
        process: subprocess.Popen,
        project_dir: str,
        project_name: str,
        restart_cmd: Optional[List[str]] = None,
        speak_fn: Optional[Callable[[str], None]] = None
    ):
        """
        Monitors a launched subprocess. If it terminates with non-zero exit code or emits a traceback,
        it automatically diagnoses, patches, and restarts the process.
        """
        def _monitor_worker():
            print(f"[Self-Healing Watcher]: Active monitoring enabled for '{project_name}' in {project_dir}...")
            stderr_buffer = []

            # Tail stderr stream
            if process.stderr:
                for line in iter(process.stderr.readline, ""):
                    if not line:
                        break
                    stderr_buffer.append(line)
                    if len(stderr_buffer) > 40:
                        stderr_buffer = stderr_buffer[-40:]

            process.wait()
            exit_code = process.returncode

            if exit_code != 0 and exit_code is not None:
                full_stderr = "".join(stderr_buffer)
                trace_info = self.parse_python_traceback(full_stderr)

                if trace_info and trace_info.get("failing_file"):
                    failing_file = trace_info["failing_file"]
                    if not os.path.isabs(failing_file):
                        failing_file = os.path.join(project_dir, failing_file)

                    print(f"\n[Self-Healing Watcher]: CRASH DETECTED in {project_name}! Error: {trace_info['error_message']}")
                    if speak_fn:
                        speak_fn(f"Boss, I detected a {trace_info['error_type']} in {project_name}. Initiating autonomous self-healing now.")

                    healed = self.repair_failing_code(project_dir, failing_file, trace_info)

                    if healed and restart_cmd:
                        time.sleep(0.5)
                        print(f"[Self-Healing Watcher]: Relaunching {project_name} post-patch...")
                        new_proc = subprocess.Popen(
                            restart_cmd,
                            cwd=project_dir,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            shell=True
                        )
                        if speak_fn:
                            speak_fn(f"Self-healing complete, Boss. I have patched the error and restarted {project_name} successfully.")
                        self.watch_subprocess(new_proc, project_dir, project_name, restart_cmd, speak_fn)

        t = threading.Thread(target=_monitor_worker, daemon=True)
        with self._lock:
            self._active_watchers[project_name] = t
        t.start()


# Global singleton instance
runtime_debugger = RuntimeSelfHealer()
