#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass

from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QSizePolicy)
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette


@dataclass
class Thumb:
	"""Thumb class which holds information about a thumb.
	"""
	value: int
	rect: QRect
	pressed: bool

class QtRangeSlider(QWidget):
	"""QtRangeSlider is a class which implements a slider with 2 thumbs.
	"""
	HEIGHT = 30
	WIDTH = 120
	THUMB_WIDTH = 16
	THUMB_HEIGHT = 16
	TRACK_HEIGHT = 3
	TRACK_COLOR = QColor(0xc7, 0xc7, 0xc7)
	TRACK_FILL_COLOR = QColor(0x01, 0x81, 0xff)
	TRACK_PADDING = THUMB_WIDTH // 2 + 5

	left_thumb_value_changed = pyqtSignal(int)
	right_thumb_value_changed = pyqtSignal(int)

	def __init__(self, parent, left_value, right_value, left_thumb_value=0, right_thumb_value=None):
		super().__init__(parent)

		self.setSizePolicy(
			QSizePolicy.MinimumExpanding,
			QSizePolicy.MinimumExpanding
		)

		self._left_value = left_value
		self._right_value = right_value

		self._left_thumb = Thumb(left_thumb_value, None, False)
		_right_thumb_value = right_thumb_value if right_thumb_value is not None \
			else self._right_value
		if _right_thumb_value < left_thumb_value + 1:
			raise ValueError("Right thumb value is less or equal left thumb value.")
		self._right_thumb = Thumb(_right_thumb_value, None, False)

		self._canvas_width = None

		parent_palette = parent.palette()
		self._background_color = parent_palette.color(QPalette.Window)
		self._base_color = parent_palette.color(QPalette.Base)
		self._button_color = parent_palette.color(QPalette.Button)
		self._border_color = parent_palette.color(QPalette.Mid)


	def sizeHint(self):
		return QSize(self.HEIGHT, self.WIDTH)

	def paintEvent(self, unused_e):
		del unused_e
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		self._canvas_width = painter.device().width()
		canvas_height = painter.device().height()

		self.__draw_track(self._canvas_width, canvas_height, painter)
		self.__draw_track_fill(self._canvas_width, canvas_height, painter)
		self.__draw_left_thumb(self._canvas_width, canvas_height, painter)
		self.__draw_right_thumb(self._canvas_width, canvas_height, painter)

		painter.end()

	def __get_track_y_position(self, canvas_height):
		return canvas_height // 2 - self.TRACK_HEIGHT // 2

	def __draw_track(self, canvas_width, canvas_height, painter):
		brush = QBrush()
		brush.setColor(self.TRACK_COLOR)
		brush.setStyle(Qt.SolidPattern)

		rect = QRect(self.TRACK_PADDING, self.__get_track_y_position(canvas_height), \
			canvas_width - 2 * self.TRACK_PADDING, self.TRACK_HEIGHT)
		painter.fillRect(rect, brush)

	def __draw_track_fill(self, canvas_width, canvas_height, painter):
		brush = QBrush()
		brush.setColor(self.TRACK_FILL_COLOR)
		brush.setStyle(Qt.SolidPattern)

		available_width = canvas_width - 2 * self.TRACK_PADDING
		x1 = self._left_thumb.value / self._right_value * available_width + self.TRACK_PADDING
		x2 = self._right_thumb.value / self._right_value * available_width + self.TRACK_PADDING
		rect = QRect(x1, self.__get_track_y_position(canvas_height), \
			x2 - x1, self.TRACK_HEIGHT)
		painter.fillRect(rect, brush)

	def __draw_thumb(self, x, y, painter):
		brush = QBrush()
		brush.setColor(self._base_color)
		brush.setStyle(Qt.SolidPattern)

		pen = painter.pen()
		pen.setColor(self._border_color)
		painter.setPen(pen)

		painter.setBrush(brush)

		thumb_rect = QRect(x - self.THUMB_WIDTH // 2 + self.TRACK_PADDING, \
			y + self.TRACK_HEIGHT // 2 - self.THUMB_HEIGHT // 2, self.THUMB_WIDTH, self.THUMB_HEIGHT)
		painter.drawEllipse(thumb_rect)
		return thumb_rect

	def __draw_right_thumb(self, canvas_width, canvas_height, painter):
		available_width = canvas_width - 2 * self.TRACK_PADDING
		x = self._right_thumb.value / self._right_value * available_width
		y = self.__get_track_y_position(canvas_height)
		self._right_thumb.rect = self.__draw_thumb(x, y, painter)

	def __draw_left_thumb(self, canvas_width, canvas_height, painter):
		available_width = canvas_width - 2 * self.TRACK_PADDING
		x = round(self._left_thumb.value / self._right_value * available_width)
		y = self.__get_track_y_position(canvas_height)
		self._left_thumb.rect = self.__draw_thumb(x, y, painter)

	def set_left_thumb_value(self, value):
		if value < 0 or value > self._right_thumb.value - 1:
			return
		if value == self._left_thumb.value:
			# nothing to update
			return
		self._left_thumb.value = value
		self.left_thumb_value_changed.emit(value)
		self.repaint()

	def set_right_thumb_value(self, value):
		if value > self._right_value or value < self._left_thumb.value + 1:
			return
		if value == self._right_thumb.value:
			# nothing to update
			return
		self._right_thumb.value = value
		self.right_thumb_value_changed.emit(value)
		self.repaint()

	# override Qt event
	def mousePressEvent(self, event):
		if self._left_thumb.rect.contains(event.x(), event.y()):
			self._left_thumb.pressed = True
		if self._right_thumb.rect.contains(event.x(), event.y()):
			self._right_thumb.pressed = True
		super().mousePressEvent(event)

	# override Qt event
	def mouseReleaseEvent(self, event):
		self._left_thumb.pressed = False
		self._right_thumb.pressed = False
		super().mousePressEvent(event)

	# pylint: disable=no-self-use
	def __get_thumb_value(self, x, canvas_width, right_value):
		return round(x / canvas_width * right_value)

	# override Qt event
	def mouseMoveEvent(self, event):
		if self._left_thumb.pressed:
			new_val = self.__get_thumb_value(event.x(), self._canvas_width, self._right_value)
			self.set_left_thumb_value(new_val)
			return

		if self._right_thumb.pressed:
			new_val = self.__get_thumb_value(event.x(), self._canvas_width, self._right_value)
			self.set_right_thumb_value(new_val)

	def get_left_thumb_value(self):
		return self._left_thumb.value

	def get_right_thumb_value(self):
		return self._right_thumb.value
