import sys
import os

if hasattr(sys, '_MEIPASS'):
    DB_PATH = os.path.join(sys._MEIPASS, 'database', 'rma.db')
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'rma.db')