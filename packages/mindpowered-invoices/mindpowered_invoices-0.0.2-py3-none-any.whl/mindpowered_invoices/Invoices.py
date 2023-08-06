import maglev
import invoices

from typing import Any, List, Callable

class Invoices:
	"""
	An Library for Creating Invoices
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = invoices.invoices_Invoices(bus)

	def CreateInvoice(self, clientId: str, invoiceNumber: str, date: str, dueDate: str, notes: str) -> str:
		"""		Create a new invoice
		Args:
			clientId (str):
			invoiceNumber (str):
			date (str):
			dueDate (str):
			notes (str):
		Returns:
			New invoice id
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [clientId, invoiceNumber, date, dueDate, notes]
		ret = None
		def CreateInvoice_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.CreateInvoice', args, CreateInvoice_Ret)
		return ret

	def DeleteInvoice(self, invoiceId: str):
		"""		Delete an invoice
		Args:
			invoiceId (str):
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceId]
		ret = None
		def DeleteInvoice_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.DeleteInvoice', args, DeleteInvoice_Ret)

	def ChangeInvoice(self, invoiceId: str, clientId: str, invoiceNumber: str, date: str, dueDate: str, notes: str):
		"""		
		Args:
			invoiceId (str):
			clientId (str):
			invoiceNumber (str):
			date (str):
			dueDate (str):
			notes (str):
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceId, clientId, invoiceNumber, date, dueDate, notes]
		ret = None
		def ChangeInvoice_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.ChangeInvoice', args, ChangeInvoice_Ret)

	def GetInvoiceSummary(self, invoiceId: str) -> object:
		"""		
		Args:
			invoiceId (str):
		Returns:
			
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceId]
		ret = None
		def GetInvoiceSummary_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.GetInvoiceSummary', args, GetInvoiceSummary_Ret)
		return ret

	def GetLineItems(self, invoiceId: str) -> List[Any]:
		"""		
		Args:
			invoiceId (str):
		Returns:
			Line items for invoice
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceId]
		ret = None
		def GetLineItems_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.GetLineItems', args, GetLineItems_Ret)
		return ret

	def AddLineItem(self, invoiceId: str, accountId: str, description: str, taxes: object, quantity: float, price: float) -> float:
		"""		
		Args:
			invoiceId (str):
			accountId (str):
			description (str):
			taxes (object):
			quantity (float):
			price (float):
		Returns:
			lineNumber
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceId, accountId, description, taxes, quantity, price]
		ret = None
		def AddLineItem_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.AddLineItem', args, AddLineItem_Ret)
		return ret

	def ChangeLineItem(self, invoiceId: str, lineNumber: float, accountId: str, description: str, taxes: object, quantity: float, price: float):
		"""		
		Args:
			invoiceId (str):
			lineNumber (float):
			accountId (str):
			description (str):
			taxes (object):
			quantity (float):
			price (float):
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceId, lineNumber, accountId, description, taxes, quantity, price]
		ret = None
		def ChangeLineItem_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.ChangeLineItem', args, ChangeLineItem_Ret)

	def RemoveLineItem(self, invoiceId: str, lineNumber: float):
		"""		
		Args:
			invoiceId (str):
			lineNumber (float):
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceId, lineNumber]
		ret = None
		def RemoveLineItem_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.RemoveLineItem', args, RemoveLineItem_Ret)

	def GetInvoicesByClient(self, clientId: str) -> List[Any]:
		"""		
		Args:
			clientId (str):
		Returns:
			
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [clientId]
		ret = None
		def GetInvoicesByClient_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.GetInvoicesByClient', args, GetInvoicesByClient_Ret)
		return ret

	def GetAllInvoices(self, page: float, perpage: float) -> List[Any]:
		"""		
		Args:
			page (float):
			perpage (float):
		Returns:
			
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [page, perpage]
		ret = None
		def GetAllInvoices_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.GetAllInvoices', args, GetAllInvoices_Ret)
		return ret

	def FindInvoiceByNumber(self, invoiceNumber: str) -> Any:
		"""		Returns the Invoice ID or null
		Args:
			invoiceNumber (str):
		Returns:
			
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [invoiceNumber]
		ret = None
		def FindInvoiceByNumber_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('Invoices.FindInvoiceByNumber', args, FindInvoiceByNumber_Ret)
		return ret



