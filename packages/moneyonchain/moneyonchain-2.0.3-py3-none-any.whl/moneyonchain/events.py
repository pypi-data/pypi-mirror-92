"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

from tabulate import tabulate


class BaseEvent(object):
    name = "BaseEvent"
    hours_delta = 0

    @staticmethod
    def columns():
        columns = []
        return columns

    def print_table(self):
        return tabulate([self.row()], headers=self.columns(), tablefmt="pipe")

    def print_row(self):
        return tabulate([self.row()], tablefmt="pipe")
