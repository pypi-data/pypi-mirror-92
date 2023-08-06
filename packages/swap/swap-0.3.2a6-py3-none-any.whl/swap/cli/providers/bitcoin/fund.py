#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bitcoin.transaction import FundTransaction
from ....providers.bitcoin.utils import amount_unit_converter
from ....providers.config import bitcoin as config


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Fund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-ha", "--htlc-address", type=str, required=True,
              help="Set Bitcoin Hash Time Lock Contract (HTLC) address.")
@click.option("-am", "--amount", type=float, required=True, help="Set Bitcoin fund amount.")
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set Bitcoin fund amount unit.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
@click.option("-v", "--version", type=int, default=config["version"],
              help="Set Bitcoin transaction version.", show_default=True)
def fund(address: str, htlc_address: str, amount: int, unit: str, network: str, version: int):
    try:
        click.echo(
            FundTransaction(
                network=network,
                version=version
            ).build_transaction(
                address=address,
                htlc_address=htlc_address,
                amount=(int(amount) if unit == "SATOSHI" else amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2SATOSHI"
                ))
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
