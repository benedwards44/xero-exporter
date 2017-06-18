from xero import Xero
from xero.auth import PrivateCredentials

import csv

def auth_xero():
    """
    Authenticate the calls to Xero
    """

    with open('xero_privatekey.pem') as keyfile:
        rsa_key = keyfile.read()

    credentials = PrivateCredentials('LMF7MMCDQTFINMIHXCL1U40I9V4LK7', rsa_key)
    xero = Xero(credentials)

    return xero



def export_invoices():
    """
    Export Xero invoices
    """

    xero = auth_xero()

    # Query for the invoices from Xero
    invoices = xero.invoices.filter(type='ACCPAY')

    # Write the CSv
    with open('invoices.csv', 'wb') as csvfile:

        fieldnames = ['InvoiceID','InvoiceNumber','Total']

        # Write the CSV
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for invoice in invoices:
            writer.writerow({
                'InvoiceID': invoice.get('InvoiceID'),
                'InvoiceNumber': invoice.get('InvoiceNumber'),
                'Total': invoice.get('Total')
            })


def export_credit_notes():
    """
    Export Xero invoices
    """

    xero = auth_xero()

    # Query for the invoices from Xero
    invoices = xero.creditnotes.filter(type='ACCPAYCREDIT')

    # Write the CSv
    with open('credit_notes.csv', 'wb') as csvfile:

        fieldnames = ['CreditNoteID','CreditNoteNumber','Total']

        # Write the CSV
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for invoice in invoices:
            writer.writerow({
                'CreditNoteID': invoice.get('CreditNoteID'),
                'CreditNoteNumber': invoice.get('CreditNoteNumber'),
                'Total': invoice.get('Total')
            })

