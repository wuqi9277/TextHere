import json,subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit,
    QCheckBox, QSpinBox, QPushButton, QHBoxLayout,
    QMessageBox
)
from PyQt5.QtCore import Qt,QCoreApplication

class SettingsEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Settings Editor")
        self.resize(400, 300)
        self.filename = "setting.json"
        self.setStyleSheet("""
        QWidget {
            font-size: 9pt;  /* 设置基准字体大小 */
        }
        QLineEdit, QSpinBox {
            padding: 5px;    /* 增加控件内边距 */
        }
        """)
        # 创建控件
        self.states_check = QCheckBox()
        self.states_msg_edit = QLineEdit()
        self.id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.sentences_edit = QLineEdit()
        self.sleep_spin = QSpinBox()
        self.reset_check = QCheckBox()
        self.internet_check = QCheckBox()
        
        # 配置spinbox
        self.sleep_spin.setRange(0, 99999)
        
        # 按钮
        self.save_btn = QPushButton("保存")
        self.cancel_btn = QPushButton("取消")
        self.launch_btn = QPushButton("启动程序")
        
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QFormLayout()
        
        # 添加表单行
        layout.addRow("是否启用:", self.states_check)
        layout.addRow("(上次)状态消息:", self.states_msg_edit)
        layout.addRow("(上次)ID:", self.id_edit)
        layout.addRow("(上次)名称:", self.name_edit)
        layout.addRow("(上次)句子:", self.sentences_edit)
        layout.addRow("休眠时间:", self.sleep_spin)
        layout.addRow("重置所有:", self.reset_check)
        layout.addRow("使用网络句子(实验性):", self.internet_check)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.launch_btn)  # 新增按钮
        
        layout.addRow(btn_layout)
        self.setLayout(layout)
        
        # 连接信号
        self.save_btn.clicked.connect(self.save_data)
        self.cancel_btn.clicked.connect(self.close)
        self.launch_btn.clicked.connect(self.launch_program)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            self.states_check.setChecked(data['states'])
            self.states_msg_edit.setText(data['states_msg'] or "")
            self.id_edit.setText(str(data['id']))
            self.name_edit.setText(data['name'])
            self.sentences_edit.setText(data['sentences'])
            self.sleep_spin.setValue(data['sleep_seconds'])
            self.reset_check.setChecked(data['reset_all'])
            self.internet_check.setChecked(data['use_internet_sentences'])
            
        except Exception as e:
            print(f"加载错误: {str(e)}")

    def save_data(self):
        data = {
            'states': self.states_check.isChecked(),
            'states_msg': self.states_msg_edit.text() or None,
            'id': self.id_edit.text(),
            'name': self.name_edit.text(),
            'sentences': self.sentences_edit.text(),
            'sleep_seconds': self.sleep_spin.value(),
            'reset_all': self.reset_check.isChecked(),
            'use_internet_sentences': self.internet_check.isChecked()
        }

        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
            print("保存成功")
            self.close()
        except Exception as e:
            print(f"保存错误: {str(e)}")
    
    def launch_program(self):
        print("启动程序")
        # 这里可以添加启动程序的代码
        try:
            path = ""
            subprocess.Popen(path, shell=True)
            QMessageBox.information(self, "提示", "程序已启动")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动失败: {str(e)}")



if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用自动高DPI缩放
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)     # 启用高清图标
    app = QApplication([])
    window = SettingsEditor()
    window.show()
    app.exec_()