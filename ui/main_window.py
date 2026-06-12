from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QRadioButton, QSpinBox, 
                             QStackedWidget, QMessageBox, QStyle, QGroupBox, 
                             QFormLayout, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from models.pomodoro_model import PomodoroModel
from services.timer_service import TimerService
from utils.styles import MAIN_STYLE

class PomodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(420, 560)
        self.setStyleSheet(MAIN_STYLE)

        # Inicialización de Arquitectura
        self.model = PomodoroModel()
        self.service = TimerService(self.model)

        # Conectar señales del servicio a la UI
        self.service.time_updated.connect(self.update_ui_labels)
        self.service.phase_ended.connect(self.handle_phase_end)
        self.service.session_ended.connect(self.handle_session_end)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.init_config_ui()
        self.init_timer_ui()

    def init_config_ui(self):
        config_widget = QWidget()
        layout = QVBoxLayout(config_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        title_label = QLabel("Pomodoro Timer")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #ff5964; margin-bottom: 10px;")
        layout.addWidget(title_label)

        self.mode_group = QGroupBox("Selecciona el Modo")
        mode_layout = QVBoxLayout()
        
        self.radio_default = QRadioButton("Predeterminado (25m Trab. / 10m Desc.)")
        self.radio_default.setChecked(True)
        self.radio_default.toggled.connect(self.toggle_mode_views)
        
        self.radio_custom = QRadioButton("Personalizado")
        self.radio_custom.toggled.connect(self.toggle_mode_views)
        
        mode_layout.addWidget(self.radio_default)
        mode_layout.addWidget(self.radio_custom)
        self.mode_group.setLayout(mode_layout)
        layout.addWidget(self.mode_group)

        self.custom_group = QGroupBox("Tiempos Personalizados")
        custom_layout = QFormLayout()
        
        self.spin_work = QSpinBox()
        self.spin_work.setRange(1, 120)
        self.spin_work.setValue(25)
        self.spin_work.valueChanged.connect(self.adjust_total_time)
        
        self.spin_break = QSpinBox()
        self.spin_break.setRange(1, 120)
        self.spin_break.setValue(10)
        self.spin_break.valueChanged.connect(self.adjust_total_time)
        
        custom_layout.addRow(QLabel("Tiempo de Trabajo (min):"), self.spin_work)
        custom_layout.addRow(QLabel("Tiempo de Descanso (min):"), self.spin_break)
        self.custom_group.setLayout(custom_layout)
        self.custom_group.setEnabled(False) 
        layout.addWidget(self.custom_group)

        self.session_group = QGroupBox("Duración Total de la Sesión")
        session_layout = QFormLayout()
        
        self.spin_total_time = QSpinBox()
        self.spin_total_time.setRange(35, 600) 
        self.spin_total_time.setValue(35)
        
        session_layout.addRow(QLabel("Tiempo Total (minutos):"), self.spin_total_time)
        self.session_group.setLayout(session_layout)
        layout.addWidget(self.session_group)

        self.btn_start = QPushButton("INICIAR TEMPORIZADOR")
        self.btn_start.setStyleSheet("""
            QPushButton { 
                background-color: #ff5964; 
                color: white; 
                font-size: 16px; 
                padding: 12px; 
                border: none;
            }
            QPushButton:hover { background-color: #ff737d; }
        """)
        self.btn_start.clicked.connect(self.start_pomodoro)
        layout.addWidget(self.btn_start)

        self.stacked_widget.addWidget(config_widget)
        self.adjust_total_time()

    def init_timer_ui(self):
        timer_widget = QWidget()
        layout = QVBoxLayout(timer_widget)
        layout.setContentsMargins(25, 15, 25, 40)
        layout.setSpacing(20)

        top_bar_layout = QHBoxLayout()
        self.btn_back = QPushButton("⬅ Volver al Inicio")
        self.btn_back.setObjectName("TopBarBtn")
        self.btn_back.clicked.connect(self.reset_to_config)
        
        self.btn_menu = QPushButton("⚙️ Opciones")
        self.btn_menu.setObjectName("TopBarBtn")
        
        self.menu_options = QMenu(self)
        action_restart = self.menu_options.addAction("🔄 Reiniciar Sesión")
        action_finish = self.menu_options.addAction("❌ Finalizar Sesión")
        
        action_restart.triggered.connect(self.restart_session)
        action_finish.triggered.connect(self.reset_to_config)
        self.btn_menu.setMenu(self.menu_options)

        top_bar_layout.addWidget(self.btn_back)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.btn_menu)
        layout.addLayout(top_bar_layout)

        layout.addStretch()

        self.lbl_phase = QLabel("TRABAJANDO")
        self.lbl_phase.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.lbl_phase.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_phase)

        self.lbl_time = QLabel("25:00")
        self.lbl_time.setFont(QFont("Segoe UI", 56, QFont.Bold))
        self.lbl_time.setAlignment(Qt.AlignCenter)
        self.lbl_time.setStyleSheet("color: #f4f4f9; margin: 10px 0;")
        layout.addWidget(self.lbl_time)

        self.lbl_total_remaining = QLabel("Tiempo Total Restante: --:--:--")
        self.lbl_total_remaining.setFont(QFont("Segoe UI", 11))
        self.lbl_total_remaining.setAlignment(Qt.AlignCenter)
        self.lbl_total_remaining.setStyleSheet("color: #a5a5b5;")
        layout.addWidget(self.lbl_total_remaining)

        layout.addStretch()

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        self.btn_minus = QPushButton("-5 Min")
        self.btn_minus.clicked.connect(lambda: self.service.subtract_minutes(5))
        
        self.btn_pause = QPushButton()
        self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.btn_pause.clicked.connect(self.toggle_pause)
        
        self.btn_plus = QPushButton("+5 Min")
        self.btn_plus.clicked.connect(lambda: self.service.add_minutes(5))

        controls_layout.addWidget(self.btn_minus)
        controls_layout.addWidget(self.btn_pause)
        controls_layout.addWidget(self.btn_plus)
        layout.addLayout(controls_layout)

        self.stacked_widget.addWidget(timer_widget)

    def toggle_mode_views(self):
        if self.radio_default.isChecked():
            self.custom_group.setEnabled(False)
        else:
            self.custom_group.setEnabled(True)
        self.adjust_total_time()

    def adjust_total_time(self):
        if self.radio_default.isChecked():
            min_required = 35 
        else:
            min_required = self.spin_work.value() + self.spin_break.value()
        
        self.spin_total_time.setMinimum(min_required)
        if self.spin_total_time.value() < min_required:
            self.spin_total_time.setValue(min_required)

    def start_pomodoro(self):
        if self.radio_custom.isChecked():
            self.model.work_minutes = self.spin_work.value()
            self.model.break_minutes = self.spin_break.value()
        else:
            self.model.work_minutes = 25
            self.model.break_minutes = 10
            
        self.model.total_session_minutes = self.spin_total_time.value()
        self.model.current_seconds_left = self.model.work_minutes * 60
        self.model.total_seconds_left = self.model.total_session_minutes * 60
        
        self.model.current_phase = "Trabajo"
        self.model.is_paused = False
        self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        
        self.update_ui_labels()
        self.stacked_widget.setCurrentIndex(1)
        self.service.start()

    def restart_session(self):
        self.service.stop()
        self.model.current_seconds_left = self.model.work_minutes * 60
        self.model.total_seconds_left = self.model.total_session_minutes * 60
        self.model.current_phase = "Trabajo"
        self.model.is_paused = False
        self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.update_ui_labels()
        self.service.start()

    def update_ui_labels(self):
        mins, secs = divmod(self.model.current_seconds_left, 60)
        self.lbl_time.setText(f"{mins:02d}:{secs:02d}")
        
        tot_hours, remainder = divmod(self.model.total_seconds_left, 3600)
        tot_mins, tot_secs = divmod(remainder, 60)
        self.lbl_total_remaining.setText(f"Tiempo Total Restante: {tot_hours:02d}:{tot_mins:02d}:{tot_secs:02d}")
        
        if self.model.current_phase == "Trabajo":
            self.lbl_phase.setText("TRABAJANDO")
            self.lbl_phase.setStyleSheet("color: #ff5964; letter-spacing: 2px;")
        else:
            self.lbl_phase.setText("DESCANSO")
            self.lbl_phase.setStyleSheet("color: #38b000; letter-spacing: 2px;")

    def handle_phase_end(self):
        self.service.stop() 

        if self.model.current_phase == "Trabajo":
            msg = QMessageBox(self)
            msg.setWindowTitle("¡Bloque Completado!")
            msg.setText("Buen trabajo. Es hora de tomar un descanso.")
            msg.setIcon(QMessageBox.Information)
            # Aquí aplicamos la bandera para forzar que esté siempre encima
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.exec_()
            
            self.model.current_phase = "Descanso"
            self.model.current_seconds_left = self.model.break_minutes * 60
            self.update_ui_labels()
            self.service.start()
        else:
            if self.model.total_session_minutes >= 180:
                msg = QMessageBox(self)
                msg.setWindowTitle("Ciclo Automático")
                msg.setText("El descanso ha finalizado. Iniciando siguiente ciclo de trabajo.")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
                msg.exec_()
                
                self.model.current_phase = "Trabajo"
                self.model.current_seconds_left = self.model.work_minutes * 60
                self.update_ui_labels()
                self.service.start()
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle("Siguiente Ciclo")
                msg.setText("¿Desea continuar trabajando?")
                msg.setIcon(QMessageBox.Question)
                btn_yes = msg.addButton(QMessageBox.Yes)
                btn_no = msg.addButton(QMessageBox.No)
                msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
                msg.exec_()
                
                if msg.clickedButton() == btn_yes:
                    self.model.current_phase = "Trabajo"
                    self.model.current_seconds_left = self.model.work_minutes * 60
                    self.update_ui_labels()
                    self.service.start()
                else:
                    self.reset_to_config()

    def handle_session_end(self):
        self.service.stop()
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Sesión Finalizada")
        msg.setText("¡Felicidades! Has completado el tiempo de tu sesión.\n\n¿Qué deseas hacer ahora?")
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
        
        btn_restart = msg.addButton("🔄 Reiniciar Sesión", QMessageBox.AcceptRole)
        btn_finish = msg.addButton("❌ Finalizar Sesión", QMessageBox.RejectRole)
        
        msg.exec_()
        
        if msg.clickedButton() == btn_restart:
            self.restart_session()
        else:
            self.reset_to_config()

    def toggle_pause(self):
        if self.model.is_paused:
            self.model.is_paused = False
            self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.model.is_paused = True
            self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def reset_to_config(self):
        self.service.stop()
        self.stacked_widget.setCurrentIndex(0)