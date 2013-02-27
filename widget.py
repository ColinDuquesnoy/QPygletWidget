"""
This module contains the definiton of a pyglet widget for a 
PySide application: QPygletWidget

It also provides a basic usage example.
"""
import sys
from PySide.QtCore import QSize
import pyglet
pyglet.options['shadow_window'] = False
pyglet.options['debug_gl'] = False
from pyglet import gl
from PySide import QtCore, QtGui, QtOpenGL


class ObjectSpace(object):
    """ Object space mocker """
    def __init__(self):
        # Textures and buffers scheduled for deletion the next time this
        # object space is active.
        self._doomed_textures = []
        self._doomed_buffers = []


class Context(object):
    """
    pyglet.gl.Context mocker. This is used to make pyglet believe that a valid
    context has already been setup. (Qt takes care of creating the open gl
    context)

    _Most of the methods are empty, there is just the minimum required to make
    it look like a duck..._
    """
    # define the same class attribute as pyglet.gl.Context
    CONTEXT_SHARE_NONE = None
    CONTEXT_SHARE_EXISTING = 1
    _gl_begin = False
    _info = None
    _workaround_checks = [
        ('_workaround_unpack_row_length',
         lambda info: info.get_renderer() == 'GDI Generic'),
        ('_workaround_vbo',
         lambda info: info.get_renderer().startswith('ATI Radeon X')),
        ('_workaround_vbo_finish',
         lambda info: ('ATI' in info.get_renderer() and
                       info.have_version(1, 5) and
                       sys.platform == 'darwin'))]

    def __init__(self, context_share=None):
        """
        Setup workaround attr and object spaces (again to mock what is done in
        pyglet context)
        """
        self.object_space = ObjectSpace()
        for attr, check in self._workaround_checks:
            setattr(self, attr, None)

    def __repr__(self):
        return '%s()' % self.__class__.__name__

    def set_current(self):
        pass

    def destroy(self):
        pass

    def delete_texture(self, texture_id):
        pass

    def delete_buffer(self, buffer_id):
        pass


class QPygletWidget(QtOpenGL.QGLWidget):
    """
    A simple pyglet widget.

    User can subclass this widget and implement the following methods:
        - on_init: called when open gl has been initialised
        - on_update: called every dt.
        - on_draw: called when paintGL is executed
        - on_resize: called when resizeGL is executed
    """
    def __init__(self, parent=None,
                 clear_color=(0.0, 0.0, 0.0, 1.0),
                 frame_time=32,
                 dt=16):
        """
        :param clear_color: The widget clear color
        :type clear_color: tuple(r, g, b, a)

        :param frame_time: The desired frame time [ms]
        :type: frame_time: int

        :param dt: The desired update rate [ms]
        :type: dt: int
        """
        QtOpenGL.QGLWidget.__init__(self, parent)

        # init members
        self._clear_color = clear_color
        self._dt = dt
        self.update_timer = QtCore.QTimer()
        self.draw_timer = QtCore.QTimer()

        # configure draw and update timers
        self.update_timer.setInterval(dt)
        self.update_timer.timeout.connect(self._update)
        self.draw_timer.setInterval(frame_time)
        self.draw_timer.timeout.connect(self.updateGL)

        # start timers
        self.update_timer.start()
        self.draw_timer.start()

    def _update(self):
        """
        Calls on_update with the choosen dt
        """
        self.on_update(self._dt)

    def on_init(self):
        """
        Lets the user initialise himself
        """
        pass

    def on_draw(self):
        """
        Lets the user draw his scene
        """
        pass

    def on_update(self, dt):
        """
        Lets the user draw his scene
        """
        pass

    def on_resize(self, w, h):
        """
        Lets the user handle the widget resize event. By default, this method
        resizes the view to the widget size.
        """
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, w, 0, h, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def initializeGL(self):
        """
        Initialises open gl:
            - create a mock context to fool pyglet
            - setup various opengl rule (only the clear color atm)
        """
        gl.current_context = Context()
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.on_init()

    def resizeGL(self, w, h):
        """
        Resizes the gl camera to match the widget size.
        """
        self.on_resize(w, h)

    def paintGL(self):
        """
        Clears the back buffer than calls the on_draw method
        """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.on_draw()


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
