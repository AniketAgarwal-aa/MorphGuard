"""Summarise completed inventories without decoding the raw datasets."""
import json
from pathlib import Path
import pandas as pd
root=Path(__file__).parents[1]; out=root/'data'/'metadata'; result={}
for dataset in ('monot','onot'):
    df=pd.read_csv(out/f'{dataset}_inventory.csv')
    result[dataset]={
        'records':int(len(df)), 'valid':int(df.valid.sum()), 'invalid':int((~df.valid).sum()),
        'formats':df['extension'].value_counts().to_dict(), 'modes':df['mode'].value_counts().to_dict(),
        'dimensions':df.groupby(['width','height'],dropna=False).size().reset_index(name='count').to_dict('records'),
        'bytes':{k:float(v) for k,v in df.bytes.describe().to_dict().items()},
        'categories':df.category.value_counts().to_dict(),
    }
(out/'metadata_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2))
