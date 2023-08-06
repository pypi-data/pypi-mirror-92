from argparse import ArgumentParser
import itertools as it
import logging
from pathlib import Path
import re
import sys

from cpymad.madx import Madx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QDoubleValidator
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,
    QLineEdit, QMessageBox, QShortcut, QSpinBox, QComboBox, QLabel, QCheckBox,
    QGroupBox, QDoubleSpinBox
)


logging.basicConfig(level=logging.INFO)


class LatticeExplorer(QMainWindow):

    def __init__(self, f_path: str):
        super().__init__()
        self.setWindowTitle('Lattice Explorer')
        self.main = MainWindow(f_path)
        self.setCentralWidget(self.main)


class MainWindow(QWidget):

    def __init__(self, f_path: str):
        super().__init__()

        self.controls = {
            'BETA0': QCheckBox('BETA0'),
        }
        controls_layout = QHBoxLayout()
        for widget in self.controls.values():
            controls_layout.addWidget(widget)

        self.beta0_input = Beta0Widget()
        self.beta0_input.parse_beta0(f_path)
        self.beta0_input.setVisible(bool(self.beta0_input.arguments))

        self.canvas = Canvas()

        main_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.beta0_input)
        main_layout.addWidget(self.canvas)
        self.setLayout(main_layout)

        self.script_path = f_path
        self.madx = Madx()
        self.madx.call(f_path)

        twiss = self.madx.twiss(**self.beta0_input.arguments)
        self.controls_widget = ControlsWidget(twiss, self.compute)
        self.controls_widget.show()

        self.controls['BETA0'].stateChanged.connect(self._activate_beta0)

    def compute(self):
        pass

    def _activate_beta0(self, state):
        if state:
            self.beta0_input.parse_beta0(self.script_path)
        self.beta0_input.setVisible(state)


class ControlsWidget(QWidget):

    def __init__(self, twiss, callback):
        super().__init__()
        self.setWindowTitle('Controls')
        self.groups = {
            'hkicker': QGroupBox('HKicker'),
            'vkicker': QGroupBox('VKicker'),
            'quadrupole': QGroupBox('Quadrupole'),
        }
        self.units = {
            'hkicker': dict(factor=1e-3, text='mrad'),
            'vkicker': dict(factor=1e-3, text='mrad'),
            'quadrupole': dict(factor=1, text='1/m^2')
        }
        self.input_fields = {}
        self.values = {}
        defaults = {
            'hkicker': lambda x: x['hkick'],
            'vkicker': lambda x: x['vkick'],
            'quadrupole': lambda x: x['k1l'] / x['l'],
        }
        step_sizes = {
            'hkicker': 0.1,
            'vkicker': 0.1,
            'quadrupole': 1e-3,
        }
        decimal_precision = {
            'hkicker': 2,
            'vkicker': 2,
            'quadrupole': 5,
        }
        layouts = {k: QVBoxLayout() for k in self.groups}
        for index in it.count():
            try:
                element = twiss[index]
            except IndexError:
                break
            keyword = element['keyword'].lower()
            name = element['name']
            if keyword in self.groups:
                element_layout = QHBoxLayout()
                element_layout.addWidget(QLabel(name))
                field = QDoubleSpinBox()
                field.setValue(defaults[keyword](element) / self.units[keyword]['factor'])
                field.setSingleStep(step_sizes[keyword])
                field.setDecimals(decimal_precision[keyword])
                field.editingFinished.connect(partialmethod(self._update_value, name))
                field.editingFinished.connect(callback)
                element_layout.addWidget(field)
                element_layout.addWidget(QLabel(self.units[keyword]['text']))
                layouts[keyword].addLayout(element_layout)
                self.input_fields[name] = field
                self.units[name] = self.units[keyword]
                self._update_value(name)

        for key, group in self.groups.items():
            group.setLayout(layouts[key])

        kicker_layout = QVBoxLayout()
        kicker_layout.addWidget(self.groups['hkicker'])
        kicker_layout.addWidget(self.groups['vkicker'])

        main_layout = QHBoxLayout()
        main_layout.addLayout(kicker_layout)
        main_layout.addWidget(self.groups['quadrupole'])
        self.setLayout(main_layout)

    def _update_value(self, name):
        logging.info(f'Setting {name} to {value}')
        self.values[name] = self.units[name]['factor'] * float(self.input_fields[name].text())


class Beta0Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.arguments = {}
        self.beta0_input = {
            'X': QLineEdit(),
            'Y': QLineEdit(),
            'BETX': QLineEdit(),
            'BETY': QLineEdit(),
            'ALFX': QLineEdit(),
            'ALFY': QLineEdit(),
            'DX': QLineEdit(),
            'DY': QLineEdit(),
            'DPX': QLineEdit(),
            'DPY': QLineEdit(),
        }
        layout = QHBoxLayout()
        for label, widget in self.beta0_input.items():
            widget.setPlaceholderText(label)
            widget.setValidator(QDoubleValidator())
            layout.addWidget(QLabel(f'{label}:'))
            layout.addWidget(widget)
        self.setLayout(layout)

    def parse_beta0(self, f_path: str):
        """Parse 'BETA0' command which must be placed on its own line."""
        text = Path(f_path).read_text()
        match = re.search(
            r'^(?:[a-zA-Z][a-zA-Z0-9_.]*[ \t]*:[ \t]*)?BETA0[ \t]*,[ \t]*(?P<args>.+?);$',
            text,
            flags=re.MULTILINE | re.IGNORECASE
        )
        if match is None:
            logging.info(f'No BETA0 command found in {f_path!r}')
            return
        self.arguments.clear()
        for widget in self.beta0_input.values():
            widget.clear()
        for name, value in (x.split('=') for x in match.groupdict()['args'].split(',')):
            name = name.strip().upper()
            value = value.strip()
            self.arguments[name] = value
            self.beta0_input[name].setText(value)


class Canvas(FigureCanvasQTAgg):

    def __init__(self):
        self.fig = Figure(figsize=(14, 12))
        self.ax_lattice, self.ax_twiss, self.ax_pos = self.fig.subplots(nrows=3, sharex=True)
        super().__init__(self.fig)
        self.ax_pos.set_xlabel('s [m]')
        self.ax_pos.set_ylabel('Beam position [mm]')
        self.ax_twiss.set_ylabel('Beta functions [m]')


if __name__ == '__main__':
    app = QApplication(sys.argv[2:])
    window = LatticeExplorer(sys.argv[1])
    window.show()
    sys.exit(app.exec_())

