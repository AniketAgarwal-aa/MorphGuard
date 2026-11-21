"""MorphGuard V3.2 — Synchronize 21-Model Package to Public Hugging Face Hub.

Uploads the 18 missing deep learning models and metadata, updates the 3 catalog/doc files,
and preserves the 45 already identical files in a single atomic commit.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from pathlib import Path
from huggingface_hub import HfApi, CommitOperationAdd

ROOT = Path(__file__).parents[1]
DEFAULT_REPO = "AniketAgarwal-aa/MorphGuard-Models"
EXPECTED_PARENT_SHA = "4f50fd493b2f6ea9a468b07ccd37d912ec77fbe5"

def get_file_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def sync_public_hub(dry_run: bool = False, repo_id: str = DEFAULT_REPO):
    api = HfApi()
    user = api.whoami()
    print(f"Authenticated as: {user.get('name')}")
    
    info = api.repo_info(repo_id=repo_id, repo_type="model")
    print(f"Target Repository: {repo_id}")
    print(f"Visibility: {'PUBLIC' if not info.private else 'PRIVATE'}")
    print(f"Remote Parent Revision: {info.sha}")
    
    # Read the sync plan
    plan_path = ROOT / "reports/predictions/hf_sync_plan.json"
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
        
    missing = plan["missing_on_hub"]
    updates = plan["requires_update"]
    identical = plan["identical"]
    
    print(f"\nOperations Planned:")
    print(f"  - Files to Create: {len(missing)} (18 files, ~262.63 MB)")
    print(f"  - Files to Update: {len(updates)} (3 files, catalog & README)")
    print(f"  - Files to Preserve (Skipped): {len(identical)} (45 files)")
    
    export_dir = ROOT / "models/hf_export"
    operations = []
    
    # Add missing files
    for item in missing:
        rel_p = item["path"]
        local_p = export_dir / rel_p
        if not local_p.exists():
            raise FileNotFoundError(f"Staged file missing locally: {local_p}")
        operations.append(CommitOperationAdd(path_in_repo=rel_p, path_or_fileobj=str(local_p)))
        
    # Add updated files
    for item in updates:
        rel_p = item["path"]
        local_p = export_dir / rel_p
        if not local_p.exists():
            raise FileNotFoundError(f"Staged file missing locally: {local_p}")
        operations.append(CommitOperationAdd(path_in_repo=rel_p, path_or_fileobj=str(local_p)))
        
    print(f"\nTotal Commit Operations Prepared: {len(operations)}")
    
    if dry_run:
        print("\n[DRY-RUN] Preflight checks passed. No remote modifications performed.")
        return info.sha
        
    print(f"\nExecuting Atomic Commit on {repo_id}...")
    commit_info = api.create_commit(
        repo_id=repo_id,
        repo_type="model",
        operations=operations,
        commit_message="MorphGuard V3.2 — Synchronize 21-model calibrated artifacts, metadata, and non-commercial research model card",
        parent_commit=info.sha
    )
    new_sha = commit_info.oid
    print(f"\n[SUCCESS] Atomic commit succeeded!")
    print(f"New Repository Revision: {new_sha}")
    print(f"Commit URL: https://huggingface.co/{repo_id}/commit/{new_sha}")
    return new_sha

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Validate operations without committing")
    parser.add_argument("--repo-id", default=DEFAULT_REPO, help="Target repository ID")
    args = parser.parse_args()
    
    sync_public_hub(dry_run=args.dry_run, repo_id=args.repo_id)
