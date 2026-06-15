# styles.py

QSS_STYLE = """
/* Global Styles */
QWidget {
    background-color: #f8fafc; /* Slate 50 - clean light background */
    color: #0f172a; /* Slate 900 - high contrast dark text */
    font-family: "Segoe UI", "Segoe UI Semibold", "Inter", sans-serif;
    font-size: 13px;
}

/* Sidebar and Main Panels */
#sidebarPanel, #rightPanel {
    background-color: #ffffff; /* pure white cards */
    border: 1px solid #e2e8f0; /* Slate 200 border */
    border-radius: 12px;
}

#centerPanel {
    background-color: #ffffff; /* pure white card */
    border: 1px solid #e2e8f0; /* Slate 200 border */
    border-radius: 12px;
}

/* Drag Over Animation Highlight */
#centerPanel[dragOver="true"] {
    background-color: #f0fdf4; /* Soft Emerald 50 green background */
    border: 2px dashed #22c55e; /* Emerald 500 dashed border */
}

/* Title / Header Labels */
QLabel#panelHeader {
    font-size: 15px;
    font-weight: bold;
    color: #4f46e5; /* Indigo 600 accent */
    padding: 6px 0px;
    border-bottom: 2px solid #f1f5f9; /* Slate 100 divider */
    margin-bottom: 8px;
}

/* Push Buttons */
QPushButton {
    background-color: #f1f5f9; /* Slate 100 */
    border: 1px solid #cbd5e1; /* Slate 300 */
    border-radius: 8px;
    padding: 8px 16px;
    color: #334155; /* Slate 700 */
    font-weight: 600;
}

QPushButton:hover {
    background-color: #e2e8f0; /* Slate 200 */
    border-color: #94a3b8; /* Slate 400 */
    color: #0f172a;
}

QPushButton:pressed {
    background-color: #cbd5e1; /* Slate 300 */
}

QPushButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}

/* Primary Highlighted Action Buttons (e.g. Load, Extract, Export) */
QPushButton#primaryButton {
    background-color: #4f46e5; /* Indigo 600 */
    color: #ffffff;
    border: 1px solid #4f46e5;
}

QPushButton#primaryButton:hover {
    background-color: #4338ca; /* Indigo 700 */
    border-color: #4338ca;
}

QPushButton#primaryButton:pressed {
    background-color: #3730a3; /* Indigo 800 */
}

QPushButton#primaryButton:disabled {
    background-color: #f1f5f9;
    color: #94a3b8;
    border-color: #cbd5e1;
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
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 10px;
    color: #0f172a;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #4f46e5;
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
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='rgb(79,70,229)' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    selection-background-color: #eef2ff;
    selection-color: #4f46e5;
    outline: none;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #cbd5e1;
    border-top-right-radius: 6px;
    background-color: #f8fafc;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    border-left: 1px solid #cbd5e1;
    border-bottom-right-radius: 6px;
    background-color: #f8fafc;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #e2e8f0;
}

/* Labels and GroupBoxes */
QGroupBox {
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    margin-top: 1.5ex;
    font-weight: bold;
    color: #4f46e5;
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
    color: #334155;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #cbd5e1;
    background-color: #ffffff;
}

QCheckBox::indicator:hover {
    border-color: #4f46e5;
}

QCheckBox::indicator:checked {
    background-color: #10b981; /* Emerald Green */
    border: 3px solid #ffffff;
    border-radius: 4px;
    outline: 1px solid #10b981;
}

/* ScrollBars */
QScrollBar:vertical {
    background-color: #f8fafc;
    width: 10px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #cbd5e1;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #f8fafc;
    height: 10px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #cbd5e1;
    min-width: 20px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #94a3b8;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ListWidget and Frame Cards */
QListWidget {
    background-color: #f1f5f9; /* Slate 100 inner container */
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 5px;
}

QListWidget::item {
    border-radius: 6px;
    padding: 2px;
    margin-bottom: 4px;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
}

QListWidget::item:hover {
    background-color: #f8fafc;
    border-color: #cbd5e1;
}

QListWidget::item:selected {
    background-color: #eef2ff; /* soft purple/blue */
    color: #4f46e5;
    border: 1px solid #818cf8;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    text-align: center;
    background-color: #f1f5f9;
    color: #334155;
    font-weight: bold;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #0ea5e9);
    border-radius: 5px;
}

/* Custom Sliders */
QSlider::groove:horizontal {
    border: 1px solid #cbd5e1;
    height: 6px;
    background: #f1f5f9;
    margin: 2px 0;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #4f46e5;
    border: 1px solid #818cf8;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #4338ca;
    border-color: #4338ca;
}

QSlider::sub-page:horizontal {
    background: #4f46e5;
    border-radius: 3px;
}
"""
