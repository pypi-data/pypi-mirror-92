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

from web3 import Web3
from moneyonchain.contract import Contract


class BaseChanger(Contract):
    log = logging.getLogger()

    contract_abi = None
    contract_bin = None

    contract_governor_abi = None
    contract_governor_bin = None

    mode = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

    def fnx_constructor(self, *tx_parameters, wait_receipt=True):
        """ Constructor deploy """
        sc, content_abi, content_bin = self.connection_manager.load_bytecode_contract(self.contract_abi,
                                                                                      self.contract_bin)
        tx_hash = self.connection_manager.fnx_constructor(sc, *tx_parameters)

        tx_receipt = None
        if wait_receipt:
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)

        return tx_hash, tx_receipt

    def load_governor(self):
        """ Load governor contract"""

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['governor']
        result = self.connection_manager.load_contract(self.contract_governor_abi, contract_address)
        return result


class MoCSettlementChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlementChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlementChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, input_block_span, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCSettlement']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, input_block_span)

        self.log.info("Deployed contract done!")
        self.log.info(tx_hash)
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(tx_hash)
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCMoCSettlementChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCSettlementChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCSettlementChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, input_block_span, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCSettlement']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, input_block_span)

        self.log.info("Deployed contract done!")
        self.log.info(tx_hash)
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(tx_hash)
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCMoCInrateStableChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MocInrateStableChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MocInrateStableChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, t_min, t_max, t_power, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, t_min, t_max, t_power)

        self.log.info("Deployed contract done!")
        self.log.info(tx_hash)
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(tx_hash)
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCMoCInrateRiskproxChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCInrateRiskproxChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCInrateRiskproxChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, t_min, t_max, t_power, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, t_min, t_max, t_power)

        self.log.info("Deployed contract done!")
        self.log.info(tx_hash)
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(tx_hash)
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCMoCBucketContainerChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCBucketContainerChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCBucketContainerChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, cobj_c0, cobj_x2, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCBProxManager']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, cobj_c0, cobj_x2)

        self.log.info("Deployed contract done!")
        self.log.info(tx_hash)
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(tx_hash)
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCCommissionSplitterAddressChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/SetCommissionFinalAddressChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/SetCommissionFinalAddressChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, commission_address, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['CommissionSplitter']
        commission_address = Web3.toChecksumAddress(commission_address)

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, commission_address)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCPriceFeederAdderChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederAdder.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederAdder.bin'))

    contract_medianizer_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.abi'))
    contract_medianizer_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.bin'))

    contract_feedfactory_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/FeedFactory.abi'))
    contract_feedfactory_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/FeedFactory.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, account_owner,
                    contract_address_medianizer=None,
                    contract_address_feedfactory=None,
                    execute_change=False):

        network = self.connection_manager.network
        if not contract_address_medianizer:
            contract_address_medianizer = self.connection_manager.options['networks'][network]['addresses']['oracle']
        if not contract_address_feedfactory:
            contract_address_feedfactory = self.connection_manager.options['networks'][network]['addresses']['FeedFactory']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address_feedfactory),
                                                   Web3.toChecksumAddress(contract_address_medianizer),
                                                   Web3.toChecksumAddress(account_owner))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class PriceFeederAdderChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederAdder.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederAdder.bin'))

    contract_medianizer_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.abi'))
    contract_medianizer_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.bin'))

    contract_feedfactory_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/FeedFactory.abi'))
    contract_feedfactory_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/FeedFactory.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, account_owner,
                    contract_address_medianizer=None,
                    contract_address_feedfactory=None,
                    execute_change=False):

        network = self.connection_manager.network
        if not contract_address_medianizer:
            contract_address_medianizer = self.connection_manager.options['networks'][network]['addresses']['oracle']
        if not contract_address_feedfactory:
            contract_address_feedfactory = self.connection_manager.options['networks'][network]['addresses']['FeedFactory']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address_feedfactory),
                                                   Web3.toChecksumAddress(contract_address_medianizer),
                                                   Web3.toChecksumAddress(account_owner))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class PriceFeederRemoverChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederRemover.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederRemover.bin'))

    contract_medianizer_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.abi'))
    contract_medianizer_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, contract_address_price_feed,
                    contract_address_medianizer=None,
                    execute_change=False):

        network = self.connection_manager.network
        if not contract_address_medianizer:
            contract_address_medianizer = self.connection_manager.options['networks'][network]['addresses']['oracle']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address_medianizer),
                                                   Web3.toChecksumAddress(contract_address_price_feed))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class PriceFeederWhitelistChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederWhitelist.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeederWhitelist.bin'))

    contract_medianizer_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.abi'))
    contract_medianizer_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, contract_address_price_feed,
                    contract_address_medianizer=None,
                    execute_change=False):

        network = self.connection_manager.network
        if not contract_address_medianizer:
            contract_address_medianizer = self.connection_manager.options['networks'][network]['addresses']['oracle']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address_medianizer),
                                                   Web3.toChecksumAddress(contract_address_price_feed))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCPriceFeederRemoverChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederRemover.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeederRemover.bin'))

    contract_medianizer_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.abi'))
    contract_medianizer_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'

    def constructor(self, contract_address_price_feed,
                    contract_address_medianizer=None,
                    execute_change=False):

        network = self.connection_manager.network
        if not contract_address_medianizer:
            contract_address_medianizer = self.connection_manager.options['networks'][network]['addresses']['oracle']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address_medianizer),
                                                   Web3.toChecksumAddress(contract_address_price_feed))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MoCPriceProviderChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceProviderChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, price_provider, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCState']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, Web3.toChecksumAddress(price_provider))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MoCSetCommissionMocProportionChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionMocProportionChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionMocProportionChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, moc_proportion, commission_splitter=None, execute_change=False):

        network = self.connection_manager.network
        if not commission_splitter:
            commission_splitter = self.connection_manager.options['networks'][network]['addresses']['CommissionSplitter']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(commission_splitter), moc_proportion)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MoCSetCommissionFinalAddressChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionFinalAddressChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/SetCommissionFinalAddressChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, commission_address, commission_splitter=None, execute_change=False):

        network = self.connection_manager.network
        if not commission_splitter:
            commission_splitter = self.connection_manager.options['networks'][network]['addresses']['CommissionSplitter']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(commission_splitter),
                                                   Web3.toChecksumAddress(commission_address))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MoCInrateCommissionsAddressChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionsAddressChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CommissionsAddressChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, commission_address, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address),
                                                   Web3.toChecksumAddress(commission_address))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MoCInrateRiskProRateChangerChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrateRiskProRateChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrateRiskProRateChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, bitpro_rate, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address),
                                                   bitpro_rate)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MocInrateBitProInterestChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateBitProInterestChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocInrateBitProInterestChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, bitpro_blockspan, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCInrate']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(Web3.toChecksumAddress(contract_address),
                                                   bitpro_blockspan)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MocStateMaxMintBProChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocStateMaxMintBProChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocStateMaxMintBProChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, max_mint_bpro, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCState']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, max_mint_bpro)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCMoCStateMaxMintRiskProChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCStateMaxMintRiskProChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCStateMaxMintRiskProChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'MoC'

    def constructor(self, max_mint_riskpro, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCState']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, max_mint_riskpro)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class MocMakeStoppableChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocMakeStoppableChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MocMakeStoppableChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governor.bin'))

    mode = 'MoC'

    def constructor(self, stoppable=True, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoC']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, stoppable)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCPriceProviderChanger(MoCPriceProviderChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceProviderChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceProviderChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDoC'


class DexAddTokenPairChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/AddTokenPairChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/AddTokenPairChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_token,
                    secondary_address,
                    price_provider,
                    price_precision,
                    init_price,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   [Web3.toChecksumAddress(base_token)],
                                                   [Web3.toChecksumAddress(secondary_address)],
                                                   [Web3.toChecksumAddress(price_provider)],
                                                   [price_precision],
                                                   [init_price],
                                                   )

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexTokenPairDisabler(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/TokenPairDisabler.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/TokenPairDisabler.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_address,
                    secondary_address,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   Web3.toChecksumAddress(base_address),
                                                   Web3.toChecksumAddress(secondary_address))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexTokenPairEnabler(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/TokenPairEnabler.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/TokenPairEnabler.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_address,
                    secondary_address,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   Web3.toChecksumAddress(base_address),
                                                   Web3.toChecksumAddress(secondary_address))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexEMAPriceChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/EMAPriceChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/EMAPriceChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_token,
                    secondary_token,
                    ema_price,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token),
                                                   ema_price)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexMaxOrderLifespanChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MaxOrderLifespanChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MaxOrderLifespanChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    order_lifespan,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   order_lifespan)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexPriceProviderChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/PriceProviderChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/PriceProviderChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    base_token,
                    secondary_token,
                    price_provider,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   Web3.toChecksumAddress(base_token),
                                                   Web3.toChecksumAddress(secondary_token),
                                                   Web3.toChecksumAddress(price_provider))

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexMaxBlocksForTickChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MaxBlocksForTickChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MaxBlocksForTickChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    max_blocks_for_ticks,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   max_blocks_for_ticks)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexMinBlocksForTickChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MinBlocksForTickChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MinBlocksForTickChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    min_blocks_for_ticks,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   min_blocks_for_ticks)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexCommissionRateChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/CommissionRateChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/CommissionRateChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    commission_rate,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(
            self.connection_manager.options['networks'][network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   commission_rate)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexMinOrderAmountChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MinOrderAmountChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MinOrderAmountChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    min_order_amount,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(
            self.connection_manager.options['networks'][network]['addresses']['dex'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   min_order_amount)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexCancelationPenaltyRateChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/CancelationPenaltyRateChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/CancelationPenaltyRateChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    cancelation_penalty_rate,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(
            self.connection_manager.options['networks'][network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   cancelation_penalty_rate)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexExpirationPenaltyRateChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/ExpirationPenaltyRateChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/ExpirationPenaltyRateChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    expiration_penalty_rate,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(
            self.connection_manager.options['networks'][network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   expiration_penalty_rate)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class DexMinimumCommissionChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MinimumCommissionChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MinimumCommissionChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/Governor.bin'))

    mode = 'DEX'

    def constructor(self,
                    minimum_commission,
                    execute_change=False):

        network = self.connection_manager.network
        contract_address = Web3.toChecksumAddress(
            self.connection_manager.options['networks'][network]['addresses']['commissionManager'])

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address,
                                                   minimum_commission)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt


class RDOCMocMakeStoppableChanger(BaseChanger):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MocMakeStoppableChanger.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MocMakeStoppableChanger.bin'))

    contract_governor_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.abi'))
    contract_governor_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governor.bin'))

    mode = 'RDOC'

    def constructor(self, stoppable=True, execute_change=False):

        network = self.connection_manager.network
        contract_address = self.connection_manager.options['networks'][network]['addresses']['MoC']

        self.log.info("Deploying new contract...")

        tx_hash, tx_receipt = self.fnx_constructor(contract_address, stoppable)

        self.log.info("Deployed contract done!")
        self.log.info(Web3.toHex(tx_hash))
        self.log.info(tx_receipt)

        self.log.info("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))

        if execute_change:
            self.log.info("Executing change....")
            governor = self.load_governor()
            tx_hash = self.connection_manager.fnx_transaction(governor, 'executeChange', tx_receipt.contractAddress)
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            self.log.info(Web3.toHex(tx_hash))
            self.log.info(tx_receipt)
            self.log.info("Change successfull!")

        return tx_hash, tx_receipt
