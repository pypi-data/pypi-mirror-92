"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import logging

from brownie.network.transaction import TransactionReceipt


class TransactionReceiptBase(TransactionReceipt):

    log = logging.getLogger()

    def __init__(self,
                 *args,
                 logger=None,
                 **parameters):

        if logger:
            self.log = logger

        super().__init__(*args, **parameters)

    def info_to_log(self) -> None:
        """Displays verbose information about the transaction, including decoded event logs."""
        status = ""
        if not self.status:
            status = f"({self.revert_msg or 'reverted'})"

        result = (
            f"Transaction was Mined {status}\n---------------------\n"
            f"Tx Hash: {self.txid}\n"
            f"From: {self.sender}\n"
        )

        if self.contract_address and self.status:
            result += (
                f"New {self.contract_name} address: {self.contract_address}\n"
            )
        else:
            result += (
                f"To: {self.receiver}\n"
                f"Value: {self.value}\n"
            )
            if self.input != "0x" and int(self.input, 16):
                result += f"Function: {self._full_name()}\n"

        result += (
            f"Block: {self.block_number}\nGas Used: "
            f"{self.gas_used} / {self.gas_limit}"
            f"({self.gas_used / self.gas_limit:.1%})\n"
        )

        if self.events:
            result += "\n   Events In This Transaction\n   --------------------------"
            for event in self.events:  # type: ignore
                result += f"\n   {event.name}"  # type: ignore
                for key, value in event.items():  # type: ignore
                    result += f"\n      {key}: {value}"

        self.log.info(result)


def receipt_to_log(receipt, log):
    """ Receipt to logging """

    status = ""
    if not receipt.status:
        status = ""

    result = (
        f"Transaction was Mined {status}\n---------------------\n"
        f"Tx Hash: {receipt.txid}\n"
        f"From: {receipt.sender}\n"
    )

    if receipt.contract_address and receipt.status:
        result += (
            f"New {receipt.contract_name} address: {receipt.contract_address}\n"
        )
    else:
        result += (
            f"To: {receipt.receiver}\n"
            f"Value: {receipt.value}\n"
        )
        if receipt.input != "0x" and int(receipt.input, 16):
            result += f"Function: {receipt._full_name()}\n"

    result += (
        f"Block: {receipt.block_number}\nGas Used: "
        f"{receipt.gas_used} / {receipt.gas_limit}"
        f"({receipt.gas_used / receipt.gas_limit:.1%})\n"
    )

    if receipt.events:
        result += "\n   Events In This Transaction\n   --------------------------"
        for event in receipt.events:  # type: ignore
            result += f"\n   {event.name}"  # type: ignore
            for key, value in event.items():  # type: ignore
                result += f"\n      {key}: {value}"

    log.info(result)
