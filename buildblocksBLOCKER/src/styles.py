GAME_STYLE = """
/* Main Window */
QMainWindow {
    background-color: #0A1428;
    background-image: url('assets/background.png');
    color: #C8AA6E;
}

/* Buttons */
QPushButton {
    background-color: #1E2328;
    color: #C8AA6E;
    border: 2px solid #463714;
    border-radius: 3px;
    padding: 8px 20px;
    font-size: 14px;
    font-weight: bold;
    min-width: 120px;
    text-transform: uppercase;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #2F3B46, stop:0.5 #1E2328, stop:1 #1A1F24);
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #3F4B56, stop:0.5 #2E3338, stop:1 #2A2F34);
    border: 2px solid #C8AA6E;
    color: #F0E6D2;
}

QPushButton:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #006F92, stop:0.5 #005A82, stop:1 #004A72);
    border: 2px solid #0AC8B9;
    color: #0AC8B9;
}

/* List Widget */
QListWidget {
    background-color: rgba(30, 35, 40, 0.95);
    border: 2px solid #463714;
    border-radius: 5px;
    color: #A09B8C;
    padding: 5px;
    font-size: 13px;
}

QListWidget::item {
    padding: 8px;
    margin: 2px;
    border: 1px solid #463714;
    border-radius: 3px;
    background: rgba(0, 0, 0, 0.2);
}

QListWidget::item:hover {
    background: rgba(200, 170, 110, 0.1);
    border: 1px solid #C8AA6E;
}

QListWidget::item:selected {
    background: rgba(0, 90, 130, 0.5);
    border: 1px solid #0AC8B9;
    color: #0AC8B9;
}

/* Labels */
QLabel {
    color: #A09B8C;
    font-size: 14px;
    font-weight: bold;
}

/* Checkboxes */
QCheckBox {
    color: #C8AA6E;
    spacing: 8px;
    font-size: 13px;
    font-weight: bold;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #463714;
    border-radius: 3px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #2F3B46, stop:0.5 #1E2328, stop:1 #1A1F24);
}

QCheckBox::indicator:hover {
    border: 2px solid #C8AA6E;
    background: rgba(200, 170, 110, 0.1);
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #006F92, stop:0.5 #005A82, stop:1 #004A72);
    border: 2px solid #0AC8B9;
}

/* Header Sections */
.HeaderSection {
    background-color: rgba(30, 35, 40, 0.95);
    border: 2px solid #463714;
    border-radius: 8px;
    margin: 8px;
    padding: 15px;
}

.HeaderSection:hover {
    border: 2px solid #785A28;
    background-color: rgba(30, 35, 40, 0.98);
}

/* Group Headers */
.GroupHeader {
    color: #F0E6D2;
    font-size: 18px;
    font-weight: bold;
    border-bottom: 2px solid #785A28;
    padding: 5px 0 10px 0;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Time Edit Controls */
QTimeEdit {
    background-color: #1E2328;
    border: 2px solid #463714;
    border-radius: 3px;
    color: #C8AA6E;
    padding: 5px;
    min-width: 100px;
}

QTimeEdit::up-button, QTimeEdit::down-button {
    background-color: #2F3B46;
    border: 1px solid #463714;
    border-radius: 2px;
}

QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
    background-color: #3F4B56;
    border: 1px solid #C8AA6E;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #1E2328;
    width: 12px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #463714;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #785A28;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Dialog Windows */
QDialog {
    background-color: #0A1428;
    border: 2px solid #463714;
    border-radius: 8px;
}

/* Menu */
QMenu {
    background-color: #1E2328;
    border: 2px solid #463714;
    border-radius: 5px;
    padding: 5px;
}

QMenu::item {
    padding: 8px 25px;
    color: #C8AA6E;
    border-radius: 3px;
}

QMenu::item:selected {
    background-color: rgba(200, 170, 110, 0.1);
    border: 1px solid #C8AA6E;
}

QMenu::separator {
    height: 1px;
    background-color: #463714;
    margin: 5px 0;
}

/* Tooltips */
QToolTip {
    background-color: #1E2328;
    color: #C8AA6E;
    border: 1px solid #463714;
    border-radius: 3px;
    padding: 5px;
}

/* Game Button */
#GameButton {
    color: #C8AA6E;
    background-color: #1E2328;
    border: 2px solid #463714;
    border-radius: 3px;
    padding: 8px 20px 8px 40px;  /* Extra left padding for icon */
    font-size: 14px;
    font-weight: bold;
    text-align: left;
    min-width: 160px;
}

#GameButton:hover {
    background-color: #2F3B46;
    border-color: #785A28;
    color: #F0E6D2;
}

#GameButton:checked {
    background-color: #005A82;
    border-color: #0AC8B9;
    color: #0AC8B9;
}

/* Time Display */
#TimeDisplay {
    color: #C8AA6E;
    font-size: 18px;
    font-weight: bold;
    padding: 5px;
    background-color: rgba(30, 35, 40, 0.9);
    border: 1px solid #463714;
    border-radius: 3px;
}
""" 