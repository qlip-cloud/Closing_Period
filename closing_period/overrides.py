import frappe
from erpnext.accounts.doctype.period_closing_voucher.period_closing_voucher import PeriodClosingVoucher
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions


class QlipPeriodClosingVoucher(PeriodClosingVoucher):

    def get_pl_balances(self):
        """Get balance for dimension-wise pl accounts"""

        print("******************* herencia **************************")

        dimension_fields = ['t1.cost_center']

        self.accounting_dimensions = get_accounting_dimensions()
        for dimension in self.accounting_dimensions:
            dimension_fields.append('t1.{0}'.format(dimension))

        if self.qp_finance_book:
            cond_finance_book = "t1.finance_book = '{}'".format(self.qp_finance_book)
        else:
            cond_finance_book = "t1.finance_book is null"

        return frappe.db.sql("""
            select
                t1.account, t2.account_currency, {dimension_fields},
                sum(t1.debit_in_account_currency) - sum(t1.credit_in_account_currency) as bal_in_account_currency,
                sum(t1.debit) - sum(t1.credit) as bal_in_company_currency
            from `tabGL Entry` t1, `tabAccount` t2
            where t1.account = t2.name and t2.report_type = 'Profit and Loss'
            and t2.docstatus < 2 and t2.company = %s
            and t1.posting_date between %s and %s
            and %s
            group by t1.account, {dimension_fields}
        """.format(dimension_fields = ', '.join(dimension_fields)), (self.company, self.get("year_start_date"), self.posting_date, cond_finance_book), as_dict=1)
