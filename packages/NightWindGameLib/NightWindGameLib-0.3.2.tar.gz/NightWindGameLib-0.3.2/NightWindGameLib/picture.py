import sys
from PySide6.QtWidgets import*
from PySide6.QtCore import*
from PySide6.QtGui import*


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


class Painter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup()
        self.show()

    def setup(self):
        self.img = None
        self.material = None
        self.copy_img = None
        self.painter = QPainter()

    def paintEvent(self, event):
        if self.img:
            self.painter.begin(self)
            self.painter.drawPixmap(0, 0, self.img)
            self.painter.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        # print(x, y)
        if self.img and self.material:
            self.painter.begin(self.img)
            w = self.material.width() // 2
            h = self.material.height() // 2
            self.painter.drawPixmap(x - w, y - h, self.material)
            self.painter.end()
            # self.img.save("result.png")
            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            file, _ = QFileDialog.getOpenFileName(caption="选择原图", filter="(*.jpg *.png)")
            if file:
                self.img = QPixmap(file)
                self.copy_img = self.img.copy()
                width = self.img.width()
                height = self.img.height()
                self.resize(width, height)

        elif event.key() == Qt.Key_2:
            file, _ = QFileDialog.getOpenFileName(caption="选择素材", filter="(*.jpg *.png)")
            if file:
                self.material = QPixmap(file)
                self.setCursor(QCursor(self.material))

        elif event.key() == Qt.Key_3:
            if self.img:
                file, _ = QFileDialog.getSaveFileName(caption="保存结果", filter="(*.png *.jpg)")
                if file:
                    self.img.save(file)

        elif event.key() == Qt.Key_4:
            if self.img and self.copy_img:
                self.img = self.copy_img.copy()
                self.update()


def main():
    app = QApplication(sys.argv)
    window = Painter()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
