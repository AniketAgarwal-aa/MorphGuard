from __future__ import annotations
import cv2, numpy as np

def extract_features(rgb: np.ndarray) -> dict[str,np.ndarray]:
    """Extract LBP, HOG, GLCM and statistics. Optional dependencies fail clearly."""
    try:
        from skimage.feature import local_binary_pattern, hog, graycomatrix, graycoprops
        from skimage.measure import shannon_entropy
    except ImportError as exc: raise RuntimeError("Install scikit-image for feature extraction") from exc
    gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    lbp=local_binary_pattern(gray,8,1,method="uniform"); lbp_hist=np.histogram(lbp,bins=np.arange(11),range=(0,10),density=True)[0]
    h=hog(gray,orientations=9,pixels_per_cell=(16,16),cells_per_block=(2,2),block_norm="L2-Hys")
    glcm=graycomatrix(gray,distances=[1,2],angles=[0,np.pi/4],levels=256,symmetric=True,normed=True)
    glcm_features=np.array([graycoprops(glcm,p).mean() for p in ("contrast","dissimilarity","homogeneity","energy","correlation")])
    edges=cv2.Canny(gray,80,160); stats=np.array([gray.mean(),gray.std(),shannon_entropy(gray),edges.mean()/255])
    return {"lbp":lbp_hist,"hog":h,"glcm":glcm_features,"stats":stats,"combined":np.concatenate((lbp_hist,h,glcm_features,stats))}
