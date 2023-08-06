

import sys
import argparse
from PyQt5 import QtWidgets
import filep.main_window


def main():
    argument_parser = argparse.ArgumentParser()
    app = QtWidgets.QApplication(sys.argv)
    main_window = filep.main_window.MainWindow()
    app.aboutToQuit.connect(main_window.on_about_to_quit)
    app.setQuitOnLastWindowClosed(False)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

