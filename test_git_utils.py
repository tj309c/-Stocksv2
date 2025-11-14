#!/usr/bin/env python3
"""
Unit tests for git_utils module
"""
import os
import tempfile
import subprocess
from pathlib import Path
from git_utils import GitChangeDetector, check_uncommitted_changes


def test_is_git_repo():
    """Test detection of git repository"""
    print("Testing git repository detection...")
    
    detector = GitChangeDetector(".")
    assert detector.is_git_repo(), "Current directory should be a git repo"
    print("✅ Git repo detection works")


def test_clean_repo():
    """Test with clean repository"""
    print("\nTesting clean repository...")
    
    # First ensure repo is clean
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print(f"⚠️  Repository has uncommitted changes, skipping clean repo test")
        return
    
    detector = GitChangeDetector(".")
    assert not detector.has_uncommitted_changes(), "Clean repo should have no changes"
    
    changes = detector.get_uncommitted_changes()
    assert not any(changes.values()), "All change lists should be empty"
    
    summary = detector.get_change_summary()
    assert summary == "No uncommitted changes", f"Expected 'No uncommitted changes', got '{summary}'"
    
    print("✅ Clean repository test passed")


def test_with_uncommitted_file():
    """Test with an uncommitted file"""
    print("\nTesting with uncommitted file...")
    
    # Create a temporary test file
    test_file = Path("test_temp_file.txt")
    test_file.write_text("test content")
    
    try:
        detector = GitChangeDetector(".")
        assert detector.has_uncommitted_changes(), "Should detect uncommitted file"
        
        changes = detector.get_uncommitted_changes()
        assert "test_temp_file.txt" in changes["untracked"], "Should detect untracked file"
        
        summary = detector.get_change_summary()
        assert "untracked" in summary.lower(), f"Summary should mention untracked files: {summary}"
        
        print("✅ Uncommitted file detection works")
        
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def test_check_uncommitted_changes_function():
    """Test the convenience function"""
    print("\nTesting check_uncommitted_changes function...")
    
    can_proceed, message = check_uncommitted_changes(
        repo_path=".",
        auto_proceed=True
    )
    
    assert can_proceed, "Should always be able to proceed with auto_proceed=True"
    assert isinstance(message, str), "Should return a message string"
    
    print(f"✅ Function works: {message}")


def test_non_git_directory():
    """Test behavior in non-git directory"""
    print("\nTesting non-git directory...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        detector = GitChangeDetector(tmpdir)
        assert not detector.is_git_repo(), "Temp dir should not be a git repo"
        
        summary = detector.get_change_summary()
        assert summary == "Not a git repository", f"Expected 'Not a git repository', got '{summary}'"
        
        print("✅ Non-git directory handling works")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Git Utils Test Suite")
    print("=" * 60)
    
    tests = [
        test_is_git_repo,
        test_clean_repo,
        test_with_uncommitted_file,
        test_check_uncommitted_changes_function,
        test_non_git_directory
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
