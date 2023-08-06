
from ..utils import get_phenolist, PheWebError
from ..conf_utils import conf
from ..file_utils import VariantFileWriter, write_json, get_generated_path, common_filepaths
from .read_input_file import PhenoReader
from .load_utils import parallelize_per_pheno, indent

import itertools
import argparse


def run(argv):

    parser = argparse.ArgumentParser(description="import input files into a nice format")
    parser.add_argument('--phenos')
    args = parser.parse_args(argv)

    phenos = get_phenolist()
    if args.phenos is not None:
        try:
            pheno_idxs_to_include = set(int(x) for x in args.phenos.split(','))
        except Exception as exc:
            raise PheWebError("Couldn't parse string {!r}".format(args.phenos)) from exc
        phenos = [phenos[i] for i in pheno_idxs_to_include]

    results_by_phenocode = parallelize_per_pheno(
        get_input_filepaths = lambda pheno: pheno['assoc_files'],
        get_output_filepaths = lambda pheno: common_filepaths['parsed'](pheno['phenocode']),
        convert = convert,
        cmd = 'parse-input-files',
        phenos = phenos,
    )

    failed_results = {phenocode:value for phenocode,value in results_by_phenocode.items() if not value['succeeded']}
    if failed_results:
        failed_filepath = get_generated_path('tmp', 'parse-failures.json')
        write_json(filepath=failed_filepath, data=failed_results, indent=1, sort_keys=True)
        print('\n{} phenotypes failed (saved to {!r})\n'.format(len(failed_results), failed_filepath))

        phenos = get_phenolist()
        succeeded_phenos = [p for p in phenos if p['phenocode'] not in failed_results]
        succeeded_filepath = get_generated_path('tmp', 'pheno-list-successful-only.json')
        write_json(filepath=succeeded_filepath, data=succeeded_phenos, indent=1, sort_keys=True)
        if len(succeeded_phenos) == 0:
            raise PheWebError(
                'PheWeb was unable to parse the input files for all {} phenotypes.\n\n'.format(len(phenos)) +
                'Information about the phenotypes that failed is in {!r}\n'.format(failed_filepath)
            )
        else:
            raise PheWebError(
                'Some files failed to parse.\n\n' +
                'A new pheno-list.json with only the {} phenotypes that succeeded (out of {} total) has been written to {!r}.\n'.format(
                    len(succeeded_phenos), len(phenos), succeeded_filepath) +
                'To continue with only these phenotypes, run:\n'
                'cp {!r} {!r}\n'.format(succeeded_filepath, common_filepaths['phenolist']()) +
                'Information about the phenotypes that failed is in {!r}\n'.format(failed_filepath)
            )

def convert(pheno):
    # suppress Exceptions so that we can report back on which phenotypes succeeded and which didn't.
    try:
        with VariantFileWriter(common_filepaths['parsed'](pheno['phenocode'])) as writer:
            pheno_reader = PhenoReader(pheno, minimum_maf=conf.assoc_min_maf)
            variants = pheno_reader.get_variants()
            if conf.limit_num_variants and isinstance(conf.limit_num_variants, int): variants = itertools.islice(variants, 0, conf.limit_num_variants)
            writer.write_all(variants)
    except Exception as exc:
        import traceback
        yield {
            'type': 'warning', # TODO: make PerPhenoParallelizer print this.
            'warning_str':
                'Exception:\n' + indent(str(exc)) +
                '\nTraceback:\n' + indent(traceback.format_exc()) +
                '\nFiles:\n' + indent('\n'.join(pheno['assoc_files']))
        }
        yield {"succeeded": False, "exception_str": str(exc), "exception_tb": traceback.format_exc()}
    else:
        yield {"succeeded": True}
