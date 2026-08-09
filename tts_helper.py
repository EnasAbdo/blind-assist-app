"""
وحدة تحويل النص إلى كلام - باستخدام صوت عربي أونلاين (Microsoft Edge TTS)
عن طريق مكتبة edge-tts، مع تشغيل كل جملة بعملية بايثون منفصلة
(fire-and-forget) لتفادي أي تعارض مع حلقة أحداث Kivy.

يتطلب اتصال إنترنت وقت الكلام.
"""

import sys
import subprocess
import tempfile
import os
import uuid
from kivy.utils import platform

PLYER_AVAILABLE = False
if platform in ("android", "ios"):
    try:
        from plyer import tts as plyer_tts
        PLYER_AVAILABLE = True
    except Exception:
        pass


class TTSHelper:
    def __init__(self, voice: str = "ar-SA-HamedNeural"):
        self.voice = voice

    def speak(self, text: str):
        if not text:
            return

        print(f"[TTS] >>> بدء: '{text}'")
        try:
            if PLYER_AVAILABLE:
                print("[TTS] استخدام plyer")
                from plyer import tts as plyer_tts
                plyer_tts.speak(message=text)
            else:
                out_file = os.path.join(
                    tempfile.gettempdir(), f"tts_{uuid.uuid4().hex}.mp3"
                )
                script = (
                    "import edge_tts, asyncio, playsound\n"
                    "async def main():\n"
                    f"    c = edge_tts.Communicate({text!r}, {self.voice!r})\n"
                    f"    await c.save({out_file!r})\n"
                    "asyncio.run(main())\n"
                    f"playsound.playsound({out_file!r})\n"
                )
                subprocess.Popen(
                    [sys.executable, "-c", script],
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
                print("[TTS] تم إطلاق عملية النطق (edge-tts)")
        except Exception as e:
            print(f"[خطأ TTS]: {repr(e)}")
        print("[TTS] <<< خلص")
