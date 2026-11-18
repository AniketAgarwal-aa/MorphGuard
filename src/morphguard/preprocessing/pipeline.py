from __future__ import annotations
from dataclasses import dataclass, asdict
import cv2, numpy as np

@dataclass
class QualityReport:
    blur_variance: float
    brightness: float
    contrast: float
    suitable: bool
    warnings: list[str]
    def as_dict(self): return asdict(self)

class FacePreprocessor:
    """OpenCV Haar face detector with deliberately conservative fallbacks."""
    def __init__(self, image_size=224, clahe=False):
        self.image_size=image_size; self.clahe=clahe
        cascade=cv2.data.haarcascades+"haarcascade_frontalface_default.xml"
        self.detector=cv2.CascadeClassifier(cascade)
    def load(self, source):
        if isinstance(source, (str, bytes)):
            img=cv2.imread(str(source), cv2.IMREAD_COLOR)
        else: img=cv2.imdecode(np.frombuffer(source.read(),np.uint8),cv2.IMREAD_COLOR)
        if img is None or img.size == 0: raise ValueError("Invalid or unsupported image")
        return img
    def detect(self, bgr):
        gray=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
        faces=self.detector.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(40,40))
        return sorted([tuple(map(int,x)) for x in faces],key=lambda b:b[2]*b[3],reverse=True)
    def crop(self,bgr,box):
        x,y,w,h=box; pad=int(.15*max(w,h)); return bgr[max(0,y-pad):y+h+pad,max(0,x-pad):x+w+pad]
    def quality(self,bgr,face_box=None):
        region=self.crop(bgr,face_box) if face_box else bgr; gray=cv2.cvtColor(region,cv2.COLOR_BGR2GRAY)
        blur=float(cv2.Laplacian(gray,cv2.CV_64F).var()); brightness=float(gray.mean()); contrast=float(gray.std()); warns=[]
        if blur<50: warns.append("Image appears blurred")
        if brightness<45 or brightness>220: warns.append("Brightness is outside the recommended range")
        if min(region.shape[:2])<80: warns.append("Face/image resolution is low")
        return QualityReport(blur,brightness,contrast,not warns,warns)
    def transform(self,bgr,face_box=None):
        image=self.crop(bgr,face_box) if face_box else bgr
        image=cv2.resize(image,(self.image_size,self.image_size),interpolation=cv2.INTER_AREA)
        rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        return rgb
