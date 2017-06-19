from xero import Xero
from xero.auth import PrivateCredentials
from invoices import INVOICE_IDS

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


def void_invoices(invoice_ids=None):
    """
    Void a list of invoices
    """

    xero = auth_xero()

    # Load the defaults if they 
    if not invoice_ids:
        invoice_ids = INVOICE_IDS

    with open('void_results.csv', 'wb') as csvfile:

        fieldnames = ['InvoiceID','Current Status','Result','Error']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for invoice_id in invoice_ids:

            result = None
            error = None

            print '\n\nVoiding Invoice %s' % invoice_id

            # Check the current status
            xero_invoice = xero.invoices.get(invoice_id)

            current_status = xero_invoice[0].get('Status')

            print '    Current invoice status is %s' % current_status

            if current_status != 'VOIDED':

                invoice_to_void = {
                    'InvoiceID': invoice_id,
                    'Status': 'VOIDED',
                    'LineAmountTypes': 'NoTax'
                }

                try:
                    result = xero.invoices.save(invoice_to_void)

                    if result[0].get('Status') == 'VOIDED':
                        result = 'Void'
                        print '        Successfully voided invoice'
                    else:
                        result = 'Failed'
                        print '        Still not voided...'

                except Exception as ex:
                    print '        Failed to void invoice %s' % str(ex)
                    result = 'Failed'
                    error = str(ex)

            else:

                result = 'Void'

                print '        Invoice already voided, doing nothing!'


            writer.writerow({
                'InvoiceID': invoice_id,
                'Current Status': current_status,
                'Result': result,
                'Error': error
            })


