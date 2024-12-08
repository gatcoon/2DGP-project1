def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    import sys
    import os

    try:
        # PyInstaller에서 사용하는 MEIPASS 경로
        base_path = sys._MEIPASS
    except AttributeError:
        # 개발 환경에서의 기본 경로
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
