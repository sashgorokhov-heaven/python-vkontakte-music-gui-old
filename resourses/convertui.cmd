@echo off
C:\Python33\Scripts\pyside-uic.exe loadform.ui -o ..\modules\forms\downloadform\ui.py
C:\Python33\Scripts\pyside-uic.exe mainform.ui -o ..\modules\forms\mainform\ui.py
C:\Python33\Scripts\pyside-uic.exe audiowidget.ui -o ..\modules\forms\mainform\components\audiolist\components\audiolistitemwidget\ui.py
C:\Python33\Scripts\pyside-uic.exe audiodownloadwidget.ui -o ..\modules\forms\downloadform\components\audiolist\components\audiolistitemwidget\ui.py