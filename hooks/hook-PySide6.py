from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Include all PySide6 modules
hiddenimports = collect_submodules('PySide6')

# Include Qt plugins and translations
datas = collect_data_files('PySide6', include_py_files=True)

# Include SQLite driver
datas += [('venv/lib/python3.11/site-packages/PySide6/plugins/sqldrivers/libqsqlite.so', 'PySide6/plugins/sqldrivers')]