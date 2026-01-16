import sys
import requests
import json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread, pyqtSignal
from ui.ui_mainwindow import Ui_MainWindow


class RequestWorker(QThread):
    success = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, url, context):
        super().__init__()

        self.context = context
        self.url = url

    def run(self):
        try:
            headers = {'Content-Type': 'application/json'}
            data = {"prompt": self.context}
            response = requests.post(url=self.url, 
                                     headers=headers, 
                                     data=json.dumps(data),
                                     timeout=(5, 60))

            self.success.emit(response.json()["response"])

        except requests.exceptions.ConnectTimeout:
            self.failed.emit(f"{self.url} ConnectTimeout")
        except requests.exceptions.ConnectionError:
            self.failed.emit(f"{self.url} ConnectionError")
        except Exception as e:
            self.failed.emit(f"{self.url} Request exception {e}")




class MainWindow(QMainWindow, Ui_MainWindow):
    """
    主窗口类
    
    使用 Qt Designer 设计的 UI，通过 pyuic6 转换为 Python 代码
    命令: pyuic6 ui/mainwindow.ui -o ui/ui_mainwindow.py
    """
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化 UI
        self._setup_ui()
        
        # 连接信号
        self._connect_signals()
    
    def _setup_ui(self):
        """初始化 UI 设置"""
        self.promptTextEdit.setPlaceholderText("请输入您的问题...")
        self.responTextEdit.setReadOnly(True)
        self.statusbar.showMessage("就绪")
    
    def _connect_signals(self):
        """连接信号和槽"""
        self.pushButton.clicked.connect(self.on_send_clicked)
    
    def on_send_clicked(self):
        """处理发送按钮点击事件"""
        prompt_text = self.promptTextEdit.toPlainText()
        
        if not prompt_text.strip():
            self.statusbar.showMessage("请输入内容", 2000)
            return
        
        # 显示正在处理
        self.statusbar.showMessage("正在处理...", 0)
        self.pushButton.setEnabled(False)  # 禁用按钮防止重复点击

        self.reqWorker = RequestWorker('http://127.0.0.1:6006', prompt_text)
        self.reqWorker.success.connect(self.onRequestSuccess)
        self.reqWorker.failed.connect(self.onRequestFailed)
        self.reqWorker.start()

    def onRequestSuccess(self, str):
        self.responTextEdit.setPlainText(str)
        self.statusbar.showMessage("响应成功", 3000)
        self.pushButton.setEnabled(True)

    def onRequestFailed(self, str):
        self.responTextEdit.setPlainText(str)
        self.statusbar.showMessage("响应失败！", 3000)
        self.pushButton.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
