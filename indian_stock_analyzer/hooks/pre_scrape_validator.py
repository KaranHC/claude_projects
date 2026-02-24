"""
PreToolUse hook: Validates URLs and commands before execution.

Checks that WebFetch requests target allowed domains and that
Bash commands don't use unauthorized network tools.
"""

import json
import logging
import os
from urllib.parse import urlparse

log = logging.getLogger("hooks.pre_scrape_validator")

# Load allowed domains from config
_config_path = os.path.join(os.path.dirname(__file__), "..", "config", "settings.json")
try:
    with open(_config_path) as f:
        _config = json.load(f)
    ALLOWED_DOMAINS = _config.get("allowed_domains", [])
except (FileNotFoundError, json.JSONDecodeError):
    ALLOWED_DOMAINS = ["www.tickertape.in", "api.stocktwits.com"]

BLOCKED_COMMANDS = ["curl", "wget", "nc", "ncat"]


async def pre_scrape_validator(tool_input: dict, tool_use_id: str, tool_name: str) -> dict:
    """
    Validate tool usage before execution.

    For WebFetch: checks URL domain against allowed list.
    For Bash: checks command doesn't use unauthorized network tools.

    Returns:
        dict with 'decision' key: 'allow', 'deny', or 'skip' (no opinion).
              Optional 'reason' key for deny decisions.
    """
    if tool_name == "WebFetch":
        url = tool_input.get("url", "")
        if not url:
            return {"decision": "deny", "reason": "WebFetch called without URL"}

        parsed = urlparse(url)
        domain = parsed.hostname or ""

        if domain in ALLOWED_DOMAINS:
            log.info(f"[ALLOW] WebFetch to allowed domain: {domain}")
            return {"decision": "allow"}
        else:
            log.warning(f"[DENY] WebFetch to unauthorized domain: {domain}")
            return {
                "decision": "deny",
                "reason": f"Domain '{domain}' not in allowed list: {ALLOWED_DOMAINS}",
            }

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        for blocked in BLOCKED_COMMANDS:
            if blocked in command.split():
                log.warning(f"[DENY] Bash command contains blocked tool: {blocked}")
                return {
                    "decision": "deny",
                    "reason": f"Command uses blocked network tool: {blocked}",
                }
        log.info(f"[ALLOW] Bash command: {command}")
        return {"decision": "allow"}

    # No opinion on other tools
    return {"decision": "skip"}
