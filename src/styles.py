# styles.py

QSS_STYLE = """
/* Global Styles */
QWidget {
    background-color: #0f172a; /* Obsidian Slate 900 */
    color: #f8fafc; /* Slate 50 - off-white text */
    font-family: "Segoe UI", "Segoe UI Semibold", "Inter", sans-serif;
    font-size: 13px;
}

/* Sidebar and Main Panels */
#sidebarPanel, #rightPanel {
    background-color: #1e293b; /* Slate 800 cards */
    border: 1px solid #334155; /* Slate 700 border */
    border-radius: 12px;
}

#centerPanel {
    background-color: #1e293b; /* Slate 800 card */
    border: 1px solid #334155; /* Slate 700 border */
    border-radius: 12px;
}

/* Drag Over Animation Highlight */
#centerPanel[dragOver="true"] {
    background-color: #064e3b; /* Soft Forest Green background */
    border: 2px dashed #10b981; /* Emerald 500 dashed border */
}

/* Title / Header Labels */
QLabel#panelHeader {
    font-size: 15px;
    font-weight: bold;
    color: #a78bfa; /* Violet 400 accent */
    padding: 6px 0px;
    border-bottom: 2px solid #334155; /* Slate 700 divider */
    margin-bottom: 8px;
}

/* Push Buttons */
QPushButton {
    background-color: #334155; /* Slate 700 */
    border: 1px solid #475569; /* Slate 600 */
    border-radius: 8px;
    padding: 8px 16px;
    color: #f8fafc; /* Slate 50 */
    font-weight: 600;
}

QPushButton:hover {
    background-color: #475569; /* Slate 600 */
    border-color: #64748b; /* Slate 500 */
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #1e293b; /* Slate 800 */
}

QPushButton:disabled {
    background-color: #0f172a;
    color: #64748b;
    border-color: #1e293b;
}

/* Primary Highlighted Action Buttons (e.g. Load, Extract, Export) */
QPushButton#primaryButton {
    background-color: #6366f1; /* Indigo 500 */
    color: #ffffff;
    border: 1px solid #6366f1;
}

QPushButton#primaryButton:hover {
    background-color: #4f46e5; /* Indigo 600 */
    border-color: #4f46e5;
}

QPushButton#primaryButton:pressed {
    background-color: #3730a3; /* Indigo 800 */
}

QPushButton#primaryButton:disabled {
    background-color: #1e293b;
    color: #64748b;
    border-color: #334155;
}

QPushButton#accentButton {
    background-color: #0ea5e9; /* Sky 500 */
    color: #ffffff;
    border: 1px solid #0ea5e9;
}

QPushButton#accentButton:hover {
    background-color: #0284c7; /* Sky 600 */
    border-color: #0284c7;
}

QPushButton#accentButton:pressed {
    background-color: #0369a1; /* Sky 700 */
}

/* Text Inputs and SpinBoxes */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #0f172a; /* Slate 900 inner */
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    color: #f8fafc;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #6366f1;
}

QComboBox {
    padding-right: 25px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 0px;
}

QComboBox::down-arrow {
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='rgb(129,140,248)' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    selection-background-color: #334155;
    selection-color: #818cf8;
    outline: none;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #334155;
    border-top-right-radius: 6px;
    background-color: #1e293b;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #334155;
    border-bottom-right-radius: 6px;
    background-color: #1e293b;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #334155;
}

/* Labels and GroupBoxes */
QGroupBox {
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 1.5ex;
    font-weight: bold;
    color: #818cf8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    left: 10px;
}

/* Checkboxes and Radio Buttons */
QCheckBox, QRadioButton {
    spacing: 8px;
    color: #cbd5e1;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #475569;
    background-color: #0f172a;
}

QCheckBox::indicator:hover {
    border-color: #818cf8;
}

QCheckBox::indicator:checked {
    background-color: #10b981; /* Emerald Green */
    border: 3px solid #0f172a;
    border-radius: 4px;
    outline: 1px solid #10b981;
}

/* ScrollBars */
QScrollBar:vertical {
    background-color: #0f172a;
    width: 10px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #334155;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #0f172a;
    height: 10px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #334155;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #475569;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ListWidget and Frame Cards */
QListWidget {
    background-color: #0f172a; /* Slate 900 inner container */
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 5px;
}

QListWidget::item {
    border-radius: 6px;
    padding: 2px;
    margin-bottom: 4px;
    background-color: #1e293b;
    border: 1px solid #334155;
}

QListWidget::item:hover {
    background-color: #334155;
    border-color: #475569;
}

QListWidget::item:selected {
    background-color: #312e81; /* soft purple/blue dark */
    color: #c7d2fe;
    border: 1px solid #6366f1;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #334155;
    border-radius: 6px;
    text-align: center;
    background-color: #0f172a;
    color: #f8fafc;
    font-weight: bold;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #0ea5e9);
    border-radius: 5px;
}

/* Custom Sliders */
QSlider::groove:horizontal {
    border: 1px solid #334155;
    height: 6px;
    background: #0f172a;
    margin: 2px 0;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #818cf8;
    border: 1px solid #a5b4fc;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #a5b4fc;
    border-color: #a5b4fc;
}

QSlider::sub-page:horizontal {
    background: #818cf8;
    border-radius: 3px;
}
"""
