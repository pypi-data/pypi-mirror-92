#!/usr/bin/env python3

import json
import os

from swap.providers.bytom.transaction import (
    NormalTransaction, FundTransaction, ClaimTransaction, RefundTransaction
)
from swap.providers.bytom.solver import (
    NormalSolver, FundSolver, ClaimSolver, RefundSolver
)
from swap.providers.bytom.utils import amount_unit_converter
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_normal_transaction():

    unsigned_normal_transaction = NormalTransaction(network=_["bytom"]["network"])

    unsigned_normal_transaction.build_transaction(
        address=_["bytom"]["wallet"]["sender"]["address"],
        asset=_["bytom"]["asset"],
        recipients={
            _["bytom"]["wallet"]["recipient"]["address"]: (
                _["bytom"]["amount"] if _["bytom"]["unit"] == "NEU" else amount_unit_converter(
                    _["bytom"]["amount"], f"{_['bytom']['unit']}2NEU")
            )
        }
    )

    assert unsigned_normal_transaction.type() == _["bytom"]["normal"]["unsigned"]["type"]
    assert unsigned_normal_transaction.fee() == _["bytom"]["normal"]["unsigned"]["fee"]
    assert unsigned_normal_transaction.hash() == _["bytom"]["normal"]["unsigned"]["hash"]
    assert unsigned_normal_transaction.raw() == _["bytom"]["normal"]["unsigned"]["raw"]
    # assert unsigned_normal_transaction.json() == _["bytom"]["normal"]["unsigned"]["json"]
    assert unsigned_normal_transaction.unsigned_datas() == _["bytom"]["normal"]["unsigned"]["unsigned_datas"]
    assert unsigned_normal_transaction.signatures() == _["bytom"]["normal"]["unsigned"]["signatures"]
    assert unsigned_normal_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["normal"]["unsigned"]["transaction_raw"]
    )

    signed_normal_transaction = unsigned_normal_transaction.sign(
        solver=NormalSolver(
            xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
            path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
            account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
            change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
            address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_normal_transaction.type() == _["bytom"]["normal"]["signed"]["type"]
    assert signed_normal_transaction.fee() == _["bytom"]["normal"]["signed"]["fee"]
    assert signed_normal_transaction.hash() == _["bytom"]["normal"]["signed"]["hash"]
    assert signed_normal_transaction.raw() == _["bytom"]["normal"]["signed"]["raw"]
    # assert signed_normal_transaction.json() == _["bytom"]["normal"]["signed"]["json"]
    assert signed_normal_transaction.unsigned_datas() == _["bytom"]["normal"]["signed"]["unsigned_datas"]
    assert signed_normal_transaction.signatures() == _["bytom"]["normal"]["signed"]["signatures"]
    assert signed_normal_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["normal"]["signed"]["transaction_raw"]
    )


def test_bytom_fund_transaction():

    unsigned_fund_transaction = FundTransaction(network=_["bytom"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["bytom"]["wallet"]["sender"]["address"],
        htlc_address=_["bytom"]["htlc"]["address"],
        asset=_["bytom"]["asset"],
        amount=(
            _["bytom"]["amount"] if _["bytom"]["unit"] == "NEU" else amount_unit_converter(
                _["bytom"]["amount"], f"{_['bytom']['unit']}2NEU")
        )
    )

    assert unsigned_fund_transaction.type() == _["bytom"]["fund"]["unsigned"]["type"]
    assert unsigned_fund_transaction.fee() == _["bytom"]["fund"]["unsigned"]["fee"]
    assert unsigned_fund_transaction.hash() == _["bytom"]["fund"]["unsigned"]["hash"]
    assert unsigned_fund_transaction.raw() == _["bytom"]["fund"]["unsigned"]["raw"]
    # assert unsigned_fund_transaction.json() == _["bytom"]["fund"]["unsigned"]["json"]
    assert unsigned_fund_transaction.unsigned_datas() == _["bytom"]["fund"]["unsigned"]["unsigned_datas"]
    assert unsigned_fund_transaction.signatures() == _["bytom"]["fund"]["unsigned"]["signatures"]
    assert unsigned_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["unsigned"]["transaction_raw"]
    )

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
            path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
            account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
            change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
            address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_fund_transaction.type() == _["bytom"]["fund"]["signed"]["type"]
    assert signed_fund_transaction.fee() == _["bytom"]["fund"]["signed"]["fee"]
    assert signed_fund_transaction.hash() == _["bytom"]["fund"]["signed"]["hash"]
    assert signed_fund_transaction.raw() == _["bytom"]["fund"]["signed"]["raw"]
    # assert signed_fund_transaction.json() == _["bytom"]["fund"]["signed"]["json"]
    assert signed_fund_transaction.unsigned_datas() == _["bytom"]["fund"]["signed"]["unsigned_datas"]
    assert signed_fund_transaction.signatures() == _["bytom"]["fund"]["signed"]["signatures"]
    assert signed_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["signed"]["transaction_raw"]
    )


def test_bytom_claim_transaction():

    unsigned_claim_transaction = ClaimTransaction(network=_["bytom"]["network"])

    unsigned_claim_transaction.build_transaction(
        address=_["bytom"]["wallet"]["recipient"]["address"],
        transaction_id=_["bytom"]["transaction_id"],
        amount=(
            _["bytom"]["amount"] if _["bytom"]["unit"] == "NEU" else amount_unit_converter(
                _["bytom"]["amount"], f"{_['bytom']['unit']}2NEU")
        ),
        max_amount=_["bytom"]["max_amount"],
        asset=_["bytom"]["asset"],
    )

    assert unsigned_claim_transaction.type() == _["bytom"]["claim"]["unsigned"]["type"]
    assert unsigned_claim_transaction.fee() == _["bytom"]["claim"]["unsigned"]["fee"]
    assert unsigned_claim_transaction.hash() == _["bytom"]["claim"]["unsigned"]["hash"]
    assert unsigned_claim_transaction.raw() == _["bytom"]["claim"]["unsigned"]["raw"]
    # assert unsigned_claim_transaction.json() == _["bytom"]["claim"]["unsigned"]["json"]
    assert unsigned_claim_transaction.unsigned_datas() == _["bytom"]["claim"]["unsigned"]["unsigned_datas"]
    assert unsigned_claim_transaction.signatures() == _["bytom"]["claim"]["unsigned"]["signatures"]
    assert unsigned_claim_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["claim"]["unsigned"]["transaction_raw"]
    )

    signed_claim_transaction = unsigned_claim_transaction.sign(
        solver=ClaimSolver(
            xprivate_key=_["bytom"]["wallet"]["recipient"]["xprivate_key"],
            secret_key=_["bytom"]["htlc"]["secret"]["key"],
            bytecode=_["bytom"]["htlc"]["bytecode"],
            path=_["bytom"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["bytom"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["bytom"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["bytom"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_claim_transaction.type() == _["bytom"]["claim"]["signed"]["type"]
    assert signed_claim_transaction.fee() == _["bytom"]["claim"]["signed"]["fee"]
    assert signed_claim_transaction.hash() == _["bytom"]["claim"]["signed"]["hash"]
    assert signed_claim_transaction.raw() == _["bytom"]["claim"]["signed"]["raw"]
    # assert signed_claim_transaction.json() == _["bytom"]["claim"]["signed"]["json"]
    assert signed_claim_transaction.unsigned_datas() == _["bytom"]["claim"]["signed"]["unsigned_datas"]
    assert signed_claim_transaction.signatures() == _["bytom"]["claim"]["signed"]["signatures"]
    assert signed_claim_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["claim"]["signed"]["transaction_raw"]
    )


def test_bytom_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["bytom"]["network"])

    unsigned_refund_transaction.build_transaction(
        address=_["bytom"]["wallet"]["sender"]["address"],
        transaction_id=_["bytom"]["transaction_id"],
        amount=(
            _["bytom"]["amount"] if _["bytom"]["unit"] == "NEU" else amount_unit_converter(
                _["bytom"]["amount"], f"{_['bytom']['unit']}2NEU")
        ),
        max_amount=_["bytom"]["max_amount"],
        asset=_["bytom"]["asset"],
    )

    assert unsigned_refund_transaction.type() == _["bytom"]["refund"]["unsigned"]["type"]
    assert unsigned_refund_transaction.fee() == _["bytom"]["refund"]["unsigned"]["fee"]
    assert unsigned_refund_transaction.hash() == _["bytom"]["refund"]["unsigned"]["hash"]
    assert unsigned_refund_transaction.raw() == _["bytom"]["refund"]["unsigned"]["raw"]
    # assert unsigned_refund_transaction.json() == _["bytom"]["refund"]["unsigned"]["json"]
    assert unsigned_refund_transaction.unsigned_datas() == _["bytom"]["refund"]["unsigned"]["unsigned_datas"]
    assert unsigned_refund_transaction.signatures() == _["bytom"]["refund"]["unsigned"]["signatures"]
    assert unsigned_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["refund"]["unsigned"]["transaction_raw"]
    )

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
            bytecode=_["bytom"]["htlc"]["bytecode"],
            path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
            account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
            change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
            address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_refund_transaction.type() == _["bytom"]["refund"]["signed"]["type"]
    assert signed_refund_transaction.fee() == _["bytom"]["refund"]["signed"]["fee"]
    assert signed_refund_transaction.hash() == _["bytom"]["refund"]["signed"]["hash"]
    assert signed_refund_transaction.raw() == _["bytom"]["refund"]["signed"]["raw"]
    # assert signed_refund_transaction.json() == _["bytom"]["refund"]["signed"]["json"]
    assert signed_refund_transaction.unsigned_datas() == _["bytom"]["refund"]["signed"]["unsigned_datas"]
    assert signed_refund_transaction.signatures() == _["bytom"]["refund"]["signed"]["signatures"]
    assert signed_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["refund"]["signed"]["transaction_raw"]
    )
