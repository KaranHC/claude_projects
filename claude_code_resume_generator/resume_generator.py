"""
Resume Generator using Claude Agent SDK

This example uses web search to research a person and generates
a professional 1-page resume as a .docx file.

Usage: python resume_generator.py "Person Name"
"""

import asyncio
import logging
import os
import re
import sys

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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("resume_generator")


def slugify(name: str) -> str:
    """Convert a person's name to a filename-safe slug."""
    return re.sub(r"[^\w\-]", "-", name.strip().lower()).strip("-")


def build_system_prompt(output_dir: str, filename: str) -> str:
    return f"""You are a professional resume writer. Research a person and create a 1-page .docx resume.

WORKFLOW:
1. FIRST, use the Skill tool to load the "docx" skill. This is MANDATORY.
2. After the skill is loaded, READ the docx-js.md file completely — it contains critical formatting rules.
3. WebSearch for the person's background (LinkedIn, GitHub, company pages).
4. Create a .docx file using the docx JS library following the patterns from docx-js.md.

OUTPUT:
- Script: {output_dir}/generate_resume.js
- Resume: {output_dir}/{filename}

IMPORTANT:
- You MUST use the Skill tool for "docx" before generating any .docx file.
- You MUST read the full docx-js.md skill file before writing any docx code.
- Save all output files to the exact paths above (use absolute paths).

PAGE FIT (must be exactly 1 page):
- 0.5 inch margins, Name 24pt, Headers 12pt, Body 10pt
- 2-3 bullet points per job, ~80-100 chars each
- Max 3 job roles, 2-line summary, 2-line skills"""


async def generate_resume(person_name: str) -> None:
    slug = slugify(person_name)
    filename = f"{slug}.docx"
    output_dir = os.path.join(os.getcwd(), "output", "resumes")
    os.makedirs(output_dir, exist_ok=True)
    expected_path = os.path.join(output_dir, filename)

    print(f"\n📝 Generating resume for: {person_name}")
    print(f"📂 Output: {expected_path}\n")
    print("=" * 50)

    prompt = (
        f'Research "{person_name}" and create a professional 1-page resume '
        f"as a .docx file. Search for their professional background, "
        f"experience, education, and skills. "
        f'Save the resume to "{expected_path}".'
    )

    log.info("Starting resume generation")

    system_prompt = build_system_prompt(output_dir, filename)

    options = ClaudeAgentOptions(
        max_turns=30,
        cwd=os.getcwd(),
        model="sonnet",
        allowed_tools=["Skill", "WebSearch", "WebFetch", "Bash", "Write", "Read", "Glob"],
        setting_sources=["project"],
        system_prompt=system_prompt,
        permission_mode="acceptEdits",
    )

    skill_triggered = False
    skill_file_read = False
    tools_used: list[str] = []

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    tools_used.append(block.name)

                    if block.name == "Skill":
                        skill_triggered = True
                        skill_name = ""
                        if isinstance(block.input, dict):
                            skill_name = block.input.get("skill", "")
                        log.info(f'⚡ SKILL TRIGGERED: "{skill_name}"')
                        print(f'\n⚡ Skill triggered: "{skill_name}"')

                    elif block.name == "Read":
                        file_path = ""
                        if isinstance(block.input, dict):
                            file_path = block.input.get("file_path", "")
                        if "docx-js" in file_path or "SKILL" in file_path:
                            skill_file_read = True
                            log.info(f"📖 Skill file read: {file_path}")
                            print(f"\n📖 Reading skill file: {file_path}")
                        else:
                            log.info(f"📄 Read: {file_path}")
                            print(f"\n📄 Reading: {file_path}")

                    elif block.name == "WebSearch":
                        search_query = ""
                        if isinstance(block.input, dict):
                            search_query = block.input.get("query", "")
                        log.info(f"🔍 WebSearch: {search_query}")
                        print(f'\n🔍 Searching: "{search_query}"')

                    elif block.name == "Write":
                        file_path = ""
                        if isinstance(block.input, dict):
                            file_path = block.input.get("file_path", "")
                        log.info(f"✏️  Write: {file_path}")
                        print(f"\n✏️  Writing: {file_path}")

                    elif block.name == "Bash":
                        command = ""
                        if isinstance(block.input, dict):
                            command = str(block.input.get("command", ""))[:80]
                        log.info(f"🔧 Bash: {command}")
                        print(f"\n🔧 Running: {command}")

                    else:
                        log.info(f"🔧 Tool: {block.name}")
                        print(f"\n🔧 Using tool: {block.name}")

        elif isinstance(message, UserMessage):
            if isinstance(message.content, list):
                for block in message.content:
                    if isinstance(block, ToolResultBlock):
                        result_str = str(block.content)[:150]
                        print(
                            f"   ↳ Result: {result_str}"
                            f"{'...' if len(str(block.content)) >= 150 else ''}"
                        )

        elif isinstance(message, ResultMessage):
            print(f"\n✅ Session completed in {message.duration_ms}ms | Turns: {message.num_turns}")
            if message.total_cost_usd is not None:
                print(f"💰 Total cost: ${message.total_cost_usd:.4f}")

    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    log.info(f"Tools used: {', '.join(tools_used)}")
    print(f"  Tools used: {', '.join(dict.fromkeys(tools_used))}")
    print(f"  Skill triggered: {'✅ Yes' if skill_triggered else '❌ No'}")
    print(f"  Skill file read: {'✅ Yes' if skill_file_read else '❌ No'}")

    if not skill_triggered:
        log.warning("⚠️  Skill tool was NOT triggered — agent did not load the docx skill")
        print("  ⚠️  WARNING: Skill was not triggered. The agent skipped the docx skill.")

    if not skill_file_read:
        log.warning("⚠️  Skill file (docx-js.md) was NOT read by the agent")
        print("  ⚠️  WARNING: docx-js.md was not read. Resume may not follow best practices.")

    if os.path.exists(expected_path):
        size_kb = os.path.getsize(expected_path) / 1024
        log.info(f"Resume saved: {expected_path} ({size_kb:.1f} KB)")
        print(f"\n📄 Resume saved to: {expected_path} ({size_kb:.1f} KB)")
        print("=" * 50 + "\n")
    else:
        log.error(f"Resume not found at {expected_path}")
        print(f"\n❌ Resume file was not created at {expected_path}.")
        print("   Check the output above for errors.\n")


def main():
    if len(sys.argv) < 2:
        print('Usage: python resume_generator.py "Person Name"')
        print('Example: python resume_generator.py "Jane Doe"')
        sys.exit(1)

    person_name = sys.argv[1]
    asyncio.run(generate_resume(person_name))


if __name__ == "__main__":
    main()
