#-------------------------------------------------------------------------------
# Name:        Utils
# Purpose:
#
# Author:      Elbar
#
# Created:     01/03/2012
# Copyright:   (c) USER 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from PyQt5 import QtWidgets
from logging import Formatter
from logging.handlers import RotatingFileHandler

def errorMessageBox(msg):

    QtWidgets.QMessageBox.critical(None,"Error",msg,QtWidgets.QMessageBox.Ok,QtWidgets.QMessageBox.NoButton)

def set_up_logger_file(logger,file_name):

    fh = RotatingFileHandler(file_name, 'a', 65536, 7)
    frm = Formatter("%(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s\t%(threadName)s\t%(message)s")
    fh.setFormatter(frm)
    logger.addHandler(fh)
