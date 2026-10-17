import importlib.util
import tempfile
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('prep', Path(__file__).parents[1]/'scripts/prepare_severity_by_event.py')
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)
class PreparationTest(unittest.TestCase):
    def test_filter_counts_and_preserves_same_filenames(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'root'; out=Path(tmp)/'out'; root.mkdir()
            rows=['image\tlabel']
            for day in ['day1','day2']:
                image=root/'data_image'/'event'/day/'same.jpg'
                image.parent.mkdir(parents=True); image.write_bytes(day.encode())
                rows.append(f'data_image/event/{day}/same.jpg\tmild_damage')
            rows += ['data_image/event/day3/missing.jpg\tsevere_damage', 'data_image/event/day4/excluded.jpg\tlittle_or_no_damage']
            tsv=root/'split.tsv'; tsv.write_text('\n'.join(rows))
            self.assertEqual(prep.process_split(tsv,'train',root,out), {'copied':2,'missing':1,'excluded':1})
            self.assertEqual(len(list(out.rglob('*.jpg'))),2)
            with self.assertRaises(FileExistsError): prep.process_split(tsv,'train',root,out)
    def test_rejects_path_traversal_and_bad_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); tsv=root/'split.tsv'
            tsv.write_text('image\tlabel\ndata_image/../../escape.jpg\tmild_damage\n')
            with self.assertRaises(ValueError): prep.process_split(tsv,'train',root,root/'out')
            tsv.write_text('wrong\tcolumns\n')
            with self.assertRaises(ValueError): prep.process_split(tsv,'train',root,root/'out')
if __name__ == '__main__': unittest.main()
