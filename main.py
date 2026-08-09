# -*- coding: utf-8 -*-
"""
تطبيق مساعدة المكفوفين - بايثون / Kivy
====================================
الفكرة: المستخدم (كفيف) بفتح التطبيق، بيسمع ترحيب صوتي، وبعدين بقدر
يعمل نقرة بأي مكان بالشاشة (مو محتاج يدور على زر بالضبط):

    - نقرة واحدة   -> كشف الأجسام والعوائق (شغال حالياً)
    - نقرتين       -> كشف العملات (قريباً)
    - ثلاث نقرات   -> التعرف على السيارات (قريباً)

كل شي Real-time عن طريق كاميرا الموبايل + تنبيه صوتي (TTS) بكل جسم منكشف.
"""

import os
import time

os.environ.setdefault("KIVY_NO_ARGS", "1")

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

import cv2
import numpy as np

from tts_helper import TTSHelper
from detector import ObjectDetector

# ---------------------------------------------------------------------------
# إعدادات عامة
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "object_detection.onnx")
LABELS_PATH = os.path.join(BASE_DIR, "models", "labels.txt")

TAP_WINDOW = 0.45          # الوقت المسموح بين النقرات لتحسب "نقرات متتالية" (ثانية)
DETECTION_INTERVAL = 1.2   # كل كم ثانية نعمل كشف جديد (تخفيف الحمل + عدم تكرار الصوت بسرعة)

tts = TTSHelper()


# ---------------------------------------------------------------------------
# الشاشة الرئيسية: تستقبل النقرات وتوجه المستخدم
# ---------------------------------------------------------------------------
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap_count = 0
        self._tap_event = None

        layout = FloatLayout()

        self.label = Label(
            text="مرحبا بك في التطبيق\n\n"
                 "نقرة واحدة: كشف الأجسام والعوائق\n"
                 "نقرتين: كشف العملات (قريباً)\n"
                 "ثلاث نقرات: التعرف على السيارات (قريباً)\n\n"
                 "اضغط بأي مكان بالشاشة",
            font_size="24sp",
            halign="center",
            valign="middle",
            size_hint=(1, 1),
        )
        self.label.bind(size=self._update_text_size)
        layout.add_widget(self.label)
        self.add_widget(layout)

    def _update_text_size(self, instance, value):
        instance.text_size = value

    def on_enter(self):
        # ترحيب صوتي أول ما تفتح الشاشة
        Clock.schedule_once(lambda dt: tts.speak(
            "مرحبا بك في التطبيق. "
            "اضغط نقرة واحدة لكشف الأجسام والعوائق. "
            "اضغط نقرتين لكشف العملات، قريباً. "
            "اضغط ثلاث نقرات للتعرف على السيارات، قريباً."
        ), 0.5)

    def on_touch_down(self, touch):
        self.tap_count += 1

        if self._tap_event:
            self._tap_event.cancel()
        self._tap_event = Clock.schedule_once(self._process_taps, TAP_WINDOW)

        return super().on_touch_down(touch)

    def _process_taps(self, dt):
        count = self.tap_count
        self.tap_count = 0

        if count == 1:
            self._go_to_model("object_detection")
        elif count == 2:
            tts.speak("كشف العملات لسا قيد التطوير، رح يتوفر قريباً")
        elif count >= 3:
            tts.speak("التعرف على السيارات لسا قيد التطوير، رح يتوفر قريباً")

    def _go_to_model(self, model_key):
        camera_screen = self.manager.get_screen("camera")
        camera_screen.set_model(model_key)
        self.manager.current = "camera"


# ---------------------------------------------------------------------------
# شاشة الكاميرا: بث حي + كشف Real-time + تنبيه صوتي
# ---------------------------------------------------------------------------
class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = None
        self.detector = None
        self.last_detection_time = 0
        self.last_announced = set()

        layout = FloatLayout()
        self.image_widget = Image(size_hint=(1, 0.85), pos_hint={"x": 0, "y": 0.15})
        layout.add_widget(self.image_widget)

        back_btn = Button(
            text="ارجع للقائمة الرئيسية (نقرتين هون)",
            size_hint=(1, 0.15),
            pos_hint={"x": 0, "y": 0},
            font_size="18sp",
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def set_model(self, model_key: str):
        self.model_key = model_key
        if model_key == "object_detection":
            if self.detector is None:
                self.detector = ObjectDetector(MODEL_PATH, LABELS_PATH)

    def on_enter(self):
        tts.speak("تم فتح الكاميرا. جاري كشف الأجسام والعوائق")
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_frame, 1.0 / 20.0)  # ~20 FPS للعرض

    def on_leave(self):
        Clock.unschedule(self.update_frame)
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        self.last_announced = set()

    def go_back(self, *args):
        self.manager.current = "home"

    def update_frame(self, dt):
        if self.capture is None:
            return
        ret, frame = self.capture.read()
        if not ret:
            return

        # عرض الصورة الحية بالواجهة
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        self.image_widget.texture = texture

        # الكشف Real-time - بس مش بكل فريم، كل DETECTION_INTERVAL ثانية
        now = time.time()
        if self.detector is not None and (now - self.last_detection_time) >= DETECTION_INTERVAL:
            self.last_detection_time = now
            detected = set(self.detector.detect(frame))

            # نحكي بس الأشياء الجديدة يلي ظهرت (مش نعيد نفس الشي كل ثانيتين)
            new_items = detected - self.last_announced
            if new_items:
                message = " و ".join(new_items)
                tts.speak(message)
            self.last_announced = detected


# ---------------------------------------------------------------------------
# التطبيق
# ---------------------------------------------------------------------------
class BlindAssistApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CameraScreen(name="camera"))
        return sm


if __name__ == "__main__":
    BlindAssistApp().run()
