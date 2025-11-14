"""
Git Utilities - Check for uncommitted changes and handle them gracefully
"""
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class GitChangeDetector:
    """Utility to detect and handle uncommitted git changes"""
    
    def __init__(self, repo_path: str = "."):
        """Initialize the git change detector
        
        Args:
            repo_path: Path to the git repository (default: current directory)
        """
        self.repo_path = Path(repo_path).resolve()
    
    def is_git_repo(self) -> bool:
        """Check if the current directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def get_uncommitted_changes(self) -> Dict[str, List[str]]:
        """Get all uncommitted changes in the repository
        
        Returns:
            Dictionary with categories of changes:
            - 'modified': List of modified files
            - 'added': List of added files
            - 'deleted': List of deleted files
            - 'untracked': List of untracked files
        """
        if not self.is_git_repo():
            return {"error": ["Not a git repository"]}
        
        try:
            # Get status in porcelain format for easy parsing
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return {"error": [f"Git command failed: {result.stderr}"]}
            
            changes = {
                "modified": [],
                "added": [],
                "deleted": [],
                "untracked": []
            }
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                status = line[:2]
                filename = line[3:]
                
                # Parse git status codes
                if status[0] == 'M' or status[1] == 'M':
                    changes["modified"].append(filename)
                elif status[0] == 'A':
                    changes["added"].append(filename)
                elif status[0] == 'D' or status[1] == 'D':
                    changes["deleted"].append(filename)
                elif status == '??':
                    changes["untracked"].append(filename)
            
            return changes
            
        except subprocess.TimeoutExpired:
            return {"error": ["Git command timed out"]}
        except Exception as e:
            return {"error": [f"Unexpected error: {str(e)}"]}
    
    def has_uncommitted_changes(self) -> bool:
        """Check if there are any uncommitted changes
        
        Returns:
            True if there are uncommitted changes, False otherwise
        """
        changes = self.get_uncommitted_changes()
        
        if "error" in changes:
            return False
        
        return any(changes.values())
    
    def get_change_summary(self) -> str:
        """Get a human-readable summary of uncommitted changes
        
        Returns:
            String summary of changes
        """
        if not self.is_git_repo():
            return "Not a git repository"
        
        changes = self.get_uncommitted_changes()
        
        if "error" in changes:
            return f"Error: {', '.join(changes['error'])}"
        
        if not any(changes.values()):
            return "No uncommitted changes"
        
        summary = []
        
        if changes["modified"]:
            summary.append(f"{len(changes['modified'])} modified file(s)")
        if changes["added"]:
            summary.append(f"{len(changes['added'])} added file(s)")
        if changes["deleted"]:
            summary.append(f"{len(changes['deleted'])} deleted file(s)")
        if changes["untracked"]:
            summary.append(f"{len(changes['untracked'])} untracked file(s)")
        
        return ", ".join(summary)
    
    def proceed_with_changes(self, auto_confirm: bool = False) -> bool:
        """Ask user if they want to proceed despite uncommitted changes
        
        Args:
            auto_confirm: If True, automatically confirm to proceed
            
        Returns:
            True if user wants to proceed, False otherwise
        """
        if not self.has_uncommitted_changes():
            return True
        
        if auto_confirm:
            return True
        
        summary = self.get_change_summary()
        print(f"\n⚠️  Uncommitted changes detected: {summary}")
        print("Files may be out of sync with the repository.")
        
        try:
            response = input("\nProceed anyway? [y/N]: ").strip().lower()
            return response in ('y', 'yes')
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return False


def check_uncommitted_changes(
    repo_path: str = ".",
    auto_proceed: bool = False,
    raise_on_changes: bool = False
) -> Tuple[bool, str]:
    """Convenience function to check for uncommitted changes
    
    Args:
        repo_path: Path to the git repository
        auto_proceed: If True, automatically proceed despite changes
        raise_on_changes: If True, raise an exception when changes are detected
        
    Returns:
        Tuple of (can_proceed, message)
        
    Raises:
        RuntimeError: If raise_on_changes is True and changes are detected
    """
    detector = GitChangeDetector(repo_path)
    
    if not detector.is_git_repo():
        return True, "Not a git repository - skipping check"
    
    has_changes = detector.has_uncommitted_changes()
    
    if not has_changes:
        return True, "No uncommitted changes"
    
    summary = detector.get_change_summary()
    message = f"Uncommitted changes detected: {summary}"
    
    if raise_on_changes:
        raise RuntimeError(message)
    
    if auto_proceed:
        return True, f"{message} (proceeding as configured)"
    
    # Interactive mode
    can_proceed = detector.proceed_with_changes()
    
    if can_proceed:
        return True, f"{message} (user confirmed to proceed)"
    else:
        return False, f"{message} (user chose not to proceed)"


if __name__ == "__main__":
    """Run git change detection as a standalone script"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Check for uncommitted git changes"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to git repository (default: current directory)"
    )
    parser.add_argument(
        "--auto-proceed",
        action="store_true",
        help="Automatically proceed without prompting"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error if uncommitted changes are found"
    )
    
    args = parser.parse_args()
    
    try:
        can_proceed, message = check_uncommitted_changes(
            repo_path=args.path,
            auto_proceed=args.auto_proceed,
            raise_on_changes=args.strict
        )
        
        if can_proceed:
            print(f"✅ {message}")
            sys.exit(0)
        else:
            print(f"❌ {message}")
            sys.exit(1)
            
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
