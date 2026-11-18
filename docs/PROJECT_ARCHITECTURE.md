# Project Architecture

MorphGuard separates Streamlit presentation (`app/`), reusable components (`app/components`), research modules (`src/morphguard`), scripts, configuration, safe metadata and raw datasets. Training and split generation require an approved manifest; inference requires a validated model artifact. Docker packages application code and safe metadata, never raw MONOT/ONOT images.
