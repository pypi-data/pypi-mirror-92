import logging
import sys

from PySide2.QtWidgets import QApplication
from famegui.mainwindow import MainWindow


def run():
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication([])

    app.setOrganizationDomain("dlr.de")
    app.setOrganizationName("DLR")
    app.setApplicationName("FAME Gui")
    app.setApplicationVersion("0.2")
    app.setApplicationDisplayName("{} (version {})".format(
        app.applicationName(), app.applicationVersion()))

    main_wnd = MainWindow()
    main_wnd.resize(1200, 1000)
    main_wnd.show()

    if len(sys.argv) > 1:
        main_wnd.load_scenario_file(sys.argv[1])

    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
