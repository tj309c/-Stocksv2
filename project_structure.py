"""
Project Organization Script
Maintains backward compatibility while introducing new organized structure
"""
import sys
from pathlib import Path

# Add both old and new paths to Python path for compatibility
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"

# Add paths
for path in [PROJECT_ROOT, SRC_DIR]:
    path_str = str(path.absolute())
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

# Import mapping for backward compatibility
# This allows old imports to work while gradually migrating to new structure
import importlib.util

def setup_compatibility_imports():
    """Setup compatibility layer for old imports"""
    # Map old module names to new locations
    module_mapping = {
        # Keep old imports working
        'utils': 'src.utils',
        'config': 'src.config',
        'theme_manager': 'src.components.theme_manager',
        'data_fetcher': 'src.components.data_fetcher',
        'analysis_engine': 'src.components.analysis_engine',
        'wsb_quotes': 'src.utils.wsb_quotes',
        'debug_tools': 'src.utils.debug_tools',
    }
    
    return module_mapping

# Setup on import
MODULE_MAPPING = setup_compatibility_imports()
