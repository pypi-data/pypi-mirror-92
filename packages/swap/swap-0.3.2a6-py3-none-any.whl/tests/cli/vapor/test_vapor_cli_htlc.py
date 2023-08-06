#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_cli_htlc(cli_tester):

    htlc = cli_tester.invoke(
        cli_main, [
            "vapor",
            "htlc",
            "--secret-hash", _["vapor"]["htlc"]["secret"]["hash"],
            "--recipient-public-key", _["vapor"]["wallet"]["recipient"]["public_key"],
            "--sender-public-key", _["vapor"]["wallet"]["sender"]["public_key"],
            "--sequence", _["vapor"]["htlc"]["sequence"],
            "--network", _["vapor"]["network"]
        ]
    )

    assert htlc.exit_code == 0
    assert htlc.output == str(json.dumps(dict(
        bytecode=_["vapor"]["htlc"]["bytecode"],
        address=_["vapor"]["htlc"]["address"]
    ), indent=4)) + "\n"
