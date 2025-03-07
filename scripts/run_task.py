"""
Author: Wenyu Ouyang
Date: 2022-04-27 10:54:32
LastEditTime: 2024-04-15 20:02:45
LastEditors: Wenyu Ouyang
Description: Generate commands to run scripts in Linux Screen
FilePath: \HydroMTL\scripts\run_task.py
Copyright (c) 2021-2022 Wenyu Ouyang. All rights reserved.
"""
import argparse
import os
from pathlib import Path
import sys


sys.path.append(os.path.dirname(Path(os.path.abspath(__file__)).parent))
import definitions
from scripts.mtl_results_utils import run_mtl_camels


def train_and_test(args):
    exp = args.exp
    output_vars = args.output_vars
    loss_weight = args.loss_weight
    train_periods = args.train_period
    test_periods = args.test_period
    limit_parts = args.limit_part
    ctxs = args.ctx
    random_seed = args.random
    cache_dir = args.cache_path
    weight_path = args.weight_path
    train_epochs = args.train_epoch
    gage_id_file = args.gage_id_file
    if gage_id_file is None or gage_id_file == "None":
        gage_id_file = os.path.join(
            definitions.RESULT_DIR,
            "camels_us_mtl_2001_2021_flow_screen.csv",
        )
    if cache_dir is None or cache_dir == "None":
        cache_dir = os.path.join(definitions.RESULT_DIR, "camels", exp)
    if weight_path == "None":
        weight_path = None
    if limit_parts == "None":
        limit_parts = None
    run_mtl_camels(
        exp,
        targets=output_vars,
        random_seed=random_seed,
        cache_dir=cache_dir,
        ctx=ctxs,
        weight_ratio=loss_weight,
        limit_part=limit_parts,
        train_period=train_periods,
        test_period=test_periods,
        weight_path=weight_path,
        train_epoch=train_epochs,
        gage_id_file=gage_id_file,
    )


if __name__ == "__main__":
    print("Here are your commands:")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp",
        dest="exp",
        help="the ID of the experiment, such as expstlq001",
        type=str,
        default="testmtl001",
        # default="expmtl001",
        # default="expstlet001",
        # default="expstlq201",
        # default="expmtlqssm101",
    )
    parser.add_argument(
        "--output_vars",
        dest="output_vars",
        help="the variables as output of MTL models, chosen from ['usgsFlow', 'ET', 'ssm']",
        nargs="+",
        type=str,
        default=["usgsFlow", "ET"],
        # default=["usgsFlow", "ssm"],
    )
    parser.add_argument(
        "--loss_weight",
        dest="loss_weight",
        help="weight of loss for usgsFlow or/and ET/ssm",
        nargs="+",
        type=float,
        default=[0.5, 0.5],
        # default=[0.0, 1.0],
        # default=[1.0, 0.0],
    )
    parser.add_argument(
        "--train_period",
        dest="train_period",
        help="training period, such as ['2001-10-01', '2011-10-01']",
        nargs="+",
        default=["2001-10-01", "2011-10-01"],
        # default=["2005-10-01", "2015-10-01"],
        # default=["2015-10-01", "2018-10-01"],
    )
    parser.add_argument(
        "--test_period",
        dest="test_period",
        help="testing period, such as ['2011-10-01', '2016-10-01']",
        nargs="+",
        default=["2011-10-01", "2016-10-01"],
        # default=["2015-10-01", "2018-10-01"],
        # default=["2018-10-01", "2021-10-01"],
    )
    parser.add_argument(
        "--ctx", dest="ctx", help="CUDA IDs", nargs="+", type=int, default=[1]
    )
    parser.add_argument(
        "--random", dest="random", help="random seed", type=int, default=1234
    )
    parser.add_argument(
        "--limit_part",
        dest="limit_part",
        help="if an output variable is ignored, then its index in all outputs are used.\
            For example,two variables' index are 0 and 1. If first is ignored, then the limit value is 0",
        nargs="+",
        type=int,
        default=None,
        # default=[0],
        # default=[1],
    )
    parser.add_argument(
        "--cache_path",
        dest="cache_path",
        help="the cache file for forcings, attributes and targets data",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--weight_path",
        dest="weight_path",
        help="training with pre-trained model",
        type=str,
        default=None,
        # default="/mnt/sdc/owen/code/HydroMTL/results/camels/expstlq201/04_May_202306_17PM_model.pth",
    )
    parser.add_argument(
        "--train_epoch",
        dest="train_epoch",
        help="epoch of training",
        type=int,
        default=300,
    )
    parser.add_argument(
        "--gage_id_file",
        dest="gage_id_file",
        help="the file of gage IDs",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    print(f"Your command arguments:{str(args)}")
    train_and_test(args)
