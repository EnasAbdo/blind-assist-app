# سكريبت بسيط لاختبار الصوت لحاله - يساعدنا نتأكد المشكلة انحلت
# شغله بـ: python test_tts.py

import pyttsx3
import time

for i in range(3):
    print(f"محاولة رقم {i+1} ...")
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(f"هذه محاولة رقم {i+1}")
    engine.runAndWait()
    engine.stop()
    del engine
    time.sleep(1)

print("خلصت -- هل سمعت الأصوات التلاتة؟")
