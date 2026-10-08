# GitHub packaging record

The owner authorized GitHub upload after the pilot was completed, on 2026-10-09
(Asia/Shanghai). This later authorization does not alter the historical scope
of the frozen pre-run protocol.

- Repository: https://github.com/richardsh3n/mergeable-neural-memory
- Current visibility: **public**. The owner explicitly authorized public access
  on 2026-10-09 after the initial private upload; both the repository and release
  archive are now publicly accessible.
- Version: **v0.1.0**, a research pilot prerelease, not a peer-reviewed paper.
- Complete archive: [download from the version page](https://github.com/richardsh3n/mergeable-neural-memory/releases/tag/v0.1.0).
- Asset: `mergeable-neural-memory-pilot-2026-10-09.zip` (30,971,412 bytes).
- Archive SHA-256: `789ac4529d90dbab645e7223b3d85cfaf066f4bc701b8782fb58b061ae4495b6`.

The 47-file archive is the unchanged original post-run package. It includes the
source, locally frozen protocol, dependencies, tests, manuscript, figures,
396,000 prediction rows, all three trained checkpoints, and independent audit.
The repository preserves the same files and adds this packaging record. All
three `.pt` checkpoints are intentionally tracked even though `.gitignore`
ignores future checkpoint files by default.

The pre-run manifest, run-artifact hashes, and post-run package manifest refer
to different stages. This record is a later repository addition and is not
included in the original pre-run or 47-file package hashes.

The primary superiority hypothesis remains **unsupported**: residual 78.85%
versus MAXSET 79.33%; effect −0.47 percentage points, conditional 95% interval
[−1.23, +0.32]. There is no real LLM experiment or strong-compression claim.

The manuscript source compiled successfully in the desktop editor. A standalone
manuscript PDF was not exported; the archive contains `.tex` and exportable
plot PDFs. Publishing this package does not constitute a new experiment,
independent model replication or external registration.
