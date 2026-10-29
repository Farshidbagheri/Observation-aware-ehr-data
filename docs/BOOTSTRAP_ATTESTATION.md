# Source bundle provenance

- Release: Observation-Aware EHR research v0.2, assembled from the user-supplied pilot and actual MIMIC-IV v2.2 demo archives.
- Source ZIP SHA256: `08dd661719f5e277853ff7350281a2695df2ee4080f9b4b4a488bcd0c1653f9b`.
- **No raw patient-level rows** or restricted patient records are inside the source bundle.
- The initialization workflow verifies the archive checksum before extracting 34 source, test, documentation, aggregate-evidence and fixture files.
- The original public ED and clinical demo files remain separate ODbL-licensed datasets; the package contains a hash-verifying downloader.
- MongoDB integration requires a live MongoDB deployment; the local authoring environment did not run a MongoDB performance comparison.
