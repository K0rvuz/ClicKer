import sys
import os
import time
import shutil
import pyautogui as pa

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon


# Path para o nuikta

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# config global

PASTA_IMAGENS = resource_path("imagens")
os.makedirs(PASTA_IMAGENS, exist_ok=True)

pa.PAUSE = 0.2  #tempo entre as ações do pyautogui


# darkmode

DARK_STYLE = """
QWidget {
    background-color: #121212;
    color: #e0e0e0;
    font-family: Segoe UI;
    font-size: 13px;
}

QPushButton {
    background-color: #1f1f1f;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 8px 14px;
}

QPushButton:hover {
    background-color: #2a2a2a;
}

QPushButton:pressed {
    background-color: #333;
}

QListWidget {
    background-color: #1a1a1a;
    border: 1px solid #333;
    border-radius: 8px;
}

QLabel#StatusLabel {
    font-weight: bold;
    padding: 6px;
}
"""


# Automação base

class AutomationWorker(QThread):
    imagem_encontrada = Signal(str)

    def __init__(self, imagens):
        super().__init__()
        self.imagens = imagens
        self.running = True

    def run(self):
        while self.running:
            for img in list(self.imagens):
                try:
                    pos = pa.locateCenterOnScreen(img, confidence=0.9)
                    if pos:
                        pa.moveTo(pos)
                        pa.click()
                        self.imagem_encontrada.emit(img)
                except Exception:
                    pass
            time.sleep(0.4)

    def stop(self):
        self.running = False


# configuração de arrasta e solta

class DropArea(QLabel):
    imagem_solte = Signal(str)

    def __init__(self):
        super().__init__("Arraste imagens aqui")
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #444;
                border-radius: 10px;
                padding: 30px;
                color: #aaa;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            caminho = url.toLocalFile()
            if caminho.lower().endswith((".png", ".jpg", ".jpeg")):
                self.imagem_solte.emit(caminho)


# interface principal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Icone
        self.setWindowIcon(QIcon(resource_path("assets/clicker.ico")))

        self.setWindowTitle("ClicKer")
        self.resize(620, 520)

        self.imagens = []
        self.contador = {}
        self.worker = None

        # Widgets
        self.status = QLabel("🔴 Parado")
        self.status.setObjectName("StatusLabel")

        self.lista = QListWidget()
        self.drop_area = DropArea()

        self.btn_add = QPushButton("Adicionar")
        self.btn_remove = QPushButton("Remover")
        self.btn_start = QPushButton("Iniciar")
        self.btn_stop = QPushButton("Parar")

        # Layout 
        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.drop_area)
        layout.addWidget(self.lista)

        botoes = QHBoxLayout()
        botoes.addWidget(self.btn_add)
        botoes.addWidget(self.btn_remove)
        botoes.addStretch()
        botoes.addWidget(self.btn_start)
        botoes.addWidget(self.btn_stop)

        layout.addLayout(botoes)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conexões
        self.btn_add.clicked.connect(self.add_imagem)
        self.btn_remove.clicked.connect(self.remover_imagem)
        self.btn_start.clicked.connect(self.iniciar)
        self.btn_stop.clicked.connect(self.parar)
        self.drop_area.imagem_solte.connect(self.adicionar_por_drop)

        # Carregar imagens existentes (banco de dados pra imagem, ficará em uma pasta)
        self.carregar_imagens()

    # imgs

    def copiar_para_pasta(self, origem):
        nome = os.path.basename(origem)
        destino = os.path.join(PASTA_IMAGENS, nome)

        if not os.path.exists(destino):
            shutil.copy(origem, destino)

        return destino

    def carregar_imagens(self):
        for arquivo in os.listdir(PASTA_IMAGENS):
            if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
                caminho = os.path.join(PASTA_IMAGENS, arquivo)
                self.imagens.append(caminho)
                self.contador[caminho] = 0
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.clear()
        for img in self.imagens:
            nome = os.path.basename(img)
            count = self.contador.get(img, 0)
            self.lista.addItem(f"{nome}   •   Cliques: {count}")

    def add_imagem(self):
        arquivos, _ = QFileDialog.getOpenFileNames(
            self, "Selecionar imagens", "", "Imagens (*.png *.jpg *.jpeg)"
        )
        for arq in arquivos:
            destino = self.copiar_para_pasta(arq)
            if destino not in self.imagens:
                self.imagens.append(destino)
                self.contador[destino] = 0
        self.atualizar_lista()

    def adicionar_por_drop(self, caminho):
        destino = self.copiar_para_pasta(caminho)
        if destino not in self.imagens:
            self.imagens.append(destino)
            self.contador[destino] = 0
            self.atualizar_lista()

    def remover_imagem(self):
        row = self.lista.currentRow()
        if row >= 0:
            img = self.imagens.pop(row)
            self.contador.pop(img, None)
            try:
                os.remove(img)
            except Exception:
                pass
            self.atualizar_lista()

    # Automação

    def iniciar(self):
        if not self.imagens:
            QMessageBox.warning(self, "Aviso", "Nenhuma imagem adicionada.")
            return

        self.worker = AutomationWorker(self.imagens)
        self.worker.imagem_encontrada.connect(self.incrementar)
        self.worker.start()

        self.status.setText("🟢 Rodando")

    def parar(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
            self.worker = None
        self.status.setText("🔴 Parado")

    def incrementar(self, img):
        self.contador[img] += 1
        self.atualizar_lista()

    def closeEvent(self, event):
        self.parar()
        event.accept()


# Principal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

