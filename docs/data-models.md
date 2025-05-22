ynab-mcp-server API Enhancement Data Models
This document outlines the key data models and schemas used by the MCP tools, primarily focusing on tool inputs (defined via Zod) and the structure of data returned from the YNAB API.

1. Core MCP Tool Input Schemas (Defined via Zod)
Input schemas for each new tool are defined within their respective ToolName.ts files. These Zod schemas serve as the data models for tool inputs. Below are conceptual representations based on the Epics. Refer to the specific tool implementation for the canonical Zod schema.

Epic 1: Core Category Endpoint Implementation
list_categories (ListCategoriesTool)
Input Schema (ListCategoriesInput):
budgetId (string, optional): ID of the budget. Defaults to YNAB_BUDGET_ID.
Output: Array of YNAB Category objects.
get_category (GetCategoryTool)
Input Schema (GetCategoryInput):
budgetId (string, optional): ID of the budget. Defaults to YNAB_BUDGET_ID.
category_id (string, required): ID of the category to retrieve.
Output: YNAB Category object.
get_category_by_month (GetCategoryByMonthTool)
Input Schema (GetCategoryByMonthInput):
budgetId (string, optional): ID of the budget. Defaults to YNAB_BUDGET_ID.
month (string, required, format YYYY-MM-DD): The month to retrieve category details for.
category_id (string, required): ID of the category.
Output: YNAB Category object (with month-specific attributes).
update_category (UpdateCategoryTool)
Input Schema (UpdateCategoryInput):
budgetId (string, optional): ID of the budget. Defaults to YNAB_BUDGET_ID.
category_id (string, required): ID of the category to update.
name (string, optional): New name for the category.
note (string, optional, nullable): New note for the category.
Output: Updated YNAB Category object.
update_month_category (UpdateMonthCategoryTool)
Input Schema (UpdateMonthCategoryInput):
budgetId (string, optional): ID of the budget. Defaults to YNAB_BUDGET_ID.
month (string, required, format YYYY-MM-DD): The month to update.
category_id (string, required): ID of the category.
budgeted (number, required): Budgeted amount in milliunits. (Tool input description should clarify if it accepts currency units and converts, or expects milliunits directly. Epics state "budgeted (number, in milliunits)" for the input, so direct milliunits is expected here).
Output: Updated YNAB Category object for the month.
Epic 2: Core Transaction Endpoint Implementation & Enhancement
list_transactions (ListTransactionsTool)
Input Schema (ListTransactionsInput):
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
since_date (string, optional, format YYYY-MM-DD): Filter by date.
type (string, optional, enum: uncategorized, unapproved): Filter by type.
Output: Array of transformed YNAB TransactionDetail objects (amounts converted).
get_transaction_by_id (GetTransactionByIdTool)
Input Schema (GetTransactionByIdInput):
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
transaction_id (string, required): ID of the transaction.
Output: Transformed YNAB TransactionDetail object (amounts converted, including subtransactions).
create_transaction (Enhanced CreateTransactionTool)
Input Schema (CreateTransactionInput - Enhanced):
budgetId (string, optional)
accountId (string, required)
date (string, required, format YYYY-MM-DD)
amount (number, required, in currency units)
payeeId (string, optional)
payeeName (string, optional, max 50 chars)
categoryId (string, optional)
memo (string, optional, max 200 chars)
cleared (enum string e.g. "cleared", "uncleared", "reconciled", optional) -> maps to ynab.TransactionClearedStatus
approved (boolean, optional)
flagColor (enum string e.g. "red", "orange", optional) -> maps to ynab.TransactionFlagColor
import_id (string, optional, max 36 chars)
subtransactions (array of SaveSubTransactionInput, optional):
amount (number, required, in currency units)
payeeId (string, optional)
payeeName (string, optional, max 50 chars)
categoryId (string, optional)
memo (string, optional, max 200 chars)
Output: Object with success, transactionId, message.
update_transaction (UpdateTransactionTool)
Input Schema (UpdateTransactionInput):
budgetId (string, optional)
transaction_id (string, required)
Plus all fields from the enhanced CreateTransactionInput (except accountId might be fixed for an existing transaction, API defines what's updatable via SaveTransaction). All fields are optional for update.
Output: Updated transformed YNAB TransactionDetail object.
delete_transaction (DeleteTransactionTool)
Input Schema (DeleteTransactionInput):
budgetId (string, optional)
transaction_id (string, required)
Output: Transformed YNAB TransactionDetail of the deleted transaction.
list_account_transactions (ListAccountTransactionsTool)
Input Schema (ListAccountTransactionsInput):
budgetId (string, optional)
account_id (string, required)
since_date (string, optional, format YYYY-MM-DD)
type (string, optional, enum: uncategorized, unapproved)
Output: Array of transformed YNAB TransactionDetail objects.
list_category_transactions (ListCategoryTransactionsTool)
Input Schema (ListCategoryTransactionsInput):
budgetId (string, optional)
category_id (string, required)
since_date (string, optional, format YYYY-MM-DD)
type (string, optional, enum: uncategorized, unapproved)
Output: Array of transformed YNAB HybridTransaction objects.
list_payee_transactions (ListPayeeTransactionsTool)
Input Schema (ListPayeeTransactionsInput):
budgetId (string, optional)
payee_id (string, required)
since_date (string, optional, format YYYY-MM-DD)
type (string, optional, enum: uncategorized, unapproved)
Output: Array of transformed YNAB HybridTransaction objects.
Epic 3: Bulk Transaction Operations
create_bulk_transactions (CreateBulkTransactionsTool)
Input Schema (CreateBulkTransactionsInput):
budgetId (string, optional)
transactions (array of SaveTransactionInputForBulk, required):
Each object mirrors SaveTransaction (similar to CreateTransactionInput but without subtransactions, as YNAB bulk API doesn't support them per item). All amounts in currency units.
Output: YNAB BulkResponse object (data.bulk).
update_bulk_transactions (UpdateBulkTransactionsTool)
Input Schema (UpdateBulkTransactionsInput):
budgetId (string, optional)
transactions (array of UpdateTransactionForBulkInput, required):
Each object requires id (string, transaction_id) and any other updatable fields from SaveTransaction (amounts in currency units, no subtransactions).
Output: YNAB BulkResponse object (data.bulk).
2. Key YNAB API Data Structures (Output from Tools)
The tools will primarily return data structured according to the YNAB API's definitions. The ynab SDK provides TypeScript types for these. Key structures include:

ynab.Category:
id: string
category_group_id: string
name: string
hidden: boolean
note: string | null
budgeted: number (milliunits)
activity: number (milliunits)
balance: number (milliunits)
goal_type: GoalType | null
... (and other goal-related fields, deleted status)
ynab.TransactionDetail:
id: string
date: string
amount: number (milliunits)
memo: string | null
cleared: TransactionClearedStatus
approved: boolean
flag_color: TransactionFlagColor | null
account_id: string
account_name: string
payee_id: string | null
payee_name: string | null
category_id: string | null
category_name: string | null
transfer_account_id: string | null
deleted: boolean
subtransactions: ynab.SubTransaction[]
Each SubTransaction has id, amount, memo, payee_id, category_id, etc.
ynab.HybridTransaction: Similar to TransactionDetail but used by some specific listing endpoints (e.g., by category/payee). May have fewer fields or a slightly different structure (e.g., type field indicating if it's a transaction or subtransaction).
ynab.MonthDetail: Contains monthly summary information, including an array of Category objects for that month.
ynab.BulkResponse:
bulk: { transaction_ids: string[], duplicate_import_ids: string[] }
Potentially transactions if creating/updating single items within a bulk call that returns full objects (less common for pure bulk endpoints).
Note on Transformation: As specified in existing tools and Epics, amounts (milliunits from YNAB) should be converted to currency strings (e.g., "123.45") in the output of read operations for better human readability and consistency.

3. Change Log
Change	Date	Version	Description	Author
Initial draft	2025-05-18	0.1	Initial data models based on Epics and YNAB API structure.	3-Architect