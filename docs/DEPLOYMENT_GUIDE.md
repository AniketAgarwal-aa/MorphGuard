# Deployment Guide

Run locally with `streamlit run app/main.py`. The Docker image packages application code and safe audit metadata only; raw MONOT/ONOT directories remain excluded. A missing or unapproved model keeps Face Analysis in research-only mode. Before deployment, run the test suite, `pip check`, and Docker build/runtime checks on the target Docker engine.
