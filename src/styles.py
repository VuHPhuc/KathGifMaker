# styles.py

QSS_STYLE = """
/* ===== GLOBAL BASE ===== */
QWidget {
    background-color: #080d1a;
    color: #e2e8f0;
    font-family: "Segoe UI Variable", "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}

/* ===== MAIN WINDOW ===== */
QMainWindow {
    background-color: #080d1a;
}

/* ===== TITLE BAR AREA ===== */
#appTitleBar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0f1729, stop:0.5 #12193a, stop:1 #0f1729);
    border-bottom: 1px solid #1e3a5f;
    border-radius: 0px;
    padding: 0px 16px;
    min-height: 52px;
    max-height: 52px;
}

#appTitleLabel {
    font-size: 18px;
    font-weight: 700;
    color: #f0f4ff;
    letter-spacing: 0.5px;
}

#appSubtitleLabel {
    font-size: 11px;
    color: #6b8cbf;
    letter-spacing: 1.2px;
    font-weight: 500;
}

#appVersionBadge {
    background-color: rgba(99, 102, 241, 0.25);
    border: 1px solid rgba(99, 102, 241, 0.5);
    border-radius: 10px;
    color: #a5b4fc;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    letter-spacing: 0.5px;
}

/* ===== SPLITTER ===== */
QSplitter::handle {
    background-color: #1e2d4a;
    width: 1px;
    margin: 4px 0px;
}

QSplitter::handle:hover {
    background-color: #3b4f7a;
}

/* ===== SIDE / RIGHT PANELS ===== */
#sidebarPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0f1929, stop:1 #0b1322);
    border: 1px solid #1a2d4a;
    border-radius: 16px;
}

#rightPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0f1929, stop:1 #0b1322);
    border: 1px solid #1a2d4a;
    border-radius: 16px;
}

/* ===== CENTER PANEL ===== */
#centerPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0c1524, stop:1 #09101e);
    border: 1px solid #1a2d4a;
    border-radius: 16px;
}

#centerPanel[dragOver="true"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #053d2d, stop:1 #032318);
    border: 2px dashed #10b981;
    border-radius: 16px;
}

/* ===== PANEL HEADER ===== */
QLabel#panelHeader {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    padding: 4px 0px 8px 2px;
    border-bottom: 1px solid #1a2d4a;
    margin-bottom: 4px;
    letter-spacing: 1.5px;
}

/* ===== DEFAULT PUSH BUTTONS ===== */
QPushButton {
    background-color: #162032;
    border: 1px solid #253d5e;
    border-radius: 10px;
    padding: 8px 16px;
    color: #cbd5e1;
    font-weight: 600;
    font-size: 12px;
    letter-spacing: 0.2px;
}

QPushButton:hover {
    background-color: #1e3050;
    border-color: #3b5c8a;
    color: #e2e8f0;
}

QPushButton:pressed {
    background-color: #0f1e33;
    border-color: #2a4468;
    color: #94a3b8;
}

QPushButton:disabled {
    background-color: #0c1624;
    color: #2d4060;
    border-color: #152030;
}

/* ===== PRIMARY BUTTON (Load, Extract) ===== */
QPushButton#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #6366f1);
    color: #ffffff;
    border: 1px solid #4f46e5;
    border-radius: 10px;
    padding: 9px 18px;
    font-weight: 700;
    font-size: 13px;
}

QPushButton#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4338ca, stop:1 #5254eb);
    border-color: #4338ca;
}

QPushButton#primaryButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3730a3, stop:1 #4044d4);
    border-color: #312e81;
}

QPushButton#primaryButton:disabled {
    background: #162032;
    color: #2d4060;
    border-color: #152030;
}

/* ===== EXPORT BUTTON (special green gradient) ===== */
QPushButton#exportButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #059669, stop:1 #10b981);
    color: #ffffff;
    border: 1px solid #059669;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 800;
    font-size: 14px;
    letter-spacing: 0.3px;
    min-height: 44px;
}

QPushButton#exportButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #047857, stop:1 #059669);
    border-color: #047857;
}

QPushButton#exportButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #065f46, stop:1 #047857);
}

QPushButton#exportButton:disabled {
    background: #162032;
    color: #2d4060;
    border-color: #152030;
    font-size: 13px;
    min-height: 44px;
    border-radius: 12px;
}

/* ===== ACCENT BUTTON (Sky Blue) ===== */
QPushButton#accentButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0284c7, stop:1 #0ea5e9);
    color: #ffffff;
    border: 1px solid #0284c7;
    border-radius: 10px;
}

QPushButton#accentButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0369a1, stop:1 #0284c7);
    border-color: #0369a1;
}

QPushButton#accentButton:pressed {
    background: #075985;
    border-color: #075985;
}

/* ===== ICON-ONLY CONTROL BUTTONS (Prev/Next) ===== */
QPushButton#iconButton {
    background-color: #162032;
    border: 1px solid #253d5e;
    border-radius: 10px;
    padding: 6px;
    color: #94a3b8;
}

QPushButton#iconButton:hover {
    background-color: #1e3050;
    border-color: #6366f1;
    color: #a5b4fc;
}

QPushButton#iconButton:pressed {
    background-color: #0f1e33;
}

/* ===== PLAY BUTTON ===== */
QPushButton#playButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #6366f1);
    color: #ffffff;
    border: 1px solid #4f46e5;
    border-radius: 10px;
    padding: 8px 16px;
    font-weight: 700;
}

QPushButton#playButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4338ca, stop:1 #5254eb);
    border-color: #4338ca;
}

QPushButton#playButton:pressed {
    background: #3730a3;
}

/* ===== TEXT INPUTS / SPINBOXES / COMBOBOXES ===== */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #0c1624;
    border: 1px solid #1e3050;
    border-radius: 8px;
    padding: 7px 12px;
    color: #e2e8f0;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #6366f1;
    background-color: #0f1e33;
}

QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {
    border-color: #2a4468;
}

/* ===== COMBOBOX ===== */
QComboBox {
    padding-right: 30px;
    border-radius: 8px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 1px solid #1e3050;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background-color: #0f1e33;
}

QComboBox::down-arrow {
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='rgb(99,102,241)' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
    width: 14px;
    height: 14px;
}

QComboBox::drop-down:hover {
    background-color: #162032;
}

QComboBox QAbstractItemView {
    background-color: #0f1929;
    border: 1px solid #253d5e;
    border-radius: 8px;
    selection-background-color: #1e3050;
    selection-color: #a5b4fc;
    outline: none;
    padding: 4px;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 6px;
    min-height: 28px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #162032;
}

/* ===== SPINBOX BUTTONS ===== */
QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid #1e3050;
    border-top-right-radius: 8px;
    background-color: #0f1929;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 22px;
    border-left: 1px solid #1e3050;
    border-bottom-right-radius: 8px;
    background-color: #0f1929;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #162032;
}

QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed,
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {
    background-color: #0c1624;
}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='rgb(99,102,241)' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='18 15 12 9 6 15'></polyline></svg>");
    width: 10px;
    height: 10px;
}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='rgb(99,102,241)' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
    width: 10px;
    height: 10px;
}

/* ===== GROUP BOXES ===== */
QGroupBox {
    background-color: #0c1624;
    border: 1px solid #1a2d4a;
    border-radius: 12px;
    margin-top: 14px;
    padding-top: 8px;
    font-weight: 700;
    font-size: 12px;
    color: #7c8cc5;
    letter-spacing: 0.5px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 10px;
    left: 12px;
    background-color: #0f1929;
    border: 1px solid #1a2d4a;
    border-radius: 8px;
    color: #818cf8;
}

/* ===== CHECKBOXES ===== */
QCheckBox, QRadioButton {
    spacing: 8px;
    color: #94a3b8;
    font-size: 12px;
}

QCheckBox:hover, QRadioButton:hover {
    color: #cbd5e1;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1.5px solid #2a4468;
    background-color: #0c1624;
}

QCheckBox::indicator:hover {
    border-color: #6366f1;
    background-color: rgba(99, 102, 241, 0.1);
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #059669, stop:1 #10b981);
    border: 2px solid #059669;
    border-radius: 5px;
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 9 17 4 12'></polyline></svg>");
}

/* ===== RADIO BUTTONS ===== */
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 1.5px solid #2a4468;
    background-color: #0c1624;
}

QRadioButton::indicator:hover {
    border-color: #6366f1;
}

QRadioButton::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #4f46e5, stop:1 #6366f1);
    border: 3px solid #0c1624;
    outline: 2px solid #6366f1;
    border-radius: 8px;
}

/* ===== SCROLLBARS ===== */
QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    margin: 2px 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #1e3050;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #2a4468;
}

QScrollBar::handle:vertical:pressed {
    background-color: #6366f1;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #1e3050;
    min-width: 24px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #2a4468;
}

QScrollBar::handle:horizontal:pressed {
    background-color: #6366f1;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
}

/* ===== LIST WIDGET (Frame Cards) ===== */
QListWidget {
    background-color: #080d1a;
    border: 1px solid #1a2d4a;
    border-radius: 12px;
    padding: 6px;
    outline: none;
}

QListWidget::item {
    border-radius: 10px;
    padding: 3px;
    margin-bottom: 5px;
    background-color: #0f1929;
    border: 1px solid #1a2d4a;
}

QListWidget::item:hover {
    background-color: #122030;
    border-color: #2a4468;
}

QListWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a1557, stop:1 #1e1e5a);
    border: 1px solid #4f46e5;
    border-radius: 10px;
}

/* ===== PROGRESS BAR ===== */
QProgressBar {
    border: 1px solid #1e3050;
    border-radius: 8px;
    text-align: center;
    background-color: #0c1624;
    color: #a5b4fc;
    font-weight: 700;
    font-size: 11px;
    min-height: 18px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #10b981);
    border-radius: 7px;
}

/* ===== TIMELINE SLIDER ===== */
QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background: #0f1929;
    margin: 0px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #818cf8, stop:1 #6366f1);
    border: 2px solid #0c1624;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #a5b4fc, stop:1 #818cf8);
    border-color: #6366f1;
}

QSlider::handle:horizontal:pressed {
    background: #4f46e5;
    border-color: #312e81;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #818cf8);
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #1a2d4a;
    border-radius: 3px;
}

/* ===== TOOLTIPS ===== */
QToolTip {
    background-color: #0f1929;
    color: #e2e8f0;
    border: 1px solid #253d5e;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 500;
}

/* ===== STATUS BAR ===== */
#statusBar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0b1322, stop:1 #0f1929);
    border-top: 1px solid #1a2d4a;
    padding: 4px 16px;
    min-height: 30px;
    max-height: 30px;
    border-radius: 0px;
}

#statusLabel {
    color: #4a6a9a;
    font-size: 11px;
    font-weight: 500;
}

/* ===== FRAME COUNT BADGE ===== */
#frameCountBadge {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(99, 102, 241, 0.2), stop:1 rgba(99, 102, 241, 0.1));
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 10px;
    color: #818cf8;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    letter-spacing: 0.3px;
}

/* ===== INFO LABEL (meta info) ===== */
#infoBox {
    background-color: rgba(12, 22, 36, 0.7);
    border: 1px solid #1a2d4a;
    border-radius: 10px;
    padding: 8px 12px;
}

/* ===== DRAG DROP HINT LABEL ===== */
#dropHintLabel {
    color: #2a4468;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.3px;
}

/* ===== MESSAGE BOXES ===== */
QMessageBox {
    background-color: #0f1929;
}

QMessageBox QPushButton {
    min-width: 80px;
    min-height: 32px;
    border-radius: 8px;
}
"""
