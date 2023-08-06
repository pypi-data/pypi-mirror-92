#!/usr/bin/python3
import re
import logging
import argparse
import pandas as pd
from pathlib import Path
from logging.handlers import RotatingFileHandler
from inspect import signature, Parameter
from pyhard import integrator, log_file
from pyhard.context import Configuration
from pyhard.visualization import Demo, App
from pyhard.feature_selection import featfilt
from pyhard.app import graphene
from pyhard import formatter
from pyhard.hpo import set_hyperopt_progressbar


def main():
    logger = logging.getLogger(__name__)
    _my_path = Path().absolute()

    if args.other is None:
        config_path = _my_path / 'config.yaml'
    else:
        config_path = args.other

    with Configuration(config_path) as conf:
        logger.info(f"Configuration file: '{str(config_path)}'")
        for name, path_str in conf.get(['rootdir', 'matildadir', 'datafile']).items():
            if path_str is None:
                continue
            path = Path(path_str)
            if not path.is_absolute():
                abs_path = _my_path / path
                abs_path = abs_path.resolve()
                if abs_path.exists():
                    conf.set(name, str(abs_path))
                else:
                    logger.error("Invalid '{0}': '{1}'".format(name, abs_path))
                    raise NotADirectoryError

        file_path = Path(conf.get('datafile'))
        if file_path.is_file():
            logger.info("Reading input dataset: {0}".format(file_path))
            df_dataset = pd.read_csv(file_path)
        else:
            logger.error("Invalid datafile '{0}'".format(file_path))
            raise FileNotFoundError

        kwargs = conf.get_full()
        rootdir_path = Path(conf.get('rootdir'))

        if args.meta:
            logger.info("Building metadata.")
            df_metadata, df_ih = integrator.build_metadata(data=df_dataset, return_ih=True,
                                                           verbose=args.verbose, **kwargs)

        if args.matilda:
            if conf.get('feat_select'):
                logger.info("Feature selection on")
                if 'df_metadata' not in locals():
                    df_metadata = pd.read_csv(rootdir_path / 'metadata.csv', index_col='instances')
                df_metadata.to_csv(rootdir_path / 'metadata_original.csv')

                sig = signature(featfilt)
                param_dict = {param.name: kwargs[param.name] for param in sig.parameters.values()
                              if param.kind == param.POSITIONAL_OR_KEYWORD and param.default != Parameter.empty and
                              param.name in kwargs}
                selected, df_metadata = featfilt(df_metadata, **param_dict)
                logger.info("Selected features: {0}".format(selected))

            isa_engine = str.lower(conf.get('isa_engine'))
            logger.info(f"Running Instance Space Analysis with {repr(isa_engine)} engine.")
            if isa_engine == 'python':
                integrator.run_isa(rootdir=rootdir_path)
            elif isa_engine == 'matlab':
                _ = integrator.run_matilda(metadata=df_metadata, rootdir=conf.get('rootdir'),
                                           matildadir=conf.get('matildadir'))
            elif isa_engine == 'matlab_compiled':
                integrator.run_matilda_module(rootdir=rootdir_path)
            else:
                raise RuntimeError(f"Unknown ISA engine {repr(isa_engine)}.")

        if args.app:
            logging.getLogger().setLevel(logging.WARNING)
            if not args.meta:
                df_metadata = pd.read_csv(rootdir_path / 'metadata.csv', index_col='instances')
                df_ih = pd.read_csv(rootdir_path / 'ih.csv', index_col='instances')
            df_metadata = df_ih.join(df_metadata, how='right')
            df_is = pd.read_csv(rootdir_path / 'coordinates.csv', index_col='Row')
            df_foot_perf = pd.read_csv(rootdir_path / 'footprint_performance.csv', index_col='Row')
            df_foot_perf.index.name = 'Algorithm'

            pattern = re.compile('(^footprint)_(.+)_(good|bad|best)', re.IGNORECASE)
            footprint_files = [u.name for u in rootdir_path.glob('*.csv')
                               if u.is_file() and bool(pattern.search(u.name))]
            fp_dict = dict()
            for file in footprint_files:
                g = pattern.match(file).groups()
                try:
                    fp_dict[(g[1], g[2])] = pd.read_csv(rootdir_path / file, usecols=['Row', 'z_1', 'z_2'],
                                                        index_col='Row')
                except ValueError:
                    continue
            df_footprint = pd.concat(fp_dict)
            df_footprint.reset_index(level='Row', drop=True, inplace=True)
            df_footprint.index.names = ['algo', 'type']
            df_footprint.sort_index(inplace=True)

            df_is.index.name = df_metadata.index.name
            df_dataset.index = df_metadata.index

            app = App(df_dataset, df_metadata, df_is, df_footprint, df_foot_perf)
            app.show(port=5001, websocket_origin=['127.0.0.1:5001', 'localhost:5001'])

        logger.info("Instance Hardness analysis finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyHard - Instance Hardness Framework. \n"
                                                 "Run 'python3 -m pyhard -h' for help with the options. \n"
                                                 "In case of trouble, submit us an issue: "
                                                 "https://gitlab.com/ita-ml/instance-hardness/")
    parser.add_argument('--no-meta', dest='meta', action='store_false',
                        help="does not generate a new metadata file; uses previously saved instead")
    parser.add_argument('--no-matilda', dest='matilda', action='store_false',
                        help="does not execute matilda")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help="verbose mode")
    parser.add_argument('--app', dest='app', action='store_true', default=False,
                        help="run app to visualize data")
    parser.add_argument('--demo', dest='demo', action='store_true', default=False,
                        help="run demo for datasets in 'data/' directory")
    parser.add_argument('-g', '--graphene', dest='graphene', action='store_true', default=False,
                        help="run graphene")
    parser.add_argument('-c', '--config', dest='other', default=None, required=False,
                        metavar='FILE', help="specifies a path to a config file other than default")

    args = parser.parse_args()
    print("run 'python3 -m pyhard -h' for help.")

    # Temporary solution for known warnings
    logging.getLogger("param").setLevel(logging.ERROR)
    if not args.graphene:
        sh = logging.StreamHandler()
        if args.verbose:
            sh.setLevel(logging.DEBUG)
        else:
            sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        logging.getLogger().addHandler(sh)
    else:
        with open(log_file, 'w'):
            pass
        fh = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=5)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logging.getLogger().addHandler(fh)

    if args.demo:
        print("Press ^C to exit demo")
        demo = Demo()
        pane = demo.display()
        pane.servable()
        pane.show(title="Demo", port=5001, websocket_origin=['127.0.0.1:5001', 'localhost:5001'])  # threaded=True
    elif args.app:
        args.matilda = False
        args.meta = False
        main()
    elif args.graphene:
        set_hyperopt_progressbar(False)
        graphene.run()
    else:
        logging.getLogger().setLevel(logging.INFO)
        main()
