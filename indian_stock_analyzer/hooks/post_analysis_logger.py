"""
PostToolUse hook: Logs file writes and data operations.

Tracks when analysis files are written to the data directory
and provides additional context messages.
"""

import logging
import os
from datetime import datetime, timezone

log = logging.getLogger("hooks.post_analysis_logger")

# Track all writes for session summary
write_log: list[dict] = []


async def post_analysis_logger(tool_input: dict, tool_use_id: str, tool_name: str) -> dict:
    """
    Log tool usage after execution.

    For Write operations to data/*.json: logs the operation and returns
    additional context for the agent.

    Returns:
        dict with optional 'additionalContext' key containing a message
        to feed back to the agent.
    """
    if tool_name == "Write":
        file_path = tool_input.get("file_path", "")

        if "/data/" in file_path and file_path.endswith(".json"):
            filename = os.path.basename(file_path)
            timestamp = datetime.now(timezone.utc).isoformat()

            entry = {
                "file": filename,
                "path": file_path,
                "timestamp": timestamp,
                "tool_use_id": tool_use_id,
            }
            write_log.append(entry)

            log.info(f"[LOG] Data file written: {filename} at {timestamp}")

            return {
                "additionalContext": (
                    f"Successfully saved {filename}. "
                    f"Total analysis files written this session: {len(write_log)}."
                ),
            }

    return {}


def get_write_log() -> list[dict]:
    """Return the list of all logged write operations."""
    return list(write_log)


def clear_write_log() -> None:
    """Clear the write log (e.g., between sessions)."""
    write_log.clear()
