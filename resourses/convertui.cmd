@echo off
C:\Python34\Scripts\pyside-uic.exe loadform.ui -o ..\modules\forms\downloadform\ui.py
C:\Python34\Scripts\pyside-uic.exe mainform.ui -o ..\modules\forms\mainform\ui.py
C:\Python34\Scripts\pyside-uic.exe audiolistitemwidget.ui -o ..\modules\forms\mainform\components\audiolist\components\audiolistitemwidget\ui.py
C:\Python34\Scripts\pyside-uic.exe audiodownloadwidget.ui -o ..\modules\forms\downloadform\components\audiolist\components\audiolistitemwidget\ui.py