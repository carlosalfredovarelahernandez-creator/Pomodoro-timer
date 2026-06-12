MAIN_STYLE = """
    QMainWindow { background-color: #1e1e24; }
    QLabel { color: #f4f4f9; font-family: 'Segoe UI', Arial, sans-serif; }
    QPushButton { 
        background-color: #2a2a35; 
        color: #f4f4f9; 
        border: 1px solid #444454; 
        border-radius: 6px; 
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover { background-color: #3f3f52; border-color: #ff5964; }
    QPushButton:pressed { background-color: #1e1e24; }
    
    /* Estilo para los botones de la barra superior */
    QPushButton#TopBarBtn {
        background-color: transparent;
        border: none;
        color: #a5a5b5;
        padding: 5px;
        font-size: 13px;
    }
    QPushButton#TopBarBtn:hover { color: #ff5964; background-color: #2a2a35; }
    QPushButton#TopBarBtn::menu-indicator { image: none; }
    
    /* Menú desplegable */
    QMenu {
        background-color: #2a2a35;
        color: #f4f4f9;
        border: 1px solid #444454;
        border-radius: 4px;
        font-size: 14px;
        padding: 5px;
    }
    QMenu::item { padding: 8px 25px; border-radius: 4px; }
    QMenu::item:selected { background-color: #ff5964; color: white; }
    
    QSpinBox { 
        background-color: #2a2a35; 
        color: #f4f4f9; 
        border: 1px solid #444454; 
        border-radius: 4px; 
        padding: 5px; 
        font-size: 14px;
    }
    QGroupBox { 
        color: #ff5964; 
        border: 2px solid #444454; 
        border-radius: 8px; 
        margin-top: 15px; 
        font-weight: bold;
        font-size: 14px;
    }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
    QRadioButton { color: #f4f4f9; font-size: 14px; padding: 5px; }
"""