"""
Progressive Loading Indicators
Provides visual feedback during long operations to eliminate perceived freezing.

Features:
- Progress bars with time estimation
- Skeleton loaders for charts/tables
- Async loading wrappers
- Step-by-step progress tracking
"""
import streamlit as st
import time
from typing import Callable, Any, Dict, List, Optional
from contextlib import contextmanager
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# PROGRESS BAR UTILITIES
# ============================================================================

@dataclass
class ProgressStep:
    """Represents a step in a multi-step loading operation"""
    name: str
    weight: float = 1.0  # Relative weight (for progress calculation)
    estimated_seconds: float = 1.0


class ProgressTracker:
    """Tracks progress across multiple steps with time estimation"""
    
    def __init__(self, steps: List[ProgressStep], show_time: bool = True):
        self.steps = steps
        self.current_step = 0
        self.show_time = show_time
        self.start_time = time.time()
        self.total_weight = sum(step.weight for step in steps)
        self.completed_weight = 0.0
        
        # Create progress bar
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
        
    def update(self, step_index: int, message: str = None):
        """Update progress to a specific step"""
        if step_index >= len(self.steps):
            self.complete()
            return
        
        self.current_step = step_index
        step = self.steps[step_index]
        
        # Calculate progress
        self.completed_weight = sum(s.weight for s in self.steps[:step_index])
        progress = self.completed_weight / self.total_weight
        
        # Update progress bar
        self.progress_bar.progress(progress)
        
        # Calculate time remaining
        elapsed = time.time() - self.start_time
        if progress > 0:
            estimated_total = elapsed / progress
            remaining = estimated_total - elapsed
        else:
            remaining = sum(s.estimated_seconds for s in self.steps[step_index:])
        
        # Update status text
        display_message = message or step.name
        if self.show_time and remaining > 0:
            remaining_str = f"{int(remaining)}s" if remaining < 60 else f"{int(remaining/60)}m {int(remaining%60)}s"
            self.status_text.text(f"⏳ {display_message} (Est. {remaining_str} remaining)")
        else:
            self.status_text.text(f"⏳ {display_message}")
    
    def next(self, message: str = None):
        """Move to next step"""
        self.update(self.current_step + 1, message)
    
    def complete(self, message: str = "Complete! ✅"):
        """Mark progress as complete"""
        self.progress_bar.progress(1.0)
        elapsed = time.time() - self.start_time
        if self.show_time:
            self.status_text.text(f"✅ {message} ({elapsed:.1f}s)")
        else:
            self.status_text.text(f"✅ {message}")
        time.sleep(0.5)  # Brief pause to show completion
        self.progress_bar.empty()
        self.status_text.empty()


@contextmanager
def show_progress(steps: List[ProgressStep], show_time: bool = True):
    """Context manager for showing progress across multiple steps"""
    tracker = ProgressTracker(steps, show_time)
    try:
        yield tracker
    finally:
        tracker.complete()


# ============================================================================
# SKELETON LOADERS
# ============================================================================

def show_skeleton_chart(height: int = 400):
    """Display skeleton loader for chart"""
    st.markdown(f"""
    <div style="
        width: 100%;
        height: {height}px;
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 8px;
        margin: 10px 0;
    ">
    </div>
    <style>
        @keyframes loading {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}
    </style>
    """, unsafe_allow_html=True)


def show_skeleton_table(rows: int = 5, columns: int = 4):
    """Display skeleton loader for table"""
    skeleton_html = """
    <style>
        .skeleton-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        .skeleton-cell {
            height: 20px;
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
            border-radius: 4px;
            margin: 5px;
        }
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    <table class="skeleton-table">
    """
    
    for _ in range(rows):
        skeleton_html += "<tr>"
        for _ in range(columns):
            skeleton_html += '<td><div class="skeleton-cell"></div></td>'
        skeleton_html += "</tr>"
    
    skeleton_html += "</table>"
    st.markdown(skeleton_html, unsafe_allow_html=True)


def show_skeleton_metric(count: int = 4):
    """Display skeleton loader for metrics row"""
    cols = st.columns(count)
    for col in cols:
        with col:
            st.markdown("""
            <div style="
                width: 100%;
                height: 80px;
                background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
                background-size: 200% 100%;
                animation: loading 1.5s infinite;
                border-radius: 8px;
                margin: 10px 0;
            "></div>
            """, unsafe_allow_html=True)


def show_skeleton_card(height: int = 200):
    """Display skeleton loader for card/panel"""
    st.markdown(f"""
    <div style="
        width: 100%;
        height: {height}px;
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 12px;
        margin: 10px 0;
        padding: 20px;
    ">
        <div style="
            width: 60%;
            height: 20px;
            background: #d0d0d0;
            border-radius: 4px;
            margin-bottom: 15px;
        "></div>
        <div style="
            width: 40%;
            height: 15px;
            background: #d0d0d0;
            border-radius: 4px;
        "></div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ASYNC LOADING WRAPPERS
# ============================================================================

def async_load_with_placeholder(
    load_func: Callable[[], Any],
    placeholder_func: Callable[[], None] = None,
    success_message: str = None
) -> Any:
    """
    Load data asynchronously with placeholder.
    
    Args:
        load_func: Function that loads the data
        placeholder_func: Function that shows placeholder (skeleton loader)
        success_message: Optional success message
    
    Returns:
        Result from load_func
    """
    # Create placeholder container
    container = st.container()
    
    with container:
        # Show placeholder
        if placeholder_func:
            placeholder_func()
        else:
            st.info("⏳ Loading...")
    
    # Load data
    try:
        result = load_func()
        
        # Clear placeholder and show success
        container.empty()
        if success_message:
            st.success(success_message, icon="✅")
            time.sleep(0.5)
        
        return result
    
    except Exception as e:
        container.empty()
        st.error(f"❌ Error loading data: {e}")
        logger.error(f"Async load error: {e}", exc_info=True)
        return None


def progressive_load(
    tasks: List[Dict[str, Any]],
    show_time: bool = True
) -> Dict[str, Any]:
    """
    Load multiple tasks progressively with visual feedback.
    
    Args:
        tasks: List of task dicts with keys:
            - name: Display name
            - func: Function to execute
            - weight: Relative weight (default 1.0)
            - estimated_seconds: Estimated time (default 1.0)
            - key: Key for result dict
        show_time: Show time estimation
    
    Returns:
        Dict mapping task keys to results
    """
    # Create progress steps
    steps = [
        ProgressStep(
            name=task.get("name", "Loading..."),
            weight=task.get("weight", 1.0),
            estimated_seconds=task.get("estimated_seconds", 1.0)
        )
        for task in tasks
    ]
    
    results = {}
    
    with show_progress(steps, show_time) as tracker:
        for i, task in enumerate(tasks):
            tracker.update(i)
            
            try:
                # Execute task
                result = task["func"]()
                key = task.get("key", f"task_{i}")
                results[key] = result
                
            except Exception as e:
                logger.error(f"Error in task {task.get('name', i)}: {e}", exc_info=True)
                key = task.get("key", f"task_{i}")
                results[key] = {"error": str(e)}
            
            tracker.next()
    
    return results


# ============================================================================
# SPINNER WITH TIME ESTIMATION
# ============================================================================

@contextmanager
def spinner_with_timer(message: str, estimated_seconds: float = None):
    """
    Context manager for spinner with time estimation.
    
    Args:
        message: Message to display
        estimated_seconds: Estimated time (optional)
    """
    if estimated_seconds:
        est_str = f"{int(estimated_seconds)}s" if estimated_seconds < 60 else f"{int(estimated_seconds/60)}m {int(estimated_seconds%60)}s"
        full_message = f"{message} (Est. {est_str})"
    else:
        full_message = message
    
    start_time = time.time()
    
    with st.spinner(full_message):
        yield
    
    elapsed = time.time() - start_time
    st.success(f"✅ {message} completed in {elapsed:.1f}s", icon="✅")
    time.sleep(0.3)


# ============================================================================
# PROGRESSIVE DATA FETCHING
# ============================================================================

class ProgressiveDataFetcher:
    """Fetches data progressively with visual feedback"""
    
    def __init__(self, components: Dict):
        self.components = components
        self.cache = {}
    
    def fetch_stock_data_progressive(self, ticker: str) -> Dict:
        """Fetch stock data with progressive loading indicators"""
        from src.config.performance_config import (
            get_current_mode,
            should_fetch_institutional,
            should_fetch_sentiment,
            should_fetch_options
        )
        
        mode = get_current_mode()
        
        # Define tasks based on mode
        tasks = [
            {
                "name": f"📊 Fetching {ticker} stock data",
                "func": lambda: self.components["fetcher"].get_stock_data(ticker),
                "key": "stock_data",
                "weight": 1.5,
                "estimated_seconds": 5 if mode.name == "Deep Mode 🔬" else 2
            },
            {
                "name": "💰 Getting real-time quote",
                "func": lambda: self.components["fetcher"].get_realtime_quote(ticker),
                "key": "quote",
                "weight": 0.5,
                "estimated_seconds": 1
            },
            {
                "name": "📈 Loading fundamentals",
                "func": lambda: self.components["fetcher"].get_fundamentals(ticker),
                "key": "fundamentals",
                "weight": 1.0,
                "estimated_seconds": 3
            }
        ]
        
        # Add optional tasks based on mode
        if should_fetch_institutional():
            tasks.append({
                "name": "🏛️ Fetching institutional holdings",
                "func": lambda: self.components["fetcher"].get_institutional_data(ticker),
                "key": "institutional",
                "weight": 1.0,
                "estimated_seconds": 8
            })
        
        if should_fetch_options():
            tasks.append({
                "name": "📉 Loading options chain",
                "func": lambda: self.components["fetcher"].get_options_chain(ticker),
                "key": "options",
                "weight": 2.0,
                "estimated_seconds": 15
            })
        
        if should_fetch_sentiment():
            tasks.append({
                "name": "💬 Scraping sentiment data",
                "func": lambda: {
                    "stocktwits": self.components["sentiment"].get_stocktwits_sentiment(ticker),
                    "news": self.components["sentiment"].get_news_sentiment(ticker)
                },
                "key": "sentiment",
                "weight": 2.5,
                "estimated_seconds": 30
            })
        else:
            # Fast mode - cached sentiment only
            tasks.append({
                "name": "💬 Loading cached sentiment",
                "func": lambda: {
                    "stocktwits": {"cached": True},
                    "news": []
                },
                "key": "sentiment",
                "weight": 0.3,
                "estimated_seconds": 1
            })
        
        # Execute progressive loading
        start_time = time.time()
        results = progressive_load(tasks, show_time=True)
        elapsed = time.time() - start_time
        
        # Add metadata
        results["ticker"] = ticker
        results["timestamp"] = time.strftime("%Y-%m-%d %I:%M:%S %p")
        results["fetch_time"] = f"{elapsed:.2f}s"
        results["mode"] = mode.name
        
        # Show success message
        st.success(f"✅ Data loaded in {elapsed:.1f}s ({mode.name})", icon="✅")
        
        return results


# ============================================================================
# CHART LOADING HELPERS
# ============================================================================

def load_chart_with_skeleton(
    chart_func: Callable[[], None],
    height: int = 400,
    show_spinner: bool = False
):
    """Load chart with skeleton placeholder"""
    placeholder = st.empty()
    
    with placeholder.container():
        show_skeleton_chart(height)
    
    # Load actual chart
    try:
        if show_spinner:
            with st.spinner("Loading chart..."):
                chart_func()
        else:
            chart_func()
        
        placeholder.empty()
    
    except Exception as e:
        placeholder.empty()
        st.error(f"❌ Error loading chart: {e}")
        logger.error(f"Chart loading error: {e}", exc_info=True)


def load_table_with_skeleton(
    table_func: Callable[[], None],
    rows: int = 5,
    columns: int = 4
):
    """Load table with skeleton placeholder"""
    placeholder = st.empty()
    
    with placeholder.container():
        show_skeleton_table(rows, columns)
    
    # Load actual table
    try:
        table_func()
        placeholder.empty()
    
    except Exception as e:
        placeholder.empty()
        st.error(f"❌ Error loading table: {e}")
        logger.error(f"Table loading error: {e}", exc_info=True)


# ============================================================================
# PREFETCHING & BACKGROUND LOADING
# ============================================================================

def prefetch_data(ticker: str, components: Dict):
    """
    Prefetch data in background (future enhancement with threading).
    Currently returns None. To be implemented with concurrent.futures.
    """
    logger.info(f"Prefetch requested for {ticker} (not yet implemented)")
    return None


# ============================================================================
# LOADING STATE MANAGER
# ============================================================================

class LoadingStateManager:
    """Manages loading states across multiple components"""
    
    def __init__(self):
        if "loading_states" not in st.session_state:
            st.session_state.loading_states = {}
    
    def set_loading(self, key: str, message: str = "Loading..."):
        """Set a component to loading state"""
        st.session_state.loading_states[key] = {
            "loading": True,
            "message": message,
            "start_time": time.time()
        }
    
    def set_loaded(self, key: str):
        """Mark a component as loaded"""
        if key in st.session_state.loading_states:
            elapsed = time.time() - st.session_state.loading_states[key]["start_time"]
            st.session_state.loading_states[key] = {
                "loading": False,
                "elapsed": elapsed
            }
    
    def is_loading(self, key: str) -> bool:
        """Check if a component is loading"""
        return st.session_state.loading_states.get(key, {}).get("loading", False)
    
    def get_message(self, key: str) -> str:
        """Get loading message for a component"""
        return st.session_state.loading_states.get(key, {}).get("message", "Loading...")
    
    def clear(self, key: str = None):
        """Clear loading state(s)"""
        if key:
            st.session_state.loading_states.pop(key, None)
        else:
            st.session_state.loading_states = {}


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "ProgressStep",
    "ProgressTracker",
    "show_progress",
    "show_skeleton_chart",
    "show_skeleton_table",
    "show_skeleton_metric",
    "show_skeleton_card",
    "async_load_with_placeholder",
    "progressive_load",
    "spinner_with_timer",
    "ProgressiveDataFetcher",
    "load_chart_with_skeleton",
    "load_table_with_skeleton",
    "prefetch_data",
    "LoadingStateManager"
]
