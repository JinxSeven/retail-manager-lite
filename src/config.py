import sys
import os
import shutil

if hasattr(sys, '_MEIPASS'):
    DB_PATH = os.path.join(sys._MEIPASS, 'database', 'rma.db')
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'rma.db')

DB_NAME = "rma.db"

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_appdata_dir():
    base = os.getenv("APPDATA")
    app_dir = os.path.join(base, "RetailManagerLite")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

def get_db_path():
    db_dst = os.path.join(get_appdata_dir(), DB_NAME)

    if not os.path.exists(db_dst):
        db_src = resource_path(os.path.join("database", DB_NAME))
        shutil.copyfile(db_src, db_dst)

    return db_dst