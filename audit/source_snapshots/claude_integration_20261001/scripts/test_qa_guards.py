"""Regression tests for stale-evidence rejection; not physics validation."""
import copy
import unittest
import subprocess
import hashlib
import json
from pathlib import Path
from write_build_audit import validate_binding
import tempfile
from qa_series import series_paths

class QASeriesTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        prior=self.root/'audit/iterations/iteration_99.json'
        prior.parent.mkdir(parents=True)
        prior.write_text('{"result":"pass"}')
        self.spec={'series':'new_revision','predecessor':'audit/iterations/iteration_99.json',
                   'predecessor_sha256':hashlib.sha256(prior.read_bytes()).hexdigest()}
    def resolve(self):
        (self.root/'audit/current_qa_series.json').write_text(json.dumps(self.spec))
        return series_paths(self.root)
    def test_new_series_does_not_fall_back_to_old_pass(self):
        records,renders=self.resolve()
        self.assertEqual(records,self.root/'audit/qa_series/new_revision')
        self.assertEqual(list(records.glob('iteration_*.json')),[])
        self.assertNotEqual(renders,self.root/'audit/qa_runs')
    def test_series_path_traversal_rejected(self):
        self.spec['series']='../iterations'
        with self.assertRaisesRegex(ValueError,'Invalid QA series'): self.resolve()
    def test_changed_predecessor_rejected(self):
        self.spec['predecessor_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'hash mismatch'): self.resolve()

class ReleaseBindingTests(unittest.TestCase):
    def setUp(self):
        self.qa={'result':'pass','full_suite':True,'source_sha256':{'main.tex':'source'},'pdf':{'sha256':'pdf'},'figures_manifest_sha256':'figures','page_metrics':[{'page':1,'sha256':'page1'},{'page':2,'sha256':'page2'}]}
        self.visual={'result':'pass','pdf_sha256':'pdf','page_sha256':{'1':'page1','2':'page2'}}
    def check(self,qa=None,visual=None,sources=None,pdf='pdf',figures='figures'):
        validate_binding(qa or self.qa,visual or self.visual,sources or {'main.tex':'source'},pdf,figures)
    def test_current_exact_binding(self): self.check()
    def test_changed_source_rejected(self):
        with self.assertRaisesRegex(ValueError,'source hashes'): self.check(sources={'main.tex':'edited'})
    def test_changed_pdf_rejected(self):
        with self.assertRaisesRegex(ValueError,'PDF hash'): self.check(pdf='new')
    def test_changed_figure_manifest_rejected(self):
        with self.assertRaisesRegex(ValueError,'figure manifest'): self.check(figures='changed')
    def test_partial_visual_review_rejected(self):
        visual=copy.deepcopy(self.visual); del visual['page_sha256']['2']
        with self.assertRaisesRegex(ValueError,'every current'): self.check(visual=visual)
    def test_failed_latest_suite_rejected(self):
        with self.assertRaisesRegex(ValueError,'did not pass'): self.check(qa=dict(self.qa,result='fail'))
    def test_native_build_failure_preserves_deliverable(self):
        root=Path(__file__).resolve().parents[1]
        pdf=root/'output/fast_mc_zdc_manuscript.pdf'
        before=hashlib.sha256(pdf.read_bytes()).hexdigest()
        stub=root/'audit/qa_runs/negative_native_exit.cmd'
        stub.parent.mkdir(parents=True,exist_ok=True)
        stub.write_text('@exit /b 7\n')
        argv=['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'build.ps1'),'-Python',str(stub)]
        result=subprocess.run(argv,cwd=root,capture_output=True,text=True)
        after=hashlib.sha256(pdf.read_bytes()).hexdigest()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('failed with exit code 7',result.stderr)
        self.assertEqual(before,after)
        (root/'audit/native_build_guard.json').write_text(json.dumps({'command':argv,'returncode':result.returncode,'expected_native_exit':7,'pdf_before':before,'pdf_after':after,'result':'pass','interpretation':'Intentional synthetic build failure rejected; not physics validation'},indent=2)+'\n')
if __name__=='__main__': unittest.main()
