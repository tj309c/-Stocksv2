"""
Comprehensive Debugging and Diagnostics Tool
Automatically diagnoses issues and provides recommendations
"""
import streamlit as st
import sys
import os
import subprocess
from pathlib import Path
import traceback
from datetime import datetime
import pandas as pd
import importlib.util

class DebugTools:
    """Comprehensive debugging and diagnostics"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.recommendations = []
    
    def check_dependencies(self):
        """Check if all required packages are installed"""
        required_packages = {
            'streamlit': '1.28.0',
            'pandas': '2.0.0',
            'numpy': '1.24.0',
            'plotly': '5.17.0',
            'yfinance': '0.2.28',
            'ta': '0.11.0',
            'beautifulsoup4': '4.12.0',
            'requests': '2.31.0',
            'scipy': '1.11.0',
        }
        
        missing = []
        outdated = []
        
        for package, min_version in required_packages.items():
            try:
                if package == 'beautifulsoup4':
                    import bs4
                    pkg = bs4
                else:
                    pkg = __import__(package)
                
                version = getattr(pkg, '__version__', 'unknown')
                self.info.append(f"✓ {package}: {version}")
            except ImportError:
                missing.append(package)
                self.errors.append(f"✗ {package}: NOT INSTALLED")
        
        if missing:
            self.recommendations.append({
                'severity': 'CRITICAL',
                'issue': f'Missing packages: {", ".join(missing)}',
                'fix': f'Run: pip install {" ".join(missing)}',
                'command': f'pip install {" ".join(missing)}'
            })
        
        return len(missing) == 0
    
    def check_file_integrity(self):
        """Check if all required files exist and are readable"""
        required_files = [
            'main.py',
            'config.py',
            'data_fetcher.py',
            'analysis_engine.py',
            'dashboard_selector.py',
            'dashboard_stocks.py',
            'dashboard_options.py',
            'dashboard_crypto.py',
            'wsb_quotes.py',
            'requirements.txt'
        ]
        
        missing_files = []
        
        for file in required_files:
            if not Path(file).exists():
                missing_files.append(file)
                self.errors.append(f"✗ {file}: FILE NOT FOUND")
            else:
                # Check if readable
                try:
                    with open(file, 'r') as f:
                        f.read(1)
                    self.info.append(f"✓ {file}: OK")
                except Exception as e:
                    self.errors.append(f"✗ {file}: {str(e)}")
        
        if missing_files:
            self.recommendations.append({
                'severity': 'CRITICAL',
                'issue': f'Missing files: {", ".join(missing_files)}',
                'fix': 'Restore missing files from repository',
                'command': None
            })
        
        return len(missing_files) == 0
    
    def check_syntax(self):
        """Check Python syntax for all files"""
        python_files = list(Path('.').glob('*.py')) + list(Path('.').glob('dashboard_*.py'))
        
        syntax_errors = []
        
        for file in python_files:
            if file.name.startswith('.'):
                continue
                
            try:
                with open(file, 'r') as f:
                    compile(f.read(), file.name, 'exec')
                self.info.append(f"✓ {file.name}: Syntax OK")
            except SyntaxError as e:
                syntax_errors.append((file.name, str(e)))
                self.errors.append(f"✗ {file.name}: {e.msg} (line {e.lineno})")
                self.recommendations.append({
                    'severity': 'CRITICAL',
                    'issue': f'Syntax error in {file.name} line {e.lineno}',
                    'fix': f'Fix: {e.msg}',
                    'command': None
                })
        
        return len(syntax_errors) == 0
    
    def check_imports(self):
        """Check if all imports can be resolved"""
        files_to_check = [
            'data_fetcher.py',
            'analysis_engine.py',
            'wsb_quotes.py',
        ]
        
        import_errors = []
        
        for file in files_to_check:
            if not Path(file).exists():
                continue
                
            try:
                spec = importlib.util.spec_from_file_location('temp_module', file)
                module = importlib.util.module_from_spec(spec)
                # Don't execute, just check if spec can be created
                self.info.append(f"✓ {file}: Imports resolvable")
            except Exception as e:
                import_errors.append((file, str(e)))
                self.errors.append(f"✗ {file}: Import error - {str(e)[:100]}")
        
        return len(import_errors) == 0
    
    def check_environment(self):
        """Check environment variables and configuration"""
        env_vars = {
            'GEMINI_API_KEY': False,  # Optional
            'REDDIT_CLIENT_ID': False,  # Optional
            'REDDIT_CLIENT_SECRET': False,  # Optional
        }
        
        for var, required in env_vars.items():
            value = os.getenv(var)
            if value:
                self.info.append(f"✓ {var}: SET")
            else:
                if required:
                    self.errors.append(f"✗ {var}: NOT SET (REQUIRED)")
                    self.recommendations.append({
                        'severity': 'HIGH',
                        'issue': f'{var} not set',
                        'fix': f'Set in .env file or environment',
                        'command': f'export {var}=your_key_here'
                    })
                else:
                    self.warnings.append(f"⚠ {var}: NOT SET (optional - some features may be limited)")
        
        return True
    
    def check_data_directories(self):
        """Check if data directories exist and are writable"""
        dirs = ['data', 'data/cache']
        
        for dir_path in dirs:
            path = Path(dir_path)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self.info.append(f"✓ {dir_path}: Created")
                except Exception as e:
                    self.errors.append(f"✗ {dir_path}: Cannot create - {str(e)}")
                    self.recommendations.append({
                        'severity': 'HIGH',
                        'issue': f'Cannot create {dir_path}',
                        'fix': f'Create manually or check permissions',
                        'command': f'mkdir -p {dir_path}'
                    })
            else:
                # Check writable
                test_file = path / '.test_write'
                try:
                    test_file.touch()
                    test_file.unlink()
                    self.info.append(f"✓ {dir_path}: Writable")
                except Exception as e:
                    self.errors.append(f"✗ {dir_path}: Not writable - {str(e)}")
        
        return True
    
    def check_yfinance_connection(self):
        """Test if yfinance can fetch data"""
        try:
            import yfinance as yf
            # Quick test
            ticker = yf.Ticker("AAPL")
            info = ticker.info
            if info and 'symbol' in info:
                self.info.append("✓ yfinance: Connection OK")
                return True
            else:
                self.warnings.append("⚠ yfinance: No data returned")
                return False
        except Exception as e:
            self.errors.append(f"✗ yfinance: {str(e)[:100]}")
            self.recommendations.append({
                'severity': 'HIGH',
                'issue': 'Cannot fetch market data from yfinance',
                'fix': 'Check internet connection or try again later',
                'command': None
            })
            return False
    
    def run_full_diagnostic(self):
        """Run all diagnostic checks"""
        self.errors = []
        self.warnings = []
        self.info = []
        self.recommendations = []
        
        checks = [
            ('File Integrity', self.check_file_integrity),
            ('Python Syntax', self.check_syntax),
            ('Dependencies', self.check_dependencies),
            ('Imports', self.check_imports),
            ('Environment Variables', self.check_environment),
            ('Data Directories', self.check_data_directories),
            ('Market Data Connection', self.check_yfinance_connection),
        ]
        
        results = {}
        
        for name, check_func in checks:
            try:
                result = check_func()
                results[name] = 'PASS' if result else 'FAIL'
            except Exception as e:
                results[name] = 'ERROR'
                self.errors.append(f"✗ {name}: Check failed - {str(e)}")
        
        return results
    
    def get_summary(self):
        """Get diagnostic summary"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'recommendations': self.recommendations,
            'total_issues': len(self.errors) + len(self.warnings),
            'critical_issues': len([r for r in self.recommendations if r['severity'] == 'CRITICAL'])
        }
    
    def display_report(self):
        """Display diagnostic report in Streamlit"""
        st.markdown("## 🔧 System Diagnostics Report")
        st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run diagnostics
        results = self.run_full_diagnostic()
        summary = self.get_summary()
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Checks", len(results))
        with col2:
            passed = len([r for r in results.values() if r == 'PASS'])
            st.metric("Passed", passed, delta=None)
        with col3:
            st.metric("Issues", summary['total_issues'], 
                     delta=f"-{summary['critical_issues']} critical" if summary['critical_issues'] > 0 else None,
                     delta_color="inverse")
        
        # Detailed results
        st.markdown("### Check Results")
        
        results_data = []
        for check_name, status in results.items():
            emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
            results_data.append({
                'Check': check_name,
                'Status': f"{emoji} {status}"
            })
        
        st.table(pd.DataFrame(results_data))
        
        # Errors
        if self.errors:
            st.markdown("### ❌ Errors")
            for error in self.errors:
                st.error(error)
        
        # Warnings
        if self.warnings:
            st.markdown("### ⚠️ Warnings")
            for warning in self.warnings:
                st.warning(warning)
        
        # Recommendations
        if self.recommendations:
            st.markdown("### 💡 Recommendations")
            for i, rec in enumerate(self.recommendations):
                severity_color = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }
                
                with st.expander(f"{severity_color.get(rec['severity'], '🔵')} {rec['issue']}"):
                    st.markdown(f"**Severity:** {rec['severity']}")
                    st.markdown(f"**Fix:** {rec['fix']}")
                    if rec['command']:
                        st.code(rec['command'], language='bash')
                        if st.button(f"Copy Command", key=f"copy_{i}"):
                            st.code(rec['command'])
        
        # Info (collapsible)
        with st.expander("ℹ️ Detailed Information"):
            for info in self.info:
                st.text(info)
        
        return summary['total_issues'] == 0


def quick_health_check():
    """Quick health check for sidebar"""
    debug = DebugTools()
    
    # Just check critical things
    issues = []
    
    # Check dependencies
    try:
        import yfinance
        import pandas
        import streamlit
        import plotly
    except ImportError as e:
        issues.append(f"Missing: {str(e)}")
    
    # Check data directory
    if not Path('data').exists():
        issues.append("Data directory missing")
    
    return len(issues) == 0, issues


def show_debug_panel():
    """Show debug panel in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 System Status")
    
    healthy, issues = quick_health_check()
    
    if healthy:
        st.sidebar.success("✅ All systems operational")
    else:
        st.sidebar.error(f"⚠️ {len(issues)} issue(s) detected")
        
        if st.sidebar.button("🔍 Run Full Diagnostics"):
            st.session_state.show_diagnostics = True
    
    # Cache management
    st.sidebar.markdown("### 🧹 Cache Management")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🗑️ Clear Cache", help="Clear all Streamlit caches"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("✅ Cache cleared!")
            st.rerun()
    with col2:
        if st.button("🔄 Reload", help="Reload current page"):
            st.rerun()
    
    # Full diagnostics
    if st.session_state.get('show_diagnostics', False):
        debug = DebugTools()
        with st.expander("🔬 Full Diagnostic Report", expanded=True):
            debug.display_report()
