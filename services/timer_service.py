from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class TimerService(QObject):
    # Señales para comunicar a la UI que algo ocurrió
    time_updated = pyqtSignal()
    phase_ended = pyqtSignal()
    session_ended = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timeout)

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def _on_timeout(self):
        if self.model.is_paused:
            return

        self.model.total_seconds_left -= 1
        self.model.current_seconds_left -= 1
        
        self.time_updated.emit()

        if self.model.total_seconds_left <= 0:
            self.session_ended.emit()
            return

        if self.model.current_seconds_left <= 0:
            self.phase_ended.emit()

    def add_minutes(self, minutes):
        self.model.current_seconds_left += minutes * 60
        self.model.total_seconds_left += minutes * 60
        self.time_updated.emit()

    def subtract_minutes(self, minutes):
        seconds = minutes * 60
        if self.model.current_seconds_left > seconds:
            self.model.current_seconds_left -= seconds
            if self.model.total_seconds_left > seconds:
                self.model.total_seconds_left -= seconds
            else:
                self.model.total_seconds_left = 0
            self.time_updated.emit()
        else:
            self.model.total_seconds_left -= self.model.current_seconds_left
            if self.model.total_seconds_left < 0: 
                self.model.total_seconds_left = 0
            self.model.current_seconds_left = 0
            self.time_updated.emit()
            
            if self.model.total_seconds_left <= 0:
                self.session_ended.emit()
            else:
                self.phase_ended.emit()