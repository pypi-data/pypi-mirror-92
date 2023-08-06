import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui
import qtmax
from pymxs import runtime as rt

# DO NOT SORT IMPORTS !!!!!!!!!!!!!
CONDUCTOR_LOCATION = os.path.dirname(os.path.dirname(__file__))
sys.path.append(CONDUCTOR_LOCATION)


from ciomax import reloader
reload(reloader)

# While in development, we reload classes when this file is executed.

from ciomax.components.footer_buttons_grp import FooterButtonsGrp
from ciomax.preview_tab import PreviewTab
from ciomax.main_tab import MainTab
from ciomax.store import ConductorStore
from ciomax import submit, renderer
from ciocore.gpath import Path

BACKGROUND_COLOR = "rgb(48, 48, 48)"
STYLESHEET = """
QLineEdit {{ background: {bg}; }}
QSpinBox {{ background: {bg}; }}
QListWidget {{ background: {bg}; }}
QToolButton {{ border: none; }}
QTextEdit {{ background: {bg}; }}""".format(bg=BACKGROUND_COLOR)


class ConductorDialog(QtWidgets.QDialog):
    """
    Build the dialog as a child of the Max window.

    We build a tab layout, and the first tab contains the main controls.
    """

    def __init__(self):
        QtWidgets.QDialog.__init__(
            self, QtWidgets.QWidget.find(rt.windows.getMAXHWND()))
        self.setStyleSheet(STYLESHEET)
        self.store = ConductorStore()
        self.setWindowTitle("Conductor")
        self.layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        self.conductor_location = Path(CONDUCTOR_LOCATION).posix_path()

        self.button_row = FooterButtonsGrp()

        self.setLayout(self.layout)
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.button_row)

        self.main_tab = MainTab(self)
        self.preview_tab = PreviewTab(self)

        self.tab_widget.addTab(self.main_tab, "Configure")
        self.tab_widget.addTab(self.preview_tab, "Preview")

        self.main_tab.populate_from_store()
        self.configure_signals()

    def configure_signals(self):
        self.tab_widget.currentChanged.connect(self.on_tab_change)

        self.button_row.close_button.clicked.connect(self.on_close)
        self.button_row.validate_button.clicked.connect(self.on_validate)
        self.button_row.submit_button.clicked.connect(self.on_submit)

    def on_tab_change(self, index):
        if index == 1:
            context = self.main_tab.get_context()
            submission = self.main_tab.resolve(context)
            self.preview_tab.populate(submission)

    def on_close(self):
        print "on_close"

    def on_validate(self):
        print "on_validate"

    def on_submit(self):
        submit.submit(self)


def main():

    dlg = ConductorDialog()
    dlg.resize(600, 800)

    # exec_() causes the window to be modal. This means we don't have to manage
    # any communication between max and the dialog, like changes to the frame
    # range while the dialog is open.
    dlg.exec_()


if __name__ == '__main__':
    main()
