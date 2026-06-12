class PomodoroModel:
    def __init__(self):
        # Variables de configuración
        self.work_minutes = 25
        self.break_minutes = 10
        self.total_session_minutes = 35
        
        # Variables de estado actual
        self.current_phase = "Trabajo" 
        self.current_seconds_left = 0
        self.total_seconds_left = 0
        self.is_paused = False