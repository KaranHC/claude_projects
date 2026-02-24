"""
Indian Stock Analyzer using Claude Agent SDK

Takes an Indian company name, scrapes data from Tickertape and StockTwits,
runs specialized sub-agents for sentiment/technical/fundamental analysis,
and produces buy/sell/hold recommendations.

Usage:
    python main.py "Company Name"
    python main.py "Company Name" --resume <session_id>
"""

import asyncio
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    UserMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
)

from hooks.pre_scrape_validator import pre_scrape_validator
from hooks.post_analysis_logger import post_analysis_logger, get_write_log, clear_write_log

# Configure console logging (file handler added in IndianStockAnalyzer.__init__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("indian_stock_analyzer")


def _add_file_handler(logs_dir: str, slug: str) -> None:
    """Add a file handler to the root logger so all loggers write to logs/."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"{slug}_{timestamp}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    )
    logging.getLogger().addHandler(file_handler)
    log.info(f"Logging to file: {log_file}")


def slugify(name: str) -> str:
    """Convert a company name to a filename-safe slug."""
    return re.sub(r"[^\w\-]", "-", name.strip().lower()).strip("-")


def load_config() -> dict:
    """Load configuration from config/settings.json."""
    config_path = os.path.join(os.path.dirname(__file__), "config", "settings.json")
    with open(config_path) as f:
        return json.load(f)


def load_agent_prompt(agent_file: str, replacements: dict) -> str:
    """Load an agent prompt from markdown file and apply placeholder replacements."""
    agents_dir = os.path.join(os.path.dirname(__file__), "agents")
    filepath = os.path.join(agents_dir, agent_file)
    with open(filepath) as f:
        prompt = f.read()
    for key, value in replacements.items():
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt


def save_session(slug: str, session_id: str, company_name: str) -> str:
    """Save session info for later resume."""
    sessions_dir = os.path.join(os.path.dirname(__file__), "sessions")
    os.makedirs(sessions_dir, exist_ok=True)
    session_file = os.path.join(sessions_dir, f"{slug}_session.json")
    session_data = {
        "session_id": session_id,
        "company_name": company_name,
        "company_slug": slug,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(session_file, "w") as f:
        json.dump(session_data, f, indent=2)
    log.info(f"Session saved to {session_file}")
    return session_file


def load_session(session_id: str) -> dict | None:
    """Try to find a saved session by ID."""
    sessions_dir = os.path.join(os.path.dirname(__file__), "sessions")
    if not os.path.exists(sessions_dir):
        return None
    for filename in os.listdir(sessions_dir):
        if filename.endswith("_session.json"):
            filepath = os.path.join(sessions_dir, filename)
            with open(filepath) as f:
                data = json.load(f)
            if data.get("session_id") == session_id:
                return data
    return None


def build_system_prompt(company: str, slug: str, data_dir: str) -> str:
    """Build the orchestrator system prompt that dispatches 3 merged sub-agents."""
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")

    return f"""You are an Indian Stock Analyzer orchestrator. Your job is to perform a comprehensive, institutional-grade analysis of {company} by dispatching 3 specialized sub-agents sequentially using the Task tool.

IMPORTANT: Do NOT read agent prompt files yourself. The full agent prompts are provided below in the AGENT PROMPT TEMPLATES section. Use them directly when dispatching sub-agents via the Task tool.

WORKFLOW — Execute these 4 steps IN ORDER:

## Step 1: Data Collection (data-collector) — use model=haiku
Use the Task tool to dispatch the data-collector agent.
This agent scrapes Tickertape, StockTwits, fetches Screener.in financials, and gathers recent news — all in one session.
Pass the full data-collector prompt from AGENT PROMPT TEMPLATES below.
Outputs: {data_dir}/{slug}_tickertape.json, {data_dir}/{slug}_stocktwits.json, {data_dir}/{slug}_financials.json, {data_dir}/{slug}_news.json

## Step 2: Analysis (analyzer) — use model=haiku
Use the Task tool to dispatch the analyzer agent.
This agent performs sentiment analysis, technical analysis, and peer comparison in one session.
Pass the full analyzer prompt from AGENT PROMPT TEMPLATES below.
Outputs: {data_dir}/{slug}_sentiment.json, {data_dir}/{slug}_technical.json, {data_dir}/{slug}_peers.json

## Step 3: Recommendation & Risk (recommender) — use model=sonnet
Use the Task tool to dispatch the recommender agent.
This agent synthesizes all data into a BUY/SELL/HOLD recommendation with risk assessment, position sizing, and scenario analysis.
Pass the full recommender prompt from AGENT PROMPT TEMPLATES below.
Outputs: {data_dir}/{slug}_recommendation.json, {data_dir}/{slug}_risk.json

## Step 4: Final Report
Run this Bash command directly (do NOT use Task):
python {scripts_dir}/format_report.py {slug} {data_dir}
Present the formatted report output to the user.

IMPORTANT RULES:
- Execute steps sequentially — each step depends on the previous step's output
- All data files are saved to: {data_dir}/
- If a sub-agent fails, log the error and continue with available data
- Do NOT skip any steps — proceed through all 4 steps
- Do NOT read agent files from disk — use the prompts embedded below
- Use absolute paths for all file operations
- The working directory is: {os.getcwd()}"""


class IndianStockAnalyzer:
    """Main orchestrator for Indian stock analysis."""

    def __init__(self, company_name: str, resume_session_id: str | None = None):
        self.company_name = company_name
        self.slug = slugify(company_name)
        self.config = load_config()
        self.resume_session_id = resume_session_id

        # Set up directories
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, self.config["directories"]["data"])
        self.logs_dir = os.path.join(base_dir, self.config["directories"]["logs"])
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Enable file logging
        _add_file_handler(self.logs_dir, self.slug)

        # Clear hook state
        clear_write_log()

    async def run_hook_pre(self, tool_name: str, tool_input: dict, tool_use_id: str) -> dict:
        """Run pre-tool-use hooks."""
        return await pre_scrape_validator(tool_input, tool_use_id, tool_name)

    async def run_hook_post(self, tool_name: str, tool_input: dict, tool_use_id: str) -> dict:
        """Run post-tool-use hooks."""
        return await post_analysis_logger(tool_input, tool_use_id, tool_name)

    async def analyze_stock(self) -> None:
        """Run the complete stock analysis pipeline."""
        print(f"\n{'=' * 60}")
        print(f"  INDIAN STOCK ANALYZER")
        print(f"  Analyzing: {self.company_name}")
        print(f"  Data directory: {self.data_dir}")
        if self.resume_session_id:
            print(f"  Resuming session: {self.resume_session_id}")
        print(f"{'=' * 60}\n")

        # Build prompt
        prompt = (
            f'Analyze the Indian stock "{self.company_name}" following the workflow '
            f"in your system prompt. Execute all 4 steps sequentially to produce "
            f"a comprehensive analysis with a BUY/SELL/HOLD recommendation."
        )

        # Build system prompt
        system_prompt = build_system_prompt(
            self.company_name, self.slug, self.data_dir
        )

        # Load agent prompt templates (for reference in system prompt)
        replacements = {
            "company": self.company_name,
            "company_slug": self.slug,
            "data_dir": self.data_dir,
        }

        agent_prompts = {}
        agent_files = [
            "data-collector.md",
            "analyzer.md",
            "recommender.md",
        ]
        for agent_file in agent_files:
            try:
                agent_prompts[agent_file] = load_agent_prompt(agent_file, replacements)
            except FileNotFoundError:
                log.warning(f"Agent prompt not found: {agent_file}")

        # Append agent prompts to system prompt
        system_prompt += "\n\n## AGENT PROMPT TEMPLATES\n"
        for name, content in agent_prompts.items():
            system_prompt += f"\n### {name}\n{content}\n"

        # Configure options
        agent_config = self.config.get("agent", {})
        options = ClaudeAgentOptions(
            max_turns=agent_config.get("max_turns", 30),
            cwd=os.getcwd(),
            model=agent_config.get("model", "sonnet"),
            allowed_tools=[
                "Skill", "WebSearch", "WebFetch", "Bash",
                "Write", "Read", "Glob", "Task",
            ],
            setting_sources=["project"],
            system_prompt=system_prompt,
            permission_mode=agent_config.get("permission_mode", "acceptEdits"),
        )

        # Add resume if specified
        if self.resume_session_id:
            options.resume = self.resume_session_id

        # Tracking state
        tools_used: list[str] = []
        agents_dispatched: list[str] = []
        session_id = None

        log.info("Starting stock analysis pipeline")

        try:
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text)

                        elif isinstance(block, ToolUseBlock):
                            tools_used.append(block.name)

                            # Run pre-hook
                            if block.name in ("WebFetch", "Bash"):
                                tool_input = block.input if isinstance(block.input, dict) else {}
                                hook_result = await self.run_hook_pre(
                                    block.name, tool_input, block.id if hasattr(block, 'id') else ""
                                )
                                if hook_result.get("decision") == "deny":
                                    log.warning(f"[HOOK DENY] {block.name}: {hook_result.get('reason')}")
                                    print(f"\n[HOOK] Denied {block.name}: {hook_result.get('reason')}")

                            # Log tool usage
                            if block.name == "Task":
                                desc = ""
                                if isinstance(block.input, dict):
                                    desc = block.input.get("description", "")
                                agents_dispatched.append(desc)
                                log.info(f"Sub-agent dispatched: {desc}")
                                print(f"\n>> Sub-agent: {desc}")

                            elif block.name == "Skill":
                                skill_name = ""
                                if isinstance(block.input, dict):
                                    skill_name = block.input.get("skill", "")
                                log.info(f"Skill triggered: {skill_name}")
                                print(f"\n>> Skill: {skill_name}")

                            elif block.name == "WebSearch":
                                search_query = ""
                                if isinstance(block.input, dict):
                                    search_query = block.input.get("query", "")
                                log.info(f"WebSearch: {search_query}")
                                print(f"\n>> Search: \"{search_query}\"")

                            elif block.name == "WebFetch":
                                url = ""
                                if isinstance(block.input, dict):
                                    url = block.input.get("url", "")
                                log.info(f"WebFetch: {url}")
                                print(f"\n>> Fetch: {url[:80]}")

                            elif block.name == "Write":
                                file_path = ""
                                if isinstance(block.input, dict):
                                    file_path = block.input.get("file_path", "")
                                log.info(f"Write: {file_path}")
                                print(f"\n>> Write: {file_path}")

                                # Run post-hook
                                tool_input = block.input if isinstance(block.input, dict) else {}
                                await self.run_hook_post(
                                    block.name, tool_input, block.id if hasattr(block, 'id') else ""
                                )

                            elif block.name == "Read":
                                file_path = ""
                                if isinstance(block.input, dict):
                                    file_path = block.input.get("file_path", "")
                                log.info(f"Read: {file_path}")
                                print(f"\n>> Read: {os.path.basename(file_path)}")

                            elif block.name == "Bash":
                                command = ""
                                if isinstance(block.input, dict):
                                    command = str(block.input.get("command", ""))
                                log.info(f"Bash: {command}")
                                print(f"\n>> Run: {command}")

                            else:
                                log.info(f"Tool: {block.name}")
                                print(f"\n>> Tool: {block.name}")

                elif isinstance(message, UserMessage):
                    if isinstance(message.content, list):
                        for block in message.content:
                            if isinstance(block, ToolResultBlock):
                                result_str = str(block.content)[:200]
                                print(f"   Result: {result_str}{'...' if len(str(block.content)) >= 200 else ''}")

                elif isinstance(message, ResultMessage):
                    # Capture session ID for resume
                    if hasattr(message, 'session_id') and message.session_id:
                        session_id = message.session_id

                    print(f"\n{'=' * 60}")
                    print(f"Session completed in {message.duration_ms}ms | Turns: {message.num_turns}")

                    if hasattr(message, 'total_cost_usd') and message.total_cost_usd is not None:
                        print(f"Total cost: ${message.total_cost_usd:.4f}")

                    # Check for errors
                    if hasattr(message, 'is_error') and message.is_error:
                        log.error("Session ended with error")
                        print("[ERROR] Session ended with an error. Check logs for details.")

        except KeyboardInterrupt:
            log.info("Analysis interrupted by user")
            print("\n\n[INTERRUPTED] Analysis stopped by user.")
        except Exception as e:
            log.error(f"Analysis failed: {e}")
            print(f"\n[ERROR] Analysis failed: {e}")
            raise

        # Save session for resume
        if session_id:
            session_file = save_session(self.slug, session_id, self.company_name)
            print(f"\nSession saved. Resume with:")
            print(f"  python main.py \"{self.company_name}\" --resume {session_id}")

        # Print summary
        print(f"\n{'=' * 60}")
        print("ANALYSIS SUMMARY")
        print(f"{'=' * 60}")
        print(f"  Company:            {self.company_name}")
        print(f"  Slug:               {self.slug}")
        print(f"  Tools used:         {', '.join(dict.fromkeys(tools_used)) if tools_used else 'None'}")
        print(f"  Sub-agents run:     {len(agents_dispatched)}")
        for i, agent in enumerate(agents_dispatched, 1):
            print(f"    {i}. {agent}")
        print(f"  Files written:      {len(get_write_log())}")
        for entry in get_write_log():
            print(f"    - {entry['file']}")
        print(f"  Data directory:     {self.data_dir}")

        # Check for output files
        expected_files = [
            f"{self.slug}_tickertape.json",
            f"{self.slug}_stocktwits.json",
            f"{self.slug}_financials.json",
            f"{self.slug}_news.json",
            f"{self.slug}_peers.json",
            f"{self.slug}_sentiment.json",
            f"{self.slug}_technical.json",
            f"{self.slug}_recommendation.json",
            f"{self.slug}_risk.json",
        ]
        print(f"\n  Output files:")
        for fname in expected_files:
            fpath = os.path.join(self.data_dir, fname)
            if os.path.exists(fpath):
                size_kb = os.path.getsize(fpath) / 1024
                print(f"    [OK] {fname} ({size_kb:.1f} KB)")
            else:
                print(f"    [--] {fname} (not created)")

        print(f"{'=' * 60}\n")


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "Company Name"')
        print('       python main.py "Company Name" --resume <session_id>')
        print()
        print('Examples:')
        print('  python main.py "Tata Consultancy Services"')
        print('  python main.py "Mahindra and Mahindra Ltd"')
        print('  python main.py "Infosys Ltd" --resume abc123')
        sys.exit(1)

    company_name = sys.argv[1]
    resume_session_id = None

    if "--resume" in sys.argv:
        resume_idx = sys.argv.index("--resume")
        if resume_idx + 1 < len(sys.argv):
            resume_session_id = sys.argv[resume_idx + 1]
        else:
            print("ERROR: --resume requires a session ID argument", file=sys.stderr)
            sys.exit(1)

    analyzer = IndianStockAnalyzer(company_name, resume_session_id)
    asyncio.run(analyzer.analyze_stock())


if __name__ == "__main__":
    main()
