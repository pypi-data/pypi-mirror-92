from typing import List

from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import BaseModel


class Company(BaseModel):
    vatNumber: str
    country: str
    branch: int


class Address(BaseModel):
    postalCode: int
    city: str


class Issuer(Company):
    pass


class CounterPart(Company):
    address: Address


class InvoiceHeader(BaseModel):
    series: str
    aa: int
    issueDate: str
    invoiceType: str
    currency: str


class PaymentMethodDetails(BaseModel):
    type: int
    amount: float
    paymentMethodInfo: str


class IncomeClassification(BaseModel):
    type: str
    category: str
    amount: float


class InvoiceDetails(BaseModel):
    lineNumber: int
    netValue: float
    vatAmount: float
    vatCategory: str
    discountOption: bool
    classification: IncomeClassification


class Taxes(BaseModel):
    type: int
    category: int
    underlyingValue: float
    amount: float


class InvoiceSummary(BaseModel):
    net: float = 0.0
    vat: float = 0.0
    withheld: float = 0.0
    fees: float = 0.0
    stamp_duty: float = 0.0
    other_taxes: float = 0.0
    deductions: float = 0.0
    gross: float = 0.0
    classifications: List[IncomeClassification]


class Invoice(BaseModel):
    issuer: Issuer
    counterpart: CounterPart
    header: InvoiceHeader
    payment: PaymentMethodDetails
    # invoice details
    details: List[InvoiceDetails]
    taxes: List[Taxes] = []
    summary: InvoiceSummary

    def to_xml(self):
        """
        Renders the XML template
        """
        engine = Environment(
            loader=PackageLoader('mydatapy', 'templates'),
            autoescape=['xml']
        )
        template = engine.get_template("invoice.xml")
        return template.render(invoice=self)
