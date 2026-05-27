"""
merged.py
Bisection and Newton-Raphson root-finding methods with a PyQt6 GUI.
"""

import sys
import math

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt


TOL = 1e-6
MAX_ITER = 100


def bisection(f, a, b, tol=TOL, max_iter=MAX_ITER):
    """Bisection method for root finding."""
    fa, fb = f(a), f(b)

    if abs(fa) < tol:
        return a, True, 0, [(0, a, b, a, fa, fb, fa)]
    if abs(fb) < tol:
        return b, True, 0, [(0, a, b, b, fa, fb, fb)]

    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")

    steps = []

    for i in range(max_iter):
        m = (a + b) / 2
        fm = f(m)
        steps.append((i, a, b, m, fa, fb, fm))

        if abs(fm) < tol or (b - a) / 2 < tol:
            return m, True, i + 1, steps

        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm

    return m, False, max_iter, steps


def newton_raphson(f, df, x0, tol=TOL, max_iter=MAX_ITER):
    """Newton-Raphson method for root finding."""
    steps = []

    for i in range(max_iter):
        fx = f(x0)
        dfx = df(x0)

        if abs(dfx) < 1e-15:
            return x0, False, i + 1, steps

        x1 = x0 - fx / dfx
        steps.append((i, x0, x1, fx, dfx))

        if abs(x1 - x0) < tol and abs(f(x1)) < tol:
            return x1, True, i + 1, steps

        x0 = x1

    return x0, False, max_iter, steps


class MethodApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Root Finder - Bisection & Newton-Raphson")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QVBoxLayout(self)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        self.bisection_tab = QWidget()
        self.newton_tab = QWidget()

        tabs.addTab(self.bisection_tab, "Bisection Method")
        tabs.addTab(self.newton_tab, "Newton-Raphson Method")

        self._build_bisection_ui()
        self._build_newton_ui()

    def _build_bisection_ui(self):
        layout = QVBoxLayout(self.bisection_tab)

        form = QFormLayout()
        self.b_func = QLineEdit("x**3 - x - 2")
        self.b_a = QLineEdit("1")
        self.b_b = QLineEdit("2")
        form.addRow("f(x):", self.b_func)
        form.addRow("a:", self.b_a)
        form.addRow("b:", self.b_b)
        layout.addLayout(form)

        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(self._solve_bisection)
        layout.addWidget(solve_btn)

        self.b_result = QLabel("Root \u2248")
        layout.addWidget(self.b_result)

        self.b_table = QTableWidget()
        self.b_table.setColumnCount(7)
        self.b_table.setHorizontalHeaderLabels(["n", "a", "b", "m", "f(a)", "f(b)", "f(m)"])
        self.b_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.b_table.verticalHeader().setVisible(False)
        layout.addWidget(self.b_table)

    def _build_newton_ui(self):
        layout = QVBoxLayout(self.newton_tab)

        form = QFormLayout()
        self.n_func = QLineEdit("x**3 - x - 2")
        self.n_deriv = QLineEdit("3*x**2 - 1")
        self.n_x0 = QLineEdit("1.5")
        form.addRow("f(x):", self.n_func)
        form.addRow("f'(x):", self.n_deriv)
        form.addRow("x0:", self.n_x0)
        layout.addLayout(form)

        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(self._solve_newton)
        layout.addWidget(solve_btn)

        self.n_result = QLabel("Root \u2248")
        layout.addWidget(self.n_result)

        self.n_table = QTableWidget()
        self.n_table.setColumnCount(5)
        self.n_table.setHorizontalHeaderLabels(["n", "x_n", "x_{n+1}", "f(x_n)", "f'(x_n)"])
        self.n_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.n_table.verticalHeader().setVisible(False)
        layout.addWidget(self.n_table)

    def _make_func(self, expr):
        allowed = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
            "pi": math.pi, "e": math.e, "abs": abs,
        }
        return lambda x: eval(expr, {"__builtins__": {}}, {**allowed, "x": x})

    def _solve_bisection(self):
        try:
            f = self._make_func(self.b_func.text())
            a = float(self.b_a.text())
            b = float(self.b_b.text())
            root, converged, iters, steps = bisection(f, a, b)

            self.b_table.setRowCount(len(steps))
            for i, (n, a1, b1, m, fa, fb, fm) in enumerate(steps):
                self.b_table.setItem(i, 0, QTableWidgetItem(str(n)))
                self.b_table.setItem(i, 1, QTableWidgetItem(f"{a1:.6f}"))
                self.b_table.setItem(i, 2, QTableWidgetItem(f"{b1:.6f}"))
                self.b_table.setItem(i, 3, QTableWidgetItem(f"{m:.6f}"))
                self.b_table.setItem(i, 4, QTableWidgetItem(f"{fa:.6f}"))
                self.b_table.setItem(i, 5, QTableWidgetItem(f"{fb:.6f}"))
                self.b_table.setItem(i, 6, QTableWidgetItem(f"{fm:.6f}"))

            status = "converged" if converged else "did not converge"
            self.b_result.setText(f"Root \u2248 {root:.8f}  ({status}, {iters} iterations)")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _solve_newton(self):
        try:
            f = self._make_func(self.n_func.text())
            df = self._make_func(self.n_deriv.text())
            x0 = float(self.n_x0.text())
            root, converged, iters, steps = newton_raphson(f, df, x0)

            self.n_table.setRowCount(len(steps))
            for i, (n, xn, xn1, fx, dfx) in enumerate(steps):
                self.n_table.setItem(i, 0, QTableWidgetItem(str(n)))
                self.n_table.setItem(i, 1, QTableWidgetItem(f"{xn:.6f}"))
                self.n_table.setItem(i, 2, QTableWidgetItem(f"{xn1:.6f}"))
                self.n_table.setItem(i, 3, QTableWidgetItem(f"{fx:.6f}"))
                self.n_table.setItem(i, 4, QTableWidgetItem(f"{dfx:.6f}"))

            status = "converged" if converged else "did not converge"
            self.n_result.setText(f"Root \u2248 {root:.8f}  ({status}, {iters} iterations)")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MethodApp()
    window.show()
    sys.exit(app.exec())
