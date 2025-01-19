from setuptools import setup

APP = ['src/main.py']
DATA_FILES = ['src/Info.plist', 'src/entitlements.plist']
OPTIONS = {
    'argv_emulation': False,
    'plist': 'src/Info.plist',
    'packages': ['PyQt6'],
    'includes': [
        'Foundation',
        'AppKit',
        'objc',
        'Foundation.NSBundle',
        'Foundation.NSDictionary',
        'Foundation.NSWorkspace'
    ],
    'frameworks': [
        '/System/Library/Frameworks/Foundation.framework',
        '/System/Library/Frameworks/AppKit.framework'
    ],
    'resources': [],
    'arch': 'arm64',
}

setup(
    name="BuildBlock",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 