from PIL import Image, ImageQt
import random
from PySide6.QtWidgets import*
from PySide6.QtCore import*
from PySide6.QtGui import*
import sys


class Fix:
    def analyse_code(self, contents: str) -> tuple:
        lines = contents.splitlines(keepends=True)
        # locate pyside_package_dir line index
        pkg_dir = 'os.path.abspath(os.path.dirname(__file__))'
        for index, line in enumerate(lines):
            if pkg_dir in line:
                break

        # return lines, line index, indentation
        return lines, index, ' ' * (len(line.rstrip()) - len(line.strip()))

    def insert_lines(self, contents: str) -> list:
        lines, position, indentation = self.analyse_code(contents)
        new_lines = (
                lines[position] + '\n' +
                indentation + '# add platforms plugin to PATH\n' +
                indentation + 'platforms_dir = ' +
                'os.path.join(pyside_package_dir, "plugins", "platforms")\n' +
                indentation +
                'os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_dir\n')

        # insert lines
        lines[position] = new_lines
        return lines

    def add_plugins_to_PATH(self, file_path):
        # open __init__.py
        with open(file_path, encoding='utf-8') as f:
            contents = f.read()

        # insert lines
        lines = self.insert_lines(contents)

        # save changes to __init__.py
        code = ''.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

    def start_fix(self):
        """Glitch fixing entry."""
        import PySide6
        PySide6_init_module = PySide6.__file__
        self.add_plugins_to_PATH(PySide6_init_module)


fix = Fix()
fix.start_fix()


class Pic:
    def __init__(self):
        self.color_out = self.randomColor()
        self.board = Image.new("HSV", (500, 500), self.color_out)
        self.randx = random.randint(0, 9) * 50
        self.randy = random.randint(0, 9) * 50
        self.gen_pic()

    def randomColor(self):
        color = (
            random.randint(0, 360),
            random.randint(0, 255), 255
        )
        return color

    def color_in(self):
        self.res = list(self.color_out)
        self.res[0] += random.randint(10, 15)
        self.res = tuple(self.res)
        return self.res

    def colorBright(self):
        self.res = list(self.color_out)
        self.res[2] -= random.randint(0, 15)
        self.res = tuple(self.res)
        return self.res

    def gen_pic(self):
        for y in range(0, 500, 50):
            for x in range(0, 500, 50):
                if x == self.randx and y == self.randy:
                    new_block = Image.new("HSV", (50, 50), self.color_in())
                    self.board.paste(new_block, (x, y))
                else:
                    new_block = Image.new("HSV", (50, 50), self.colorBright())
                    self.board.paste(new_block, (x, y))


class OpsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.setup()

    def setup(self):
        self.new_pic()
        self.width = self.img.width()
        self.height = self.img.height()
        self.resize(self.width, self.height)
        self.painter = QPainter()

    def new_pic(self):
        self.pic = Pic()
        self.img = ImageQt.ImageQt(self.pic.board.convert("RGBA"))
        self.img = QPixmap.fromImage(self.img)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.img)
        self.painter.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        tar_x = self.pic.randx
        tar_y = self.pic.randy
        if tar_x <= x <= tar_x + 50 and tar_y <= y <= tar_y + 50:
            QMessageBox.about(self, "恭喜", "correct")
            self.new_pic()
            self.update()
        else:
            QMessageBox.warning(self, "注意", "wrong")


def main():
    app = QApplication(sys.argv)
    window = OpsWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
