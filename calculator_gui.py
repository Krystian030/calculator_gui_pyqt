import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QScrollArea, QWidget, QVBoxLayout, QLabel, \
    QPushButton, QSizePolicy, QHBoxLayout, QMessageBox

from calculator import calculate_expression


class BaseWindow(QMainWindow):
    windows = []

    def __init__(self, width, height):
        super().__init__()
        self.setFixedSize(width, height)
        self.build_menu()

    def build_menu(self):
        menu_bar = self.menuBar()
        menu_bar.setObjectName("menu-bar")

        # Sekcja Aplikacja
        menu_application = menu_bar.addMenu("Aplikacja")
        menu_application.setObjectName("menu-application")

        # Kalkulator w sekcji Aplikacja
        calculator_action = QAction("Kalkulator", self)
        calculator_action.triggered.connect(self.on_calculator_clicked)
        menu_application.addAction(calculator_action)

        history_action = QAction("Historia", self)
        history_action.triggered.connect(self.on_history_clicked)
        menu_application.addAction(history_action)

        # Dodanie kreski oddzielającej
        menu_application.addSeparator()

        # Dodanie opcji "Wyjście" w sekcji "Aplikacja"
        quit_action = QAction("Wyjście", self)
        quit_action.triggered.connect(self.on_quit_activate)
        menu_application.addAction(quit_action)

        # Sekcja About
        about_action = QAction("O programie", self)
        about_action.setObjectName("menu-about")
        about_action.triggered.connect(self.on_about_program_clicked)
        menu_bar.addAction(about_action)

    def on_calculator_clicked(self):
        calculator_window = CalculatorWindow(None)
        calculator_window.show()
        self.windows.append(calculator_window)

    def on_history_clicked(self):
        print("on_history_clicked")

    def on_quit_activate(self):
        print("on_quit_activate")

    def on_about_program_clicked(self):
        print("on_about_program_clicked")


class CalculatorWindow(BaseWindow):
    def __init__(self, history_box):
        self.width = 385
        self.height = 450
        super().__init__(self.width, self.height)
        self.history_box = history_box
        self.expression = ""
        self.setObjectName("calculator-window")
        self.setWindowTitle("Kalkulator")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.create_display_panel()

        button_layout = QHBoxLayout()
        self.create_button_panel(button_layout)
        self.layout.addLayout(button_layout)

    def create_display_panel(self):
        scrolled_window = QScrollArea()
        scrolled_window.setObjectName("display-panel")
        scrolled_window.setWidgetResizable(True)
        scrolled_window.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Ustawiamy pasek przewijania poziomego w razie potrzeby
        scrolled_window.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(scrolled_window)

        display_widget = QWidget()
        display_widget.setObjectName("display-panel")
        display_layout = QVBoxLayout()
        display_widget.setLayout(display_layout)

        self.expression_label = QLabel()
        self.expression_label.setObjectName("expression-label")
        self.expression_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # text-align to right
        display_layout.addWidget(self.expression_label)

        self.result_label = QLabel()
        self.result_label.setObjectName("result-label")
        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # text-align to right
        display_layout.addWidget(self.result_label)

        scrolled_window.setWidget(display_widget)

        scrolled_window.setMinimumWidth(310)
        scrolled_window.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        scrolled_window.setFixedHeight(120)

    def create_button_panel(self, parent_layout):
        self.create_numeric_buttons(parent_layout)
        self.create_operator_buttons(parent_layout)

    def create_numeric_buttons(self, paren_layout):
        button_panel = QWidget()
        button_panel.setObjectName("button-panel")
        button_panel.setFixedSize(230, 291)
        button_layout = QGridLayout()

        button_panel.setLayout(button_layout)

        # Przyciski numeryczne 1-9
        numeric_buttons = ['7', '8', '9', '4', '5', '6', '1', '2', '3']
        row = 0
        col = 0
        for i, label in enumerate(numeric_buttons):
            button = QPushButton(label)
            button.setObjectName("button")
            button.setFixedSize(64, 60)
            button_layout.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

            button.clicked.connect(self.on_button_clicked)

        # Przycisk "0"
        button_0 = QPushButton("0")
        button_0.setObjectName("button")
        button_0.setFixedSize(140, 60)
        button_layout.addWidget(button_0, row, 0, 1, 2)
        button_0.clicked.connect(self.on_button_clicked)

        # Przycisk "."
        button_dot = QPushButton(".")
        button_dot.setObjectName("button")
        button_dot.setFixedSize(64, 60)
        button_layout.addWidget(button_dot, row, 2)
        button_dot.clicked.connect(self.on_button_clicked)

        paren_layout.addWidget(button_panel)

    def create_operator_buttons(self, parent_layout):
        operators_panel = QWidget()
        operators_panel.setObjectName("operators-panel")
        operators_panel.setFixedSize(150, 291)

        operators_layout = QGridLayout()
        operators_panel.setLayout(operators_layout)

        operators = ['+', '-', '*', '/', '=', '←']
        row = 0
        col = 0
        for i, label in enumerate(operators):
            button = QPushButton(label)
            button.setObjectName("operator-button")
            button.setFixedSize(64, 88)
            operators_layout.addWidget(button, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

            button.clicked.connect(self.on_button_clicked)

        parent_layout.addWidget(operators_panel)

    def on_button_clicked(self):
        button = self.sender()
        label = button.text()

        # Clean the result if the previous expression has been calculated
        if self.expression == "" and self.result_label.text() != "":
            self.result_label.setText("")

        if label == '=':
            try:
                result = calculate_expression(self.expression)
                self.result_label.setText("=" + str(result))
                # self.history_box.add_to_history(f"{self.expression}={result}")
                self.expression = ""
            except Exception as e:
                self.show_error_dialog(str(e))
                self.result_label.setText("")
                self.expression = ""
                self.expression_label.setText(self.expression)
        else:
            if label == '←':
                self.expression = self.expression[:-1]
                self.expression_label.setText(self.expression)
                if self.expression == "":
                    self.result_label.setText("")
            else:
                self.expression += label

            self.expression_label.setText(self.expression)

    @staticmethod
    def show_error_dialog(message):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setText(message)
        dialog.setWindowTitle("Błąd")
        dialog.addButton(QMessageBox.StandardButton.NoButton)
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("styles.css", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Nie można odnaleźć pliku styles.css")

    window = CalculatorWindow(None)
    window.show()
    sys.exit(app.exec())
