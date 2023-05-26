import frappe
from erpnext.accounts.doctype.period_closing_voucher.period_closing_voucher import PeriodClosingVoucher
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions


class QlipPeriodClosingVoucher(PeriodClosingVoucher):

    def on_submit(self):

        super(QlipPeriodClosingVoucher, self).on_submit()

        if self.qp_finance_book:
            sql_upd = """
                UPDATE `tabGL Entry` SET finance_book = '{cond_fb}'
                where voucher_no = '{cond_pcv}'
            """.format(cond_fb=self.qp_finance_book, cond_pcv=self.name)

            print("sql_upd--->>>", sql_upd)

            frappe.db.sql(sql_upd)


    def get_pl_balances(self):
        """Get balance for dimension-wise pl accounts"""

        dimension_fields = ['t1.cost_center']

        self.accounting_dimensions = get_accounting_dimensions()
        for dimension in self.accounting_dimensions:
            dimension_fields.append('t1.{0}'.format(dimension))

        if self.qp_finance_book:
            cond_finance_book = "t1.finance_book = '{}'".format(self.qp_finance_book)
        else:
            cond_finance_book = "(t1.finance_book in ('') OR t1.finance_book IS NULL)"

        sql_test = """
            select
                t1.account, t2.account_currency, {dimension_fields},
                sum(t1.debit_in_account_currency) - sum(t1.credit_in_account_currency) as bal_in_account_currency,
                sum(t1.debit) - sum(t1.credit) as bal_in_company_currency
            from `tabGL Entry` t1, `tabAccount` t2
            where t1.account = t2.name and t2.report_type = 'Profit and Loss'
            and t2.docstatus < 2 and t2.company = '{comp}'
            and t1.posting_date between '{fech_d}' and '{fech_h}'
            and {cond_fb}
            group by t1.account, {dimension_fields}
        """.format(dimension_fields = ', '.join(dimension_fields), comp = self.company, fech_d = self.get("year_start_date"), fech_h = self.posting_date, cond_fb= cond_finance_book)

        return frappe.db.sql(sql_test, as_dict=1)
