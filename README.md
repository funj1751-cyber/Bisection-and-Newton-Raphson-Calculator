# Bisection & Newton-Raphson Calculator

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt-6-green)](https://www.riverbankcomputing.com/software/pyqt/)

A dual-method root-finding calculator with a tabbed GUI. Supports both the **Bisection method** and the **Newton-Raphson method**.

## Features

- **Bisection Method** tab — for bracketed root finding
- **Newton-Raphson Method** tab — for faster convergence with derivative input
- Tabular iteration output for both methods
- Pure Python math function evaluation

## Setup

```bash
pip install PyQt6
python merged.py
```

## Usage

### Bisection Method
1. Enter `f(x)`, interval endpoints `a` and `b`
2. Click **Solve**

### Newton-Raphson Method
1. Enter `f(x)` and its derivative `f'(x)`
2. Provide initial guess `x₀`
3. Click **Solve**

## License

MIT
