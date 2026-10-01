# Claude proposal integration intake

{
  "created_utc": "2026-10-01T09:31:15.453664+00:00",
  "revision": "0.20.0",
  "status": "integration_in_progress",
  "inputs": {
    "review": "f15e7b0c759cc8deae9ab3bd194041b1418e6cce9291f6eaffcf245ea6e16aeb",
    "proposal_pdf": "d0893fe92881c72571158a7d34689e1c1b072c85a03435ef034ace5d67052087",
    "proposal_source": "503a9f5c87daf6467a7b9c540d95fed8e141810de7aad556c9613a210c17e805"
  },
  "baseline_sha256": {
    "main.tex": "d6ecda6718789571b4d87872e881601173db1ff16048a9dd2ac18614da45e423",
    "README.md": "8cec98bad1cce02a0abe6feed715b6397f838f41a06adf148209a80dba1419ca",
    "STATUS.md": "a3bdea9eceefb7b43ab241c29b8e8560e21fbbbbe0c03ce0ffa63c81897c7322",
    "CITATION.cff": "554e7082f929483527e7a8b2b50cb55cac0fd22be4ddd66cc9fa09f8985b23d8",
    "references.bib": "477fd4f4fc91766da1915d82f635f6db50b1f1c1444724376d2adf57f917a1bf",
    "audit/current_qa_series.json": "0c88c4c3faafe3ed1a7b7cce573247bb2def2b783d27f4f2b08bb703c65be8c0",
    "audit/finalization_20260930.json": "9e01c44054eb177d0688fbdb19ec4ce632df23d1005512aabad1c354fb941e20",
    "audit/final_build_audit.json": "a2bb950aac4018428f971e0f02139217f4bb66b6ad6180a15585368b7e550430",
    "audit/claim_register_20260922.json": "c4a161df782b192a0fe0e7865d6946ae092b6dfb76d7208f25e17836acbfadca",
    "audit/claim_register_20260922.md": "fbd8e766290bfa34c9ba5c5e6ad0863bf305f417d284e9c47825957ccfacf5f9",
    "audit/visual_review_finalization_20260930.json": "5eae125ab2824d92b7979dc1d2b5e0fa87e721e7f4f504312f3dd8d443144626",
    "scripts\\build_figures.py": "828ec61eb1f79365ce79fb59a5e0cb99bbfca519030a2e3fad4e89e59531b102",
    "scripts\\component_bounds.py": "9be89e3dfbe19fe8308af42999e4c9af4262e54789a4204e09e73488c0c80e94",
    "scripts\\full_manuscript_qa.py": "0608e431c6ac47a17b87fdc68dc8035b77c0cf3a2269c0a3dcd4554a6ccfa64e",
    "scripts\\physics_exposition_checks.py": "a2dd3ca33399af137cebda59de3033677c1e7d05140302228a16619a3be347a5",
    "scripts\\qa_series.py": "e9694aefd12bcac2c59a784e3126cb2c296b7d928cd7fcf796aa293dbd2b86e4",
    "scripts\\second_audit_checks.py": "3ebb3e06b99569fd611f22c67234163c6a344e4263f2f644b349e9955eb8fb76",
    "scripts\\test_qa_guards.py": "04e4012b2aa71a3987b1834321d9f507797df43561f3d5b9eba8118fade8feb9",
    "scripts\\write_build_audit.py": "48ac2dad99a8b44c76ea7545b9aae1766a0a6c0120021d03c8619516d4b317db",
    "figures\\detector_geometry.png": "296684aa8264da39332f23f04b3a9d56143fa2f5dcd1c0e68f1a595ff1776926",
    "figures\\generator_schematic.png": "7286a3b17792d6b90790da56560ca74a712b3b215bb55ab53accc644d33d669f",
    "figures\\longitudinal_profile.png": "738378ddc7bfdec5559397e2d8e6b7a636f033cec73509c4197ad2edd58273fb",
    "figures\\manifest.json": "88773004830611572f2727fb747b81189fc93b77e3afa5a4d758dded6cf45b86",
    "figures\\support_summary.png": "4345d6f4112bf4dfa2e9b009041f2e8f7fd5680dc7678dbfd0a06be4a5dcfcba",
    "output\\arxiv_submission_notes.md": "d689eb36ce4fec5547bb6b8e76c8fb0e032903b005fa9a0be30acb27ec840891",
    "output\\fast_mc_zdc_manuscript.pdf": "aae417e83afb71fd95ff3c410b950247654a0cf72e89ceab6a0b64b76bab278f",
    "output\\fast_mc_zdc_submission_source.zip": "ec93e8e1c7771867c422e2c206845763bae08c39dcbe11c7db93ef61aaabb621"
  },
  "environment": {
    "python": "3.13.1 (tags/v3.13.1:0671451, Dec  3 2024, 19:06:28) [MSC v.1942 64 bit (AMD64)]",
    "platform": "Windows-11-10.0.26200-SP0"
  },
  "commands": [
    "Read entire 18-page proposal via pdftotext; inspect contact sheet and detailed figure pages",
    "Read supplied fresh-reader audit and proposed figure source",
    "Read historical evaluator source, aggregate report, static geometry and training history",
    "git status, branch, remote, log; git fetch origin; HEAD...origin/main = 0 0",
    "python -X utf8 audit/integrate_claude_20261001.py"
  ],
  "graft": {
    "tokens_saved_estimate": 16736,
    "legacy_hits": "Ignored; no legacy artifact used"
  },
  "external_sources": [
    "https://arxiv.org/html/2406.12877v2"
  ],
  "scope": "Existing aggregate evidence only; no new training, remote execution, test data or model changes"
}
