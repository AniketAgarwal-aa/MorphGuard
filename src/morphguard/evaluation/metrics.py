from __future__ import annotations
import numpy as np
def binary_metrics(y_true,y_score,threshold=.5):
    from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,average_precision_score,confusion_matrix
    y_true=np.asarray(y_true); y_score=np.asarray(y_score); y_pred=(y_score>=threshold).astype(int); tn,fp,fn,tp=confusion_matrix(y_true,y_pred,labels=[0,1]).ravel()
    return {"threshold":threshold,"accuracy":accuracy_score(y_true,y_pred),"precision":precision_score(y_true,y_pred,zero_division=0),"recall":recall_score(y_true,y_pred,zero_division=0),"specificity":tn/(tn+fp) if tn+fp else 0,"f1":f1_score(y_true,y_pred,zero_division=0),"roc_auc":roc_auc_score(y_true,y_score) if len(set(y_true))==2 else None,"pr_auc":average_precision_score(y_true,y_score) if len(set(y_true))==2 else None,"confusion_matrix":[[int(tn),int(fp)],[int(fn),int(tp)]]}
