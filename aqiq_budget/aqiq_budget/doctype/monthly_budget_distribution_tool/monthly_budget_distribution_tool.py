# Copyright (c) 2024, aqiq Budget and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from collections import defaultdict

class MonthlyBudgetDistributionTool(Document):
	pass
@frappe.whitelist(allow_guest=True)
def create_budget(name):
    print(name)  
    doc = frappe.get_doc('Monthly Budget Distribution Tool', name)
    period = frappe.db.sql(f"""SELECT period FROM `tabMonthly Distribution Map Table` WHERE parent='{doc.monthly_distribution_template}'""", as_dict=True)
    periods_count = len(period)
    percentages = []
    for t in doc.monthly_budget_distribution_table:
        for index, month in enumerate(period, start=1):
            year_field = f'year_{index}'
            # print(f"Index: {index}")
            amount = getattr(t, year_field, 0)
            percentage_allocation = (amount / t.total_amount) * 100 if t.total_amount else 0
            if percentage_allocation > 0.0:
                percentages.append({
                    'account': t.account,
                    'month': month['period'],
                    'percentage_allocation': f"{percentage_allocation}",
                    'total_amount': t.total_amount
                })
    # print("Percentages collected:")
    # print(percentages)
    grouped_percentages = defaultdict(list)
    for percentage_data in percentages:
        account = percentage_data['account']
        total_amount = percentage_data['total_amount']
        grouped_percentages[account].append({
            'month': percentage_data['month'],
            'percentage_allocation': percentage_data['percentage_allocation'],
            'total_amount': total_amount
        })
    
    # print("Grouped percentages by account:")
    # print(grouped_percentages)
    account_per=set()
    for account, percentages_list in grouped_percentages.items():       
        if account not in account_per:
            distribution_id=f"{doc.fiscal_year}-{account.replace(' ', '-')}"
            if doc.budget_against == 'Project':
                new_monthly_distribution_doc = frappe.get_doc({
                    'doctype': 'Monthly Distribution',
                    'distribution_id': distribution_id,
                    'fiscal_year': doc.fiscal_year,
                    'account': account,
                    'percentages': percentages_list,
                })
                print(new_monthly_distribution_doc)
                
                new_budget_doc = frappe.get_doc({
                    'doctype': 'Budget',
                    'budget_against': doc.budget_against,
                    'company': doc.company,
                    'project': doc.project,
                    'monthly_distribution':distribution_id,
                    'applicable_on_material_request': doc.applicable_on_material_request,
                    'applicable_on_purchase_order': doc.applicable_on_purchase_order,
                    'Applicable on booking actual expenses':doc.applicable_on_booking_actual_expenses,
                    'fiscal_year': doc.fiscal_year,
                    'accounts': [{'account': account, 'budget_amount': total_amount}],
                })
            elif doc.budget_against == 'Cost Center':
                new_monthly_distribution_doc = frappe.get_doc({
                    'doctype': 'Monthly Distribution',
                    'distribution_id': distribution_id,
                    'fiscal_year': doc.fiscal_year,
                    'account': account,
                    'percentages': percentages_list,
                })
                
                new_budget_doc = frappe.get_doc({
                    'doctype': 'Budget',
                    'budget_against': doc.budget_against,
                    'company': doc.company,
                    'cost_center': doc.cost_center,
                    'monthly_distribution':distribution_id,
                    'applicable_on_material_request': doc.applicable_on_material_request,
                    'applicable_on_purchase_order': doc.applicable_on_purchase_order,
                    'fiscal_year': doc.fiscal_year,
                    'accounts': [{'account': account, 'budget_amount': total_amount}],
                })
            else:
                pass
            if frappe.db.exists("Monthly Distribution", {"name": distribution_id}):
                pass
            else:
                new_monthly_distribution_doc.insert()
                new_budget_doc.insert()
                frappe.db.commit()
                account_per.add(account)
                frappe.db.commit()
        print(account_per)
@frappe.whitelist()
def test():
    account
    new_monthly_distribution_doc = frappe.get_doc({
            'doctype': 'Monthly Distribution',
            'distribution_id': distribution_id,
            'fiscal_year': doc.fiscal_year,
            'account': account,
            'percentages': percentages_list,
        })


        

@frappe.whitelist(allow_guest=True)
def get_period(name):
    period=frappe.db.sql(f"""SELECT period from `tabMonthly Distribution Map Table` where parent='{name}'""")
    return period

def test():
    pass