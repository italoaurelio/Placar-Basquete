import sys
import socket
import threading
import os  # nova linha para gerar caminho absoluto
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QMetaObject, pyqtSlot  # modificado
from PyQt5.QtGui import QPixmap, QIcon  # novo

class PlacarWindow(QWidget):
    def __init__(self):
        super().__init__()
        base_path = os.path.dirname(os.path.abspath(__file__))  # novo
        self.setWindowTitle("Placar de Basquete")
        # Atualize as flags para incluir Qt.WindowSystemMenuHint
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.Window) # garante que apareça na barra de tarefas
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # nova linha para bordas arredondadas

        default_width = 800
        default_height = default_width // 4
        self.resize(default_width, default_height)
        self.setMinimumSize(default_width, default_height)
        self.default_width = default_width            # novo
        self.default_height = default_height          # novo
        self.scaled = False                           # novo

        self.time_a = 0
        self.time_b = 0
        self.segundos = 0
        self.timer_mode = "asc"  # novo: modo padrão de timer

        # --- NOVOS COMPONENTES ---
        self.period_label    = QLabel("Período 1")
        self.team_a_name     = QLabel("Time A")
        self.team_a_score    = QLabel("0")
        self.team_b_name     = QLabel("Time B")
        self.team_b_score    = QLabel("0")
        self.timer_label     = QLabel("00:00")

        self.team_a_icon = QLabel()
        self.team_a_icon.setFixedSize(50, 50)
        self.team_a_icon.setScaledContents(True)
        self.team_b_icon = QLabel()
        self.team_b_icon.setFixedSize(50, 50)
        self.team_b_icon.setScaledContents(True)

        for lbl in (self.period_label, self.timer_label):
            lbl.setStyleSheet("font-size: 30px; color: white;")
            lbl.setAlignment(Qt.AlignCenter)
        for lbl in (self.team_a_name, self.team_b_name):
            lbl.setStyleSheet("font-size: 40px; color: white;")
            lbl.setAlignment(Qt.AlignCenter)
        for lbl in (self.team_a_score, self.team_b_score):
            lbl.setStyleSheet("font-size: 80px; color: white;")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lbl.setMargin(5)  # reduz a margem vertical

        # Configura os estilos para os labels não numéricos (time names e período)
        
        # Sobrescreve os estilos dos números para usar fonte digital
        self.timer_label.setStyleSheet("font-family: 'Digital-7'; font-size: 50px; color: white;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setMinimumWidth(200)  # nova linha para aumentar largura horizontal do tempo
        for lbl in (self.team_a_score, self.team_b_score):
            lbl.setStyleSheet("font-family: 'Digital-7'; font-size: 80px; color: white;")

        # Novo layout em duas linhas:
        first_row = QHBoxLayout()
        # Ordem atualizada: time A logo à esquerda, team A nome, período, time B nome e por fim time B logo à direita
        first_row.addWidget(self.team_a_icon)
        first_row.addWidget(self.team_a_name)
        first_row.addWidget(self.period_label)
        first_row.addWidget(self.team_b_name)
        first_row.addWidget(self.team_b_icon)

        second_row = QHBoxLayout()
        second_row.addWidget(self.team_a_score)
        second_row.addWidget(self.timer_label)
        second_row.addWidget(self.team_b_score)

        main_layout = QVBoxLayout()
        main_layout.addLayout(first_row)
        main_layout.addLayout(second_row)
        self.setLayout(main_layout)

        self.setStyleSheet("background-color: #00004d; border-radius: 500px;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        threading.Thread(target=self.socket_server, daemon=True).start()

    def socket_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 5001))
        server.listen(1)

        print("Placar esperando controle conectar...")
        conn, _ = server.accept()
        print("Controle conectado!")

        while True:
            data = conn.recv(1024).decode()
            if data.startswith("SET_NAME_A:"):
                self.team_a_name.setText(data.split(":", 1)[1])
            elif data.startswith("SET_NAME_B:"):
                self.team_b_name.setText(data.split(":", 1)[1])
            elif data.startswith("SET_PERIOD:"):
                self.period_label.setText(data.split(":", 1)[1])
            elif data.startswith("SET_TIMER:"):
                try:
                    self.segundos = int(data.split(":", 1)[1])
                except ValueError:
                    pass
            elif data.startswith("TIMER_MODE:DESC"):
                self.timer_mode = "desc"
            elif data == "TIMER_MODE:ASC":
                self.timer_mode = "asc"
            elif data.startswith("SET_ICON:"):
                icon_path = data.split(":", 1)[1]
                self.setWindowIcon(QIcon(icon_path))
            elif data.startswith("SET_ICON_A:"):
                icon_path = data.split(":", 1)[1]
                pixmap = QPixmap(icon_path)
                self.team_a_icon.setPixmap(pixmap)
            elif data.startswith("SET_ICON_B:"):
                icon_path = data.split(":", 1)[1]
                pixmap = QPixmap(icon_path)
                self.team_b_icon.setPixmap(pixmap)
            elif data == "A+":
                self.time_a += 1
            elif data == "B+":
                self.time_b += 1
            # Novos comandos:
            elif data == "A+2":
                self.time_a += 2
            elif data == "A+3":
                self.time_a += 3
            elif data == "B+2":
                self.time_b += 2
            elif data == "B+3":
                self.time_b += 3
            elif data == "A-1":
                self.time_a = max(self.time_a - 1, 0)
            elif data == "B-1":
                self.time_b = max(self.time_b - 1, 0)
            elif data == "A0":
                self.time_a = 0
            elif data == "B0":
                self.time_b = 0
            elif data == "RESET":
                self.time_a = 0
                self.time_b = 0
                self.segundos = 0
                QMetaObject.invokeMethod(self, "stop_timer", Qt.QueuedConnection)
            elif data == "START":
                QMetaObject.invokeMethod(self, "start_timer", Qt.QueuedConnection)
            elif data == "STOP":
                QMetaObject.invokeMethod(self, "stop_timer", Qt.QueuedConnection)

            self.update_ui()

    @pyqtSlot()
    def start_timer(self):
        self.timer.start(1000)

    @pyqtSlot()
    def stop_timer(self):
        self.timer.stop()

    def update_ui(self):
        # substitui labels antigos por placares separados
        self.team_a_score.setText(str(self.time_a))
        self.team_b_score.setText(str(self.time_b))
        minutos = self.segundos // 60
        segundos = self.segundos % 60
        self.timer_label.setText(f"{minutos:02}:{segundos:02}")

    def update_timer(self):
        if self.timer_mode == "asc":
            self.segundos += 1
        else:  # Descending mode: count down until zero, then stop
            if self.segundos > 0:
                self.segundos -= 1
            if self.segundos == 0:
                QMetaObject.invokeMethod(self, "stop_timer", Qt.QueuedConnection)
        self.update_ui()

    def keyPressEvent(self, event):
        # Verifica se F11 foi pressionado
        if event.key() == Qt.Key_F11:
            screen = QApplication.primaryScreen().availableGeometry()
            if not self.scaled:
                new_width = int(screen.width() * 0.95)
                factor = new_width / self.default_width
                new_height = int(self.default_height * factor)
                self.resize(new_width, new_height)
                self.scaleUI(factor)
                # Centraliza a janela
                x = screen.x() + (screen.width() - new_width) // 2
                y = screen.y() + (screen.height() - new_height) // 2
                self.move(x, y)
                self.scaled = True
            else:
                self.resize(self.default_width, self.default_height)
                self.scaleUI(1)
                x = screen.x() + (screen.width() - self.default_width) // 2
                y = screen.y() + (screen.height() - self.default_height) // 2
                self.move(x, y)
                self.scaled = False
        else:
            super().keyPressEvent(event)

    def scaleUI(self, factor):
        # Atualiza os estilos dos labels com os novos tamanhos de fonte e ícones
        self.period_label.setStyleSheet(f"font-size: {int(30 * factor)}px; color: white;")
        self.timer_label.setStyleSheet(f"font-family: 'Digital-7'; font-size: {int(50 * factor)}px; color: white;")
        self.team_a_name.setStyleSheet(f"font-size: {int(40 * factor)}px; color: white;")
        self.team_b_name.setStyleSheet(f"font-size: {int(40 * factor)}px; color: white;")
        self.team_a_score.setStyleSheet(f"font-family: 'Digital-7'; font-size: {int(80 * factor)}px; color: white;")
        self.team_b_score.setStyleSheet(f"font-family: 'Digital-7'; font-size: {int(80 * factor)}px; color: white;")
        new_icon_size = int(50 * factor)
        self.team_a_icon.setFixedSize(new_icon_size, new_icon_size)
        self.team_b_icon.setFixedSize(new_icon_size, new_icon_size)
        self.timer_label.setMinimumWidth(int(200 * factor))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlacarWindow()
    window.show()
    sys.exit(app.exec_())
