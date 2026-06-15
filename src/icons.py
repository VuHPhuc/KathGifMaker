# icons.py
try:
    from PySide6.QtSvg import QSvgRenderer
    HAS_SVG = True
except (ImportError, ModuleNotFoundError):
    HAS_SVG = False

from PySide6.QtGui import QPainter, QIcon, QPixmap
from PySide6.QtCore import QSize, Qt

# SVG Vector Icon Definitions (Lucide Icons)
VIDEO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m22 8-6 4 6 4V8Z"/>
  <rect width="14" height="12" x="2" y="6" rx="2" ry="2"/>
</svg>
"""

SCISSORS_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="6" cy="6" r="3"/>
  <circle cx="6" cy="18" r="3"/>
  <line x1="9.8" y1="8.2" x2="21" y2="19.4"/>
  <line x1="21" y1="4.6" x2="11.5" y2="14.1"/>
</svg>
"""

SETTINGS_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="3"/>
  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
</svg>
"""

EXPORT_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="17 8 12 3 7 8"/>
  <line x1="12" y1="3" x2="12" y2="15"/>
</svg>
"""

TRASH_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 6h18"/>
  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
  <line x1="10" y1="11" x2="10" y2="17"/>
  <line x1="14" y1="11" x2="14" y2="17"/>
</svg>
"""

PLAY_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="6 3 20 12 6 21 6 3" fill="currentColor"/>
</svg>
"""

PAUSE_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="14" y="4" width="4" height="16" rx="1" fill="currentColor"/>
  <rect x="6" y="4" width="4" height="16" rx="1" fill="currentColor"/>
</svg>
"""

PREV_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="19 20 9 12 19 4 19 20" fill="currentColor"/>
  <line x1="5" y1="19" x2="5" y2="5"/>
</svg>
"""

NEXT_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="5 4 15 12 5 20 5 4" fill="currentColor"/>
  <line x1="19" y1="5" x2="19" y2="19"/>
</svg>
"""

CHECK_ALL_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/>
  <path d="m9 12 2 2 4-4"/>
</svg>
"""

UNCHECK_ALL_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="15" y1="9" x2="9" y2="15"/>
</svg>
"""

# Map to store SVG strings
_SVG_MAP = {
    "video": VIDEO_SVG,
    "scissors": SCISSORS_SVG,
    "settings": SETTINGS_SVG,
    "export": EXPORT_SVG,
    "trash": TRASH_SVG,
    "play": PLAY_SVG,
    "pause": PAUSE_SVG,
    "prev": PREV_SVG,
    "next": NEXT_SVG,
    "check_all": CHECK_ALL_SVG,
    "uncheck_all": UNCHECK_ALL_SVG,
}

def get_svg_icon(name: str, size: QSize = QSize(20, 20), color: str = "#4f46e5") -> QIcon:
    """Generate a high-quality QIcon from a registered SVG string with the specified color and size."""
    if not HAS_SVG:
        return QIcon()
        
    svg_content = _SVG_MAP.get(name)
    if not svg_content:
        return QIcon()
    
    # Inject the chosen color into the SVG stroke and fill color references
    colored_svg = svg_content.replace('currentColor', color)
    
    # Initialize the SVG renderer
    renderer = QSvgRenderer(colored_svg.encode('utf-8'))
    
    # Render onto a transparent pixmap
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    
    # Enable anti-aliasing and smooth pixmap transformation during rendering
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)
