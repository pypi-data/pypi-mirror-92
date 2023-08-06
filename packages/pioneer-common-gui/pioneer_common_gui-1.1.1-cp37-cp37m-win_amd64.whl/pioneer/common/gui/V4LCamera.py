from pioneer.common.gui import Array, Product

from PyQt5.QtCore import pyqtSignal, pyqtProperty, pyqtSlot

import cv2
import threading

class V4LCamera(Array.ArrayUByte3):
    def __init__(self, parent = None):
        super(V4LCamera, self).__init__(parent)
        self._assynchronous = True
        self._captureID = 0
        self._camera = None
        self._thread = None
        self._lock = threading.Lock()
        self._received_images = []

    captureIDChanged = pyqtSignal()

    @pyqtProperty(int, notify = captureIDChanged)
    def captureID(self):
        return self._captureID

    @captureID.setter
    def captureID(self, v):
        if Product.assign_input(self, "captureID", v):
            if self._camera is not None:
                self._camera.release()
            self._camera = None

    assynchronousChanged = pyqtSignal()
    @pyqtProperty(bool, notify = assynchronousChanged)
    def assynchronous(self):
        return self._assynchronous

    @assynchronous.setter
    def assynchronous(self, v):
        if Product.assign_input(self, "assynchronous", v):
            if self._camera is not None:
                self._camera.release()
            self._camera = None

    def _append_image(self, image):
        self._received_images.append(image)
        self.makeDirty()

    @pyqtSlot(int)
    def refresh(self, timeout_ms):
        if self._camera is None:
            self._configure_camera()

        rv, image = self._camera.read()
        if rv:
            self._append_image(image)

    def _configure_camera(self):
        if self._thread is not None:
            tmp = self._assynchronous
            self._assynchronous = False
            self._thread.join()
            self._assynchronous = tmp
            self._thread = None

        self._camera = cv2.VideoCapture(self._captureID)

        if self._assynchronous:
            def camera_thread():
                while self._assynchronous:
                    rv, image = self._camera.read()
                    if rv:
                        with self._lock:
                            self._append_image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                            if len(self._received_images) > 10:
                                self._received_images = self._received_images[-10:]

            self._thread = threading.Thread(target=camera_thread, args=())
            self._thread.start()



    def _update(self):
        if self._camera is None:
            self._configure_camera()

        with self._lock:
            if self._received_images:
                self.ndarray = self._received_images[-1]
                self._received_images = []




