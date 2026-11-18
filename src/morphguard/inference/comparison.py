"""Exploratory feature comparison helpers; never interpreted as detector scores."""
from __future__ import annotations
import numpy as np
def compare_vectors(a: np.ndarray, b: np.ndarray) -> dict:
    a=np.asarray(a,dtype=float).ravel(); b=np.asarray(b,dtype=float).ravel()
    if a.shape != b.shape: raise ValueError(f'feature dimensions differ: {a.shape[0]} vs {b.shape[0]}')
    if not (np.isfinite(a).all() and np.isfinite(b).all()): raise ValueError('feature vectors contain non-finite values')
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b)); cosine=float(np.dot(a,b)/(na*nb)) if na and nb else None
    diff=np.abs(a-b)
    return {'dimensions':int(a.size),'cosine_similarity':cosine,'absolute_difference_mean':float(diff.mean()),'absolute_difference_max':float(diff.max()),'finite':True}
