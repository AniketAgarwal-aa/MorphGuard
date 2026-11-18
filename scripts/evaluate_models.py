"""Evaluation entry point; refuses to run without an approved model/test protocol."""
import argparse
def main():
    p=argparse.ArgumentParser(); p.add_argument('--model',required=True); p.add_argument('--test-split',required=True); a=p.parse_args()
    raise SystemExit('Evaluation is blocked until an approved artifact and leakage-safe test split are available.')
if __name__=='__main__': main()
