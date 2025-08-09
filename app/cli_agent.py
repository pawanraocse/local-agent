import argparse
from agent import Agent
from dto.code_generation import CodeGenerationRequest, CodeGenerationResponse
import logging

logger = logging.getLogger("cli")

def main():
    parser = argparse.ArgumentParser(description="Local-Agent CLI: Code generation and review via LLM")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Code generation command
    gen_parser = subparsers.add_parser("generate", help="Generate code for a given task")
    gen_parser.add_argument("--task", required=True, help="Task description for code generation")
    gen_parser.add_argument("--context", default="", help="Optional context for the task")

    # Code review command
    review_parser = subparsers.add_parser("review", help="Review code for quality, bugs, and improvements")
    review_parser.add_argument("--code", required=True, help="Code to review (as a string or file path)")

    args = parser.parse_args()
    agent = Agent()

    if args.command == "generate":
        req = CodeGenerationRequest(task=args.task, context=args.context)
        logger.info(f"[CLI] Generating code for task: {req.task}")
        code = agent.generate_code(task=req.task, context=req.context)
        print("\nGenerated Code:\n" + code)
    elif args.command == "review":
        code_input = args.code
        # If the code argument is a file path, read the file
        try:
            if code_input.endswith('.py') or code_input.endswith('.txt'):
                with open(code_input, 'r') as f:
                    code_input = f.read()
        except Exception as e:
            logger.warning(f"Could not read file: {e}. Using input as code string.")
        logger.info("[CLI] Reviewing code...")
        review = agent.review_code(code=code_input)
        print("\nReview Result:\n" + review)

if __name__ == "__main__":
    main()

