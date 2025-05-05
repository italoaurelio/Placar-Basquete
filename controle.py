# controle.py
import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, QRadioButton, QButtonGroup, QLabel, QHBoxLayout, QGroupBox, QSizePolicy, QGridLayout

class ControleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle do Placar")
 # aumento do tamanho para comportar novas funções

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 5000))
        
        # Initialize current period as 1
        self.period = 1
        
        grid = QGridLayout()  # substitui a main layout

        # Seção: Atualizar Nomes
        group_names = QGroupBox("Atualizar Nomes")
        layout_names = QVBoxLayout()
        self.nome_time_a = QLineEdit()
        self.nome_time_a.setPlaceholderText("Time A")
        self.nome_time_b = QLineEdit()
        self.nome_time_b.setPlaceholderText("Time B")
        btn_update_names = QPushButton("Atualizar")
        btn_update_names.setStyleSheet("font-size: 20px; padding: 10px;")
        btn_update_names.clicked.connect(self.update_names)
        layout_names.addWidget(self.nome_time_a)
        layout_names.addWidget(self.nome_time_b)
        layout_names.addWidget(btn_update_names)
        group_names.setLayout(layout_names)
        grid.addWidget(group_names, 0, 0)

        # Atualizar Período - substituindo QLineEdit por botões para aumentar e diminuir
        group_period = QGroupBox("Atualizar Período")
        layout_period = QHBoxLayout()
        btn_decrease = QPushButton("Diminuir Período")
        btn_decrease.setStyleSheet("font-size: 20px; padding: 10px;")
        btn_decrease.clicked.connect(self.decrease_period)
        btn_increase = QPushButton("Aumentar Período")
        btn_increase.setStyleSheet("font-size: 20px; padding: 10px;")
        btn_increase.clicked.connect(self.increase_period)
        layout_period.addWidget(btn_decrease)
        layout_period.addWidget(btn_increase)
        group_period.setLayout(layout_period)
        grid.addWidget(group_period, 0, 1)

        # Seção: Atualizar Timer (Placar)
        group_timer = QGroupBox("Atualizar Timer")
        layout_timer = QVBoxLayout()
        self.input_score_a = QLineEdit()
        self.input_score_a.setPlaceholderText("Valor (ex.: 14 para 00:14)")
        btn_update_score = QPushButton("Atualizar")
        btn_update_score.setStyleSheet("font-size: 20px; padding: 10px;")
        btn_update_score.clicked.connect(self.update_score)
        layout_timer.addWidget(self.input_score_a)
        layout_timer.addWidget(btn_update_score)
        group_timer.setLayout(layout_timer)
        grid.addWidget(group_timer, 1, 0)

        # Seção: Selecionar Ícones
        group_icon = QGroupBox("Selecionar Ícones")
        layout_icon = QVBoxLayout()
        btn_select_icon_a = QPushButton("Selecionar Ícone Time A")
        btn_select_icon_a.setStyleSheet("font-size: 20px; padding: 10px;")
        btn_select_icon_a.clicked.connect(self.select_icon_a)
        btn_select_icon_b = QPushButton("Selecionar Ícone Time B")
        btn_select_icon_b.setStyleSheet("font-size: 20px; padding: 10px;")
        btn_select_icon_b.clicked.connect(self.select_icon_b)
        layout_icon.addWidget(btn_select_icon_a)
        layout_icon.addWidget(btn_select_icon_b)
        group_icon.setLayout(layout_icon)
        grid.addWidget(group_icon, 1, 1)

        # Seção para selecionar o modo do Timer
        group_mode = QGroupBox("Modo Timer")
        layout_mode = QHBoxLayout()
        radio_asc = QRadioButton("Crescente")
        radio_desc = QRadioButton("Decrescente")
        radio_asc.setChecked(True)
        layout_mode.addWidget(radio_asc)
        layout_mode.addWidget(radio_desc)
        group_mode.setLayout(layout_mode)
        grid.addWidget(group_mode, 2, 0, 1, 2)
        
        # Conectar sinais dos radio buttons
        radio_asc.toggled.connect(self.radio_asc_changed)
        radio_desc.toggled.connect(self.radio_desc_changed)
        
        # Seção: Ações Rápidas dispostas em grid com 2 colunas
        group_actions = QGroupBox("Ações")
        group_actions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_actions = QGridLayout()
        btn_a = QPushButton("+1 Time A")
        btn_b = QPushButton("+1 Time B")
        btn_start = QPushButton("Iniciar Timer")
        btn_stop = QPushButton("Parar Timer")
        btn_reset = QPushButton("Resetar Placar")
        for btn in (btn_a, btn_b, btn_start, btn_stop, btn_reset):
            btn.setStyleSheet("font-size: 18px; padding: 10px;")
        layout_actions.addWidget(btn_a, 0, 0)
        layout_actions.addWidget(btn_b, 0, 1)
        layout_actions.addWidget(btn_start, 1, 0)
        layout_actions.addWidget(btn_stop, 1, 1)
        layout_actions.addWidget(btn_reset, 2, 0, 1, 2)
        btn_a.clicked.connect(lambda: self.enviar("A+"))
        btn_b.clicked.connect(lambda: self.enviar("B+"))
        btn_start.clicked.connect(lambda: self.enviar("START"))
        btn_stop.clicked.connect(lambda: self.enviar("STOP"))
        btn_reset.clicked.connect(lambda: self.enviar("RESET"))
        group_actions.setLayout(layout_actions)
        grid.addWidget(group_actions, 3, 0, 1, 2)  # span both columns

        self.setLayout(grid)

    def update_names(self):
        nome_a = self.nome_time_a.text()
        nome_b = self.nome_time_b.text()
        if nome_a:
            self.enviar(f"SET_NAME_A:{nome_a}")
        if nome_b:
            self.enviar(f"SET_NAME_B:{nome_b}")

    def update_period(self):
        periodo = self.input_periodo.text()
        if periodo:
            self.enviar(f"SET_PERIOD:{periodo}")

    def update_score(self):
        # Ao clicar, apenas atualiza o timer com o valor digitado no input_score_a.
        raw_value = self.input_score_a.text().strip()
        if raw_value.isdigit():
            if len(raw_value) <= 2:
                total_seconds = int(raw_value)
            else:
                minutes = int(raw_value[:-2])
                seconds = int(raw_value[-2:])
                total_seconds = minutes * 60 + seconds
            self.enviar(f"SET_TIMER:{total_seconds}")

    def select_icon_a(self):
        icon_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Ícone do Time A", "", "Images (*.png *.xpm *.jpg)")
        if icon_path:
            self.enviar(f"SET_ICON_A:{icon_path}")

    def select_icon_b(self):
        icon_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Ícone do Time B", "", "Images (*.png *.xpm *.jpg)")
        if icon_path:
            self.enviar(f"SET_ICON_B:{icon_path}")

    def enviar(self, comando):
        self.sock.send(comando.encode())

    def increase_period(self):
        self.period += 1
        self.enviar(f"SET_PERIOD:Período {self.period}")

    def decrease_period(self):
        if self.period > 1:
            self.period -= 1
            self.enviar(f"SET_PERIOD:Período {self.period}")

    def radio_asc_changed(self, checked):
        if checked:
            self.enviar("TIMER_MODE:ASC")
    
    def radio_desc_changed(self, checked):
        if checked:
            self.enviar("TIMER_MODE:DESC")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ControleWindow()
    window.show()
    sys.exit(app.exec_())
