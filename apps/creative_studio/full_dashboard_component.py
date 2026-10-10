"""Register the component from an importable module for Streamlit multipage apps."""
from pathlib import Path
from streamlit.components.v1 import declare_component


def render_dashboard(snapshot: Path, height: int = 850) -> None:
    component = declare_component("cfa_full_visual_library", path=str(snapshot))
    component(height=height, key="cfa-full-visual-library", default=None)
