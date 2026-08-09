"""
وحدة الكشف عن الأجسام (Object Detection) باستخدام موديل YOLOv8
بصيغة ONNX، وتشغيله عن طريق cv2.dnn (جزء من OpenCV).

ليش ONNX + cv2.dnn وليس TFLite؟
لأن OpenCV مدعوم بشكل كامل وموثوق مع Buildozer/python-for-android
(أصلاً مستخدمينه لفتح الكاميرا بالتطبيق)، بعكس tflite-runtime أو
tensorflow اللي ما إلهم دعم رسمي مستقر لتطبيقات بايثون على أندرويد.
"""

import os
import numpy as np
import cv2


class ObjectDetector:
    def __init__(self, model_path: str, labels_path: str,
                 img_size: int = 320, conf_threshold: float = 0.45,
                 nms_threshold: float = 0.45):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ملف الموديل مش موجود: {model_path}")
        if not os.path.exists(labels_path):
            raise FileNotFoundError(f"ملف الأصناف مش موجود: {labels_path}")

        self.img_size = img_size
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold

        with open(labels_path, "r", encoding="utf-8") as f:
            self.labels = [line.strip() for line in f if line.strip()]

        self.net = cv2.dnn.readNetFromONNX(model_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def detect(self, frame):
        """
        بتاخد فريم من الكاميرا وبترجع لائحة بأسماء الأجسام المكتشفة
        (بدون تكرار) اللي تجاوزت حد الثقة، بعد تطبيق Non-Max Suppression.
        """
        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            frame, scalefactor=1 / 255.0,
            size=(self.img_size, self.img_size),
            swapRB=True, crop=False
        )
        self.net.setInput(blob)
        output = self.net.forward()  # الشكل المتوقع: (1, 4+num_classes, num_boxes)

        output = np.squeeze(output)  # -> (4+num_classes, num_boxes)
        boxes_raw = output[:4, :]
        scores_raw = output[4:, :]

        class_ids = np.argmax(scores_raw, axis=0)
        confidences = np.max(scores_raw, axis=0)

        # طباعة تشخيصية مؤقتة: أعلى نسبة ثقة شافها الموديل بهالفريم
        # (تساعدنا نعرف إذا المشكلة بحد الثقة أو الموديل مش شايف شي أصلاً)
        best_idx = int(np.argmax(confidences))
        best_conf = float(confidences[best_idx])
        best_label = self.labels[int(class_ids[best_idx])] if int(class_ids[best_idx]) < len(self.labels) else "?"
        print(f"[تشخيص] أعلى ثقة: {best_label} = {best_conf:.3f} (حد القبول: {self.conf_threshold})")

        keep = confidences >= self.conf_threshold
        if not np.any(keep):
            return []

        class_ids = class_ids[keep]
        confidences = confidences[keep]
        boxes_kept = boxes_raw[:, keep]

        scale_x, scale_y = w / self.img_size, h / self.img_size
        cx, cy, bw, bh = boxes_kept
        x = (cx - bw / 2) * scale_x
        y = (cy - bh / 2) * scale_y
        bw = bw * scale_x
        bh = bh * scale_y
        nms_boxes = np.stack([x, y, bw, bh], axis=1).tolist()

        indices = cv2.dnn.NMSBoxes(
            nms_boxes, confidences.tolist(),
            self.conf_threshold, self.nms_threshold
        )

        detected = set()
        if len(indices) > 0:
            for i in np.array(indices).flatten():
                cid = int(class_ids[i])
                if cid < len(self.labels):
                    detected.add(self.labels[cid])

        return list(detected)
