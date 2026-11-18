# Data Leakage Prevention

Training is restricted to approved manifest rows. The split generator groups by verified subject and morph-pair identifiers, records manifest hash and validates overlap. If grouping metadata is missing or ambiguous, the affected supervised experiment must remain blocked. Dataset source and acquisition strata must be reported separately because a MONOT-versus-ONOT shortcut can masquerade as morph detection.
