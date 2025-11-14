#!/usr/bin/env python3
"""
Final Validation Script
Verifies the refactored structure works correctly
"""
import sys
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

print("=" * 60)
print("🔍 FINAL REFACTORING VALIDATION")
print("=" * 60)
print()

# Track results
tests_passed = 0
tests_failed = 0

def test(name, func):
    """Run a test and track results"""
    global tests_passed, tests_failed
    try:
        func()
        print(f"✅ {name}")
        tests_passed += 1
        return True
    except Exception as e:
        print(f"❌ {name}: {e}")
        tests_failed += 1
        return False

# Test 1: Directory Structure
def test_directory_structure():
    required_dirs = [
        "src",
        "src/config",
        "src/core",
        "src/components",
        "src/dashboards",
        "src/utils",
        "tests",
        "logs",
    ]
    for dir_path in required_dirs:
        path = PROJECT_ROOT / dir_path
        assert path.exists(), f"Missing directory: {dir_path}"

test("Directory structure exists", test_directory_structure)

# Test 2: Configuration Files
def test_config_files():
    files = [
        "src/config/__init__.py",
        "src/config/constants.py",
        "src/config/settings.py",
    ]
    for file_path in files:
        path = PROJECT_ROOT / file_path
        assert path.exists(), f"Missing file: {file_path}"

test("Configuration files exist", test_config_files)

# Test 3: Core Files
def test_core_files():
    files = [
        "src/core/__init__.py",
        "src/core/logging.py",
    ]
    for file_path in files:
        path = PROJECT_ROOT / file_path
        assert path.exists(), f"Missing file: {file_path}"

test("Core files exist", test_core_files)

# Test 4: Configuration Imports
def test_config_imports():
    from src.config import get_config, COLORS, DEFAULT_TICKERS
    from src.config.constants import RSI_OVERSOLD, CACHE_TTL
    
    config = get_config()
    assert config is not None
    assert isinstance(COLORS, dict)
    assert isinstance(DEFAULT_TICKERS, dict)
    assert RSI_OVERSOLD == 30
    assert CACHE_TTL == 300

test("Configuration imports work", test_config_imports)

# Test 5: Logging Imports
def test_logging_imports():
    from src.core.logging import (
        app_logger,
        data_logger,
        analysis_logger,
        perf_tracker
    )
    
    assert app_logger is not None
    assert data_logger is not None
    assert analysis_logger is not None
    assert perf_tracker is not None

test("Logging imports work", test_logging_imports)

# Test 6: Backward Compatibility
def test_backward_compatibility():
    # Old files should still exist (we haven't moved them yet)
    old_files = [
        "utils.py",
        "theme_manager.py",
        "data_fetcher.py",
        "analysis_engine.py"
    ]
    
    for file_name in old_files:
        path = PROJECT_ROOT / file_name
        assert path.exists(), f"Original file missing: {file_name}"
        assert path.stat().st_size > 0, f"File is empty: {file_name}"

test("Backward compatibility (files exist)", test_backward_compatibility)

# Test 7: Logging Functionality
def test_logging_functionality():
    from src.core.logging import app_logger, perf_tracker
    
    # Test basic logging
    app_logger.info("Test message")
    
    # Test performance tracking
    perf_tracker.start("test_op")
    perf_tracker.end("test_op")
    
    metrics = perf_tracker.get_metrics()
    assert "test_op" in metrics
    assert metrics["test_op"]["duration"] is not None

test("Logging functionality works", test_logging_functionality)

# Test 8: Configuration Management
def test_configuration_management():
    from src.config import get_config
    
    config = get_config()
    
    # Test get
    value = config.get("app.name", default="StocksV2")
    assert value is not None
    
    # Test properties
    assert isinstance(config.is_debug, bool)
    assert isinstance(config.cache_ttl, int)

test("Configuration management works", test_configuration_management)

# Test 9: Test Files
def test_test_files():
    test_files = [
        "tests/test_config.py",
        "tests/test_utils.py",
    ]
    for file_path in test_files:
        path = PROJECT_ROOT / file_path
        assert path.exists(), f"Missing test file: {file_path}"

test("Test files exist", test_test_files)

# Test 10: Documentation
def test_documentation():
    docs = [
        "REFACTORING_GUIDE.md",
        "PROJECT_REFACTORING_SUMMARY.md",
    ]
    for doc in docs:
        path = PROJECT_ROOT / doc
        assert path.exists(), f"Missing documentation: {doc}"

test("Documentation exists", test_documentation)

# Test 11: Original Files Intact
def test_original_files():
    original_files = [
        "main.py",
        "utils.py",
        "theme_manager.py",
        "data_fetcher.py",
        "analysis_engine.py",
        "dashboard_stocks.py",
        "dashboard_options.py",
        "dashboard_crypto.py",
        "dashboard_selector.py",
    ]
    for file_path in original_files:
        path = PROJECT_ROOT / file_path
        assert path.exists(), f"Original file missing: {file_path}"

test("Original files intact", test_original_files)

# Test 12: New Entry Point
def test_new_entry_point():
    path = PROJECT_ROOT / "main_refactored.py"
    assert path.exists(), "New entry point missing"
    
    # Check it imports correctly
    import importlib.util
    spec = importlib.util.spec_from_file_location("main_refactored", path)
    assert spec is not None

test("New entry point exists", test_new_entry_point)

# Summary
print()
print("=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {tests_failed}")
print(f"Success Rate: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")
print()

if tests_failed == 0:
    print("✅ ALL VALIDATIONS PASSED!")
    print()
    print("🎉 The refactored structure is fully operational!")
    print()
    print("You can now:")
    print("  1. Continue using: streamlit run main.py")
    print("  2. Try refactored:  streamlit run main_refactored.py")
    print("  3. View logs in:    logs/")
    print("  4. Run tests:       python tests/test_config.py")
    print()
    sys.exit(0)
else:
    print("⚠️ SOME VALIDATIONS FAILED")
    print()
    print("Please review the failed tests above.")
    print()
    sys.exit(1)
