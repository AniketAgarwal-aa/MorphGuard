"""Train conventional models only from precomputed feature shards; test data is never fit."""
import argparse, glob, json
from pathlib import Path
import numpy as np, joblib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
p=argparse.ArgumentParser();p.add_argument("feature_dir",type=Path);p.add_argument("--manifest",type=Path,required=True,help="reviewed label manifest; only approved rows are permitted");p.add_argument("--model",choices=["lbp_svm","hog_svm","glcm_rf","combined_svm"],default="combined_svm");p.add_argument("--output",type=Path,default=Path("models/trained"));args=p.parse_args()
from morphguard.dataset.labels import approved_rows
root=Path(__file__).parents[1]; reviewed=approved_rows(args.manifest,root); approved_paths={r["image_path"].replace('\\','/') for r in reviewed}; approved_labels={r["image_path"].replace('\\','/'):r["verified_label"] for r in reviewed}
files=sorted(args.feature_dir.glob("*.npz")); X=[];y=[]; key={"lbp_svm":"lbp","hog_svm":"hog","glcm_rf":"glcm","combined_svm":"X"}[args.model]
for f in files:
 d=np.load(f); paths=[str(x).replace('\\','/') for x in d["paths"]]; keep=[i for i,pth in enumerate(paths) if pth in approved_paths]
 if keep: X.append(d[key][keep]); y.extend([approved_labels[paths[i]] for i in keep])
if not X: raise SystemExit("No feature shards found")
X=np.vstack(X); y=np.array(y); estimator=RandomForestClassifier(n_estimators=300,class_weight="balanced",random_state=42,n_jobs=2) if args.model=="glcm_rf" else make_pipeline(StandardScaler(),SVC(C=1.0,class_weight="balanced",probability=True,random_state=42))
estimator.fit(X,y);args.output.mkdir(parents=True,exist_ok=True);joblib.dump(estimator,args.output/f"{args.model}.joblib");print(json.dumps({"rows":len(y),"classes":sorted(set(y))}))
