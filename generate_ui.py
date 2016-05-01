

def main():
    from vkontakte_music import settings
    import os
    for filename in os.listdir(settings.QTDESIGNER_SOURCES):
        if not filename.endswith('.ui'):
            continue
        full_path = os.path.join(settings.QTDESIGNER_SOURCES, filename)
        target_filename = os.path.splitext(filename)[0] + '.py'
        target_filepath = os.path.join(settings.QTDESIGNER_GENERATED, target_filename)
        print full_path + ' >> ' + target_filepath
        os.system('pyside-uic {input} -o {output}'.format(input=full_path, output=target_filepath))

    import PySide

    pyside_path = os.path.dirname(PySide.__file__)
    resource_converter = os.path.join(pyside_path, 'pyside-rcc.exe')
    resources_path = os.path.join(settings.QTDESIGNER_SOURCES, 'resources.qrc')
    target_resources_path = os.path.join(settings.QTDESIGNER_GENERATED, 'resources_rc.py')

    print resources_path + ' >> ' + target_resources_path
    os.system('{0} {1} > {2}'.format(resource_converter, resources_path, target_resources_path))


if __name__ == '__main__':
    main()