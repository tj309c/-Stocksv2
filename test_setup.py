"""
Test script to verify the dashboard setup
"""
import sys
import importlib
from pathlib import Path

def test_dependencies():
    """Test if all required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'yfinance',
        'ta',
        'scipy',
        'sklearn',
        'bs4',
        'requests'
    ]
    
    print("🔍 Checking dependencies...")
    missing = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"Run: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def test_data_fetching():
    """Test if data fetching works"""
    print("\n🔍 Testing data fetching...")
    
    try:
        import yfinance as yf
        
        # Test with META
        ticker = yf.Ticker("META")
        info = ticker.info
        
        if info and "currentPrice" in info:
            print(f"✅ Successfully fetched META price: ${info['currentPrice']:.2f}")
            return True
        else:
            print("⚠️ Data fetched but price not found")
            return True
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return False

def test_modules():
    """Test if custom modules load"""
    print("\n🔍 Testing custom modules...")
    
    modules = [
        'data_fetcher',
        'analysis_engine'
    ]
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}.py loads successfully")
        except Exception as e:
            print(f"❌ Error loading {module}.py: {e}")
            return False
    
    return True

def test_cache_directory():
    """Test if cache directory can be created"""
    print("\n🔍 Testing cache directory...")
    
    cache_dir = Path("data/cache")
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Cache directory ready: {cache_dir.absolute()}")
        return True
    except Exception as e:
        print(f"❌ Error creating cache directory: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🎯 Smart Investment Dashboard - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Data Fetching", test_data_fetching),
        ("Custom Modules", test_modules),
        ("Cache Directory", test_cache_directory)
    ]
    
    results = []
    for name, test_func in tests:
        results.append(test_func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed! Your dashboard is ready to run.")
        print("\nRun the dashboard with:")
        print("  streamlit run main.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install missing packages: pip install -r requirements.txt")
        print("  2. Ensure all .py files are in the same directory")
        print("  3. Check internet connection for data fetching")
    print("=" * 50)

if __name__ == "__main__":
    main()
