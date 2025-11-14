#!/usr/bin/env python3
"""
Command-line utility to check for uncommitted git changes before proceeding.

Usage:
    python check_git_status.py              # Interactive mode
    python check_git_status.py --auto-proceed   # Auto-proceed mode
    python check_git_status.py --strict         # Strict mode (exit with error)
"""
import sys
from git_utils import check_uncommitted_changes


def main():
    """Main entry point for the git status checker"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Check for uncommitted git changes and optionally block execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive check (prompts user if changes are found)
  python check_git_status.py
  
  # Auto-proceed (warns but doesn't block)
  python check_git_status.py --auto-proceed
  
  # Strict mode (fails if changes are found)
  python check_git_status.py --strict
  
  # Check specific repository path
  python check_git_status.py --path /path/to/repo

Exit Codes:
  0 - No uncommitted changes or user chose to proceed
  1 - Uncommitted changes found and user chose not to proceed (or strict mode)
        """
    )
    
    parser.add_argument(
        "--path",
        default=".",
        help="Path to git repository (default: current directory)"
    )
    parser.add_argument(
        "--auto-proceed",
        action="store_true",
        help="Automatically proceed without prompting (only warn)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code if uncommitted changes are found (no proceed option)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output (only use exit codes)"
    )
    
    args = parser.parse_args()
    
    try:
        can_proceed, message = check_uncommitted_changes(
            repo_path=args.path,
            auto_proceed=args.auto_proceed,
            raise_on_changes=args.strict
        )
        
        if not args.quiet:
            if can_proceed:
                print(f"✅ {message}")
            else:
                print(f"❌ {message}")
        
        sys.exit(0 if can_proceed else 1)
        
    except RuntimeError as e:
        if not args.quiet:
            print(f"❌ {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        if not args.quiet:
            print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        if not args.quiet:
            print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
