import sys, requests
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout
import matplotlib.pyplot as plt

def upload_csv():
    file, _ = QFileDialog.getOpenFileName()
    if not file:
        return

    res = requests.post(
        "http://127.0.0.1:8000/api/upload/",
        files={"file": open(file, "rb")}
    )
    data = res.json()

    plt.bar(
        data["type_distribution"].keys(),
        data["type_distribution"].values()
    )
    plt.title("Equipment Type Distribution")
    plt.xlabel("Equipment Type")
    plt.ylabel("Count")
    plt.show()

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

btn = QPushButton("Upload CSV")
btn.clicked.connect(upload_csv)
label = QLabel("Upload a CSV file to visualize equipment distribution")
layout.addWidget(label)


layout.addWidget(btn)
window.setLayout(layout)
window.setWindowTitle("Chemical Equipment Visualizer (Desktop) – Shared Backend API")
window.show()

sys.exit(app.exec_())
