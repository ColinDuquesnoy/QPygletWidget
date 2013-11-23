QPygletWidget
=============

A widget to easily display **one** pyglet scene in a PySide/Qt application.

This has been tested on Ubuntu 12.04, Windows XP and Windows 7.

License
---------
There is no license as this is more a reminder than anything else.

You are free to use this file without any restrictions. 

Requirements
-----------------

- Python 2.7
- PySide


Usage
--------
Here is a simple example:

```python
from qpygletwidget import QPygletWidget


class MyPygletWidget(QPygletWidget):
    def on_init(self):
        self.sprite = pyglet.sprite.Sprite(pyglet.resource.image("logo.png"))
        self.label = pyglet.text.Label(
            text="This is a pyglet label rendered in a Qt widget :)")
        self.setMinimumSize(QSize(640, 480))

    def on_draw(self):
        self.sprite.draw()
        self.label.draw()


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    widget = MyPygletWidget()
    window.setCentralWidget(widget)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
```

You can run the script by issuing the following command::

```bash
  python qpygletwidget.py
```

If you are using PyQt instead of PySide, the port should be really easy as the only thing 
you will probably have to do is to replace **from PySide** by **from PyQt4**


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/ColinDuquesnoy/qpygletwidget/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

