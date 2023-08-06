import sys
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtGui import*
from PySide2.QtMultimedia import QSound


def analyse_code(contents: str) -> tuple:
    lines = contents.splitlines(keepends=True)
    # locate pyside_package_dir line index
    pkg_dir = 'os.path.abspath(os.path.dirname(__file__))'
    for index, line in enumerate(lines):
        if pkg_dir in line:
            break
    return lines, index, ' ' * (len(line.rstrip()) - len(line.strip()))


def insert_lines(contents: str) -> list:
    lines, position, indentation = analyse_code(contents)
    new_lines = (
        lines[position] + '\n' +
        indentation + '# add platforms plugin to PATH\n' +
        indentation + 'platforms_dir = ' +
        'os.path.join(pyside_package_dir, "plugins", "platforms")\n' +
        indentation +
        'os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_dir\n')
    lines[position] = new_lines
    return lines


def add_plugins_to_PATH(file_path):
    with open(file_path, encoding='utf-8') as f:
        contents = f.read()
    lines = insert_lines(contents)
    code = ''.join(lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)


def start_fix():
    import PySide2
    PySide2_init_module = PySide2.__file__
    add_plugins_to_PATH(PySide2_init_module)


start_fix()


class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setup()
        self.show()

    def setup(self):
        self.index = 0
        self.tips = ["我叫编程猫", "很高兴认识你", "很开心能一起学习Python"]
        self.icon = QIcon("images_cat/sit.png")
        self.setIcon(self.icon)
        self.setToolTip("使用鼠标点击我吧")
        self.activated.connect(self.process)
        self.sound1 = QSound("images_cat/sound1.wav")
        self.sound2 = QSound("images_cat/sound2.wav")
        self.icon2 = QIcon("images_cat/stand.png")
        self.timer = QTimer()
        self.icons = [f"images_cat/{i}.png" for i in range(0, 5)]
        self.icon_index = 0
        self.change_icon()
    
    def process(self, key):
        if key == self.Trigger:
            self.sound1.play()
            self.setIcon(self.icon)
        elif key == self.Context or key == self.MiddleClick:
            self.sound2.play()
            self.setIcon(self.icon2)
        self.setToolTip(self.tips[self.index % 3])
        self.index += 1

    def change_icon(self):
        self.setIcon(QIcon(self.icons[self.icon_index % 5]))
        self.icon_index += 1
        self.timer.singleShot(100, self.change_icon)


def main():
    app = QApplication(sys.argv)
    tray = Tray()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
