import json
import os
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from research_system.core.file_scanner import scan_directory
from research_system.core.graph import build_graph
from research_system.core.state import ReviewState
from config import OUTPUT_DIR

console = Console()

def save_report(report: dict, target: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    json_path = os.path.join(OUTPUT_DIR, "report.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)


    md_path = os.path.join(OUTPUT_DIR, "report.md")
    with open(md_path, "w") as f:
        s = report["summary"]
        f.write(f"# Code Review Report\n\n")
        f.write(f"**Scanned:** `{target}`  \n")
        f.write(f"**Files:** {report['meta']['total_files_scanned']}  \n")
        f.write(f"**Total Findings:** {report['meta']['total_findings']}\n\n")
        f.write(f"## Summary\n")
        f.write(f"| Severity | Count |\n|---|---|\n")
        for level in ["critical", "high", "medium", "low", "info"]:
            f.write(f"| {level.capitalize()} | {s[level]} |\n")
        f.write(f"\n## Findings\n\n")
        for finding in report["findings_by_severity"]:
            f.write(f"### [{finding['severity'].upper()}] {finding['category']}\n")
            f.write(f"**Agent:** {finding['agent']}  \n")
            f.write(f"**File:** `{finding['file']}`  \n")
            if finding.get('line_hint'):
                f.write(f"**Location:** {finding['line_hint']}  \n")
            f.write(f"\n{finding['description']}\n\n")
            f.write(f"**💡 Suggestion:** {finding['suggestion']}\n\n---\n\n")

    return json_path, md_path

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Code Review System")
    parser.add_argument("target", help="Path to the codebase directory to review")
    args = parser.parse_args()

    console.print(Panel.fit("🤖 Multi-Agent Code Review System", style="bold blue"))

    console.print(f"\n📂 Scanning [bold]{args.target}[/bold]...")
    try:
        files, scan_errors = scan_directory(args.target)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    if not files:
        console.print("[yellow]No supported files found. Exiting.[/yellow]")
        sys.exit(0)

    console.print(f"   Found [green]{len(files)}[/green] files to review.")
    if scan_errors:
        console.print(f"   [yellow]{len(scan_errors)} files skipped[/yellow]")


    initial_state = ReviewState(
        target_directory=args.target,
        files=files,
        security_findings=[],
        architecture_findings=[],
        code_quality_findings=[],
        final_report=None,
        errors=scan_errors
    )

    console.print("\n🚀 Running agents...\n")
    graph = build_graph()

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Agents analyzing your codebase...", total=None)
        final_state = graph.invoke(initial_state)
        progress.update(task, completed=True)

    report = final_state["final_report"]
    json_path, md_path = save_report(report, args.target)

    s = report["summary"]
    console.print(Panel(
        f"[red]Critical: {s['critical']}[/red]  [orange1]High: {s['high']}[/orange1]  "
        f"[yellow]Medium: {s['medium']}[/yellow]  [green]Low: {s['low']}[/green]  Info: {s['info']}",
        title="📊 Results Summary"
    ))
    console.print(f"\n✅ Reports saved:")
    console.print(f"   JSON → [bold]{json_path}[/bold]")
    console.print(f"   Markdown → [bold]{md_path}[/bold]")

if __name__ == "__main__":
    main()