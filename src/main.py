"""CLI entry point for Offline-DevOps-Agent-with-LLM-Brain."""

from .agent.agent import run_agent_task
from .analyzer.analyzer import analyze_logs
from .optimizer.optimizer import optimize_task

# Optional LLM backend (import lazily when used)
from typing import Optional


import argparse
from typing import Optional


def handle_analyze_logs(log_path: str) -> None:
    """Wrapper to call the analyzer module."""
    analyze_logs(log_path)


def handle_run_task(task_name: str) -> None:
    """Wrapper to run an agent task and optionally optimize it."""
    run_agent_task(task_name)
    optimize_task(task_name)


def main(argv: Optional[list] = None) -> None:
    parser = argparse.ArgumentParser(description="Offline DevOps Agent with LLM Brain")
    parser.add_argument('--analyze-logs', help='Path to logs', type=str)
    parser.add_argument('--run-task', help='Task to run', type=str)
    parser.add_argument('--backend', help='LLM backend to use (transformers)', type=str, default='transformers')
    parser.add_argument('--model-path', help='Local model path for the LLM', type=str)
    parser.add_argument('--query', help='Run the LLM on this prompt', type=str)
    parser.add_argument('--max-tokens', help='Max tokens to generate', type=int, default=128)
    parser.add_argument('--temperature', help='Sampling temperature', type=float, default=1.0)

    args = parser.parse_args(argv)

    if args.analyze_logs:
        handle_analyze_logs(args.analyze_logs)
    if args.run_task:
        handle_run_task(args.run_task)

    if args.query:
        if not args.model_path:
            print("Provide --model-path pointing to a local HF model directory when using --query")
            return
        if args.backend == 'transformers':
            try:
                from .llm.llm import LocalLLM
            except Exception as e:
                print("Transformers backend requires 'transformers' and 'torch' installed. Error:", e)
                return

            llm = LocalLLM(args.model_path)
            out = llm.generate(args.query, max_tokens=args.max_tokens, temperature=args.temperature)
            print("\n=== LLM Output ===\n")
            print(out)


if __name__ == "__main__":
    main()