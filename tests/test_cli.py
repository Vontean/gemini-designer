from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "gemini-designer"


class GeminiDesignerCliTest(unittest.TestCase):
    def run_cli(self, *extra_args: str) -> tuple[subprocess.CompletedProcess[str], list[str]]:
        with tempfile.TemporaryDirectory() as temporary_dir:
            temp = Path(temporary_dir)
            fake_agy = temp / "agy"
            captured_args = temp / "agy-args.json"
            fake_agy.write_text(
                """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

Path(os.environ[\"AGY_ARGS_PATH\"]).write_text(json.dumps(sys.argv[1:]))
print(json.dumps({
    \"event\": \"init\",
    \"conversation_id\": \"new-conversation-id\",
    \"init\": {\"model\": \"fake-model\"},
}))
print(json.dumps({
    \"event\": \"step_update\",
    \"step_update\": {
        \"step_type\": \"tool\",
        \"tool_info\": {\"name\": \"view_file\", \"parameters\": {}},
    },
}))
print(json.dumps({
    \"event\": \"step_update\",
    \"step_update\": {
        \"step_type\": \"agent_response\",
        \"text_delta\": \"# Design review\\n\",
    },
}))
print(json.dumps({
    \"event\": \"result\",
    \"result\": {
        \"status\": \"SUCCESS\",
        \"response\": \"# Design review\\n\",
        \"conversation_id\": \"new-conversation-id\",
    },
}))
"""
            )
            fake_agy.chmod(fake_agy.stat().st_mode | stat.S_IXUSR)
            env = os.environ.copy()
            env["PATH"] = f"{temp}:{env['PATH']}"
            env["AGY_ARGS_PATH"] = str(captured_args)
            env["GEMINI_DESIGNER_CONFIG_DIR"] = str(temp / "config")
            result = subprocess.run(
                [str(CLI), "ui", "Review this page", "-o", "review.md", *extra_args],
                cwd=temp,
                env=env,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return result, json.loads(captured_args.read_text())

    def test_default_runtime_is_long_running_editable_and_sandboxed(self) -> None:
        result, agy_args = self.run_cli()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("conversation_id=new-conversation-id", result.stdout)
        self.assertIn("[agy] started conversation=new-conversation-id", result.stderr)
        self.assertIn("[agy] tool: view_file", result.stderr)
        self.assertIn("# Design review", result.stderr)
        self.assertIn("[agy] completed", result.stderr)
        self.assertEqual(agy_args[agy_args.index("--print-timeout") + 1], "30m")
        self.assertEqual(agy_args[agy_args.index("--mode") + 1], "accept-edits")
        self.assertIn("--sandbox", agy_args)
        self.assertNotIn("--dangerously-skip-permissions", agy_args)
        self.assertIn("--add-dir", agy_args)
        self.assertEqual(agy_args[agy_args.index("--output-format") + 1], "stream-json")

    def test_exact_conversation_is_resumed(self) -> None:
        result, agy_args = self.run_cli("--conversation", "prior-conversation-id")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            agy_args[agy_args.index("--conversation") + 1],
            "prior-conversation-id",
        )

    def test_one_conversation_cannot_feed_parallel_reviews(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            result = subprocess.run(
                [
                    str(CLI),
                    "ui,ux",
                    "Review this page",
                    "-o",
                    "review.md",
                    "--conversation",
                    "prior-conversation-id",
                ],
                cwd=temporary_dir,
                env={
                    **os.environ,
                    "GEMINI_DESIGNER_CONFIG_DIR": str(Path(temporary_dir) / "config"),
                },
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("error=invalid_args", result.stderr)


if __name__ == "__main__":
    unittest.main()
