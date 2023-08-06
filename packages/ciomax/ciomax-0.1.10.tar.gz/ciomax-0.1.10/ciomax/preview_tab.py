from PySide2 import QtWidgets, QtGui
import json


class PreviewTab(QtWidgets.QScrollArea):

    def __init__(self,dialog):
        super(PreviewTab, self).__init__()
    
        widget = QtWidgets.QWidget()
        self.dialog = dialog
        self.setWidget(widget)
        self.setWidgetResizable(1)

        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)

        self.text_area = QtWidgets.QTextEdit()

        self.text_area.setReadOnly(True)
        self.text_area.setWordWrapMode(QtGui.QTextOption.NoWrap)
        layout.addWidget(self.text_area)

        # self.populate(JSON)

    def populate(self, submission):
        self.text_area.setText(json.dumps(submission, indent=3))




