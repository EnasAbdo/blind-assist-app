"""
سكريبت تحويل موديل YOLOv8 المدرب (best.pt) إلى صيغة ONNX
عشان يشتغل بكفاءة وبسرعة Real-time على الموبايل عن طريق cv2.dnn
(وهاد أضمن وأسهل بالتغليف لأندرويد من TFLite، لأن OpenCV مدعوم بشكل
كامل مع Buildozer/python-for-android، بعكس tflite-runtime).

الاستخدام:
    pip install ultralytics
    python export_to_onnx.py --model best.pt --imgsz 320

بعد التصدير:
1) رح تلاقي ملف "best.onnx" بنفس مجلد best.pt
2) انسخه إلى: blind_assist_app/models/object_detection.onnx
3) انسخ أسماء الأصناف المطبوعة بالأسفل إلى: blind_assist_app/models/labels.txt
   (سطر لكل صنف، بنفس الترتيب بالضبط)
"""

import argparse
from ultralytics import YOLO


def export_model(model_path: str, imgsz: int = 320):
    print(f"[*] تحميل الموديل من: {model_path}")
    model = YOLO(model_path)

    print(f"[*] تصدير إلى ONNX بحجم صورة {imgsz}x{imgsz} ...")
    exported_path = model.export(format="onnx", imgsz=imgsz, simplify=True, opset=12)

    print(f"[+] تم التصدير بنجاح: {exported_path}")
    print("[!] انسخ الملف الناتج إلى: blind_assist_app/models/object_detection.onnx")

    print("\n[*] أصناف الموديل (انسخها لملف models/labels.txt بنفس الترتيب):")
    for idx, name in model.names.items():
        print(f"{idx}: {name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="مسار ملف best.pt")
    parser.add_argument("--imgsz", type=int, default=320, help="حجم الصورة للتصدير")
    args = parser.parse_args()

    export_model(args.model, args.imgsz)
