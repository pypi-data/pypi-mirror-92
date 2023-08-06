"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
import logging

from web3.types import BlockIdentifier
from web3 import Web3
from moneyonchain.contract import Contract


class Governor(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['governor']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def owner(self, block_identifier: BlockIdentifier = 'latest'):
        """Owner"""

        result = self.sc.functions.owner().call(
            block_identifier=block_identifier)

        return result

    def transfer_ownership(self, new_owner,
                           gas_limit=3500000,
                           wait_timeout=240,
                           default_account=None,
                           wait_receipt=True):
        """

        :param new_owner:
        :param gas_limit:
        :param wait_timeout:
        :param default_account:
        :param wait_receipt:
        :return:

        function transferOwnership(address newOwner) public onlyOwner {
            _transferOwnership(newOwner);
        }
        """

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'transferOwnership',
                                                          Web3.toChecksumAddress(new_owner),
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

            self.log.info("Successfully transfer ownership to: {0} in Block [{1}] Hash: [{2}] Gas used: [{3}] From: [{4}]"
                          .format(new_owner,
                                  tx_receipt['blockNumber'],
                                  Web3.toHex(tx_receipt['transactionHash']),
                                  tx_receipt['gasUsed'],
                                  tx_receipt['from']))

        return tx_hash, tx_receipt


class DEXGovernor(Governor):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'
    precision = 10 ** 18


class Governed(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        network = connection_manager.network
        if not contract_address:
            raise ValueError("You need to pass contract address")

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def governor(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.functions.governor().call(
            block_identifier=block_identifier)

        return result

    def initialize(self, governor,
                   gas_limit=3500000,
                   wait_timeout=240,
                   default_account=None,
                   wait_receipt=True):
        """Initialize"""

        governor_address = Web3.toChecksumAddress(governor)

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'initialize',
                                                          governor_address,
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                          timeout=wait_timeout)

            self.log.info("Successfully initialized in Block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                tx_receipt['blockNumber'],
                Web3.toHex(tx_receipt['transactionHash']),
                tx_receipt['gasUsed'],
                tx_receipt['from']))

        return tx_hash, tx_receipt


class MoCStopper(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Stopper.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Stopper.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['stopper']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def address_stopper(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.functions.stopper().call(
            block_identifier=block_identifier)

        return result

    def owner(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.functions.owner().call(
            block_identifier=block_identifier)

        return result

    def pause(self, contract_to_pause,
              gas_limit=3500000,
              wait_timeout=240,
              default_account=None,
              wait_receipt=True):
        """Initialize"""

        contract_to_pause = Web3.toChecksumAddress(contract_to_pause)

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'pause',
                                                          contract_to_pause,
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

            self.log.info("Successfully paused contract {0} in Block [{1}] Hash: [{2}] Gas used: [{3}] From: [{4}]"
                          .format(contract_to_pause,
                                  tx_receipt['blockNumber'],
                                  Web3.toHex(tx_receipt['transactionHash']),
                                  tx_receipt['gasUsed'],
                                  tx_receipt['from']))

        return tx_hash, tx_receipt

    def unpause(self, contract_to_pause,
                gas_limit=3500000,
                wait_timeout=240,
                default_account=None,
                wait_receipt=True):
        """Initialize"""

        contract_to_pause = Web3.toChecksumAddress(contract_to_pause)

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'unpause',
                                                          contract_to_pause,
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

            self.log.info("Successfully paused contract {0} in Block [{1}] Hash: [{2}] Gas used: [{3}] From: [{4}]"
                          .format(contract_to_pause,
                                  tx_receipt['blockNumber'],
                                  Web3.toHex(tx_receipt['transactionHash']),
                                  tx_receipt['gasUsed'],
                                  tx_receipt['from']))

        return tx_hash, tx_receipt

    def transfer_ownership(self, new_owner,
                           gas_limit=3500000,
                           wait_timeout=240,
                           default_account=None,
                           wait_receipt=True):
        """

        :param new_owner:
        :param gas_limit:
        :param wait_timeout:
        :param default_account:
        :param wait_receipt:
        :return:

        function transferOwnership(address newOwner) public onlyOwner {
            _transferOwnership(newOwner);
        }
        """

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'transferOwnership',
                                                          Web3.toChecksumAddress(new_owner),
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

            self.log.info("Successfully transfer ownership to: {0} in Block [{1}] Hash: [{2}] Gas used: [{3}] From: [{4}]"
                          .format(new_owner,
                                  tx_receipt['blockNumber'],
                                  Web3.toHex(tx_receipt['transactionHash']),
                                  tx_receipt['gasUsed'],
                                  tx_receipt['from']))

        return tx_hash, tx_receipt


class RDOCStopper(MoCStopper):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Stopper.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Stopper.bin'))

    mode = 'RDoC'
    precision = 10 ** 18


class RDOCGoverned(Governed):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governed.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governed.bin'))

    mode = 'RDoC'
    precision = 10 ** 18
