ynab-mcp-server API Enhancement: MCP Tool Reference
This document provides a reference for the new and enhanced MCP (Model Context Protocol) tools implemented in the ynab-mcp-server API Enhancement project. Each tool allows interaction with specific YNAB API endpoints.

General Notes:

Authentication: All tools require a valid YNAB_API_TOKEN to be set as an environment variable.
Budget ID: Many tools accept an optional budgetId. If not provided, they will attempt to use the YNAB_BUDGET_ID environment variable if set. An error will occur if no budget ID context is available.
Amounts: Unless otherwise specified for a tool's input parameter, monetary amounts in tool inputs (e.g., for creating/updating transactions) are expected in standard currency units (e.g., dollars, 10.99). These are converted to milliunits before sending to YNAB. Amounts in outputs from YNAB (which are in milliunits) are generally converted back to currency strings (e.g., "10.99") for readability.
Dates: Dates are expected in YYYY-MM-DD ISO format.
Error Handling: Errors from the YNAB API or internal tool logic will typically be returned as a string message or an object containing an error property. Refer to docs/coding-standards.md for details.
Epic 1: Core Category Endpoint Implementation Tools
1. list_categories
Description: Lists all categories for a specified budget, retrieving their complete details.
YNAB API: GET /budgets/{budget_id}/categories
MCP Command Example: list_categories budget_id=my_budget_actual_id
Parameters:
budgetId (string, optional): The ID of the budget. If not provided, uses YNAB_BUDGET_ID.
Example MCP Input:
JSON

{ "budgetId": "a1b2c3d4-e5f6-7890-1234-567890abcdef" }
Or, if YNAB_BUDGET_ID is set:
JSON

{}
Success Response: An array of YNAB Category objects. Each object includes fields like id, category_group_id, name, hidden, note, budgeted, activity, balance, goal_type, etc. (Refer to YNAB API documentation for the full Category schema).
JSON

[
  {
    "id": "c1a2b3d4-e5f6...",
    "category_group_id": "g1a2b3d4...",
    "name": "Groceries",
    "hidden": false,
    "note": "Weekly grocery shopping",
    "budgeted": "500.00", // Example: Converted from 500000 milliunits
    "activity": "-250.50", // Example: Converted from -250500 milliunits
    "balance": "249.50",  // Example: Converted from 249500 milliunits
    "goal_type": "TB",
    // ... other category fields
  }
  // ... more categories
]
2. get_category
Description: Retrieves the complete details for a single specific category by its ID within a budget.
YNAB API: GET /budgets/{budget_id}/categories/{category_id}
MCP Command Example: get_category budget_id=my_budget_id category_id=my_category_id
Parameters:
budgetId (string, optional): The ID of the budget. Defaults to YNAB_BUDGET_ID.
category_id (string, required): The ID of the category to retrieve.
Example MCP Input:
JSON

{
  "budgetId": "a1b2c3d4-e5f6...",
  "category_id": "c1a2b3d4-e5f6..."
}
Success Response: A single YNAB Category object.
JSON

{
  "id": "c1a2b3d4-e5f6...",
  "category_group_id": "g1a2b3d4...",
  "name": "Groceries",
  // ... other category fields
}
3. get_category_by_month
Description: Retrieves the specific monthly details (budgeted, activity, balance, etc.) for a single category within a budget for a given month.
YNAB API: GET /budgets/{budget_id}/months/{month}/categories/{category_id}
MCP Command Example: get_category_by_month month=2025-05-01 category_id=cat_id_123
Parameters:
budgetId (string, optional): The ID of the budget. Defaults to YNAB_BUDGET_ID.
month (string, required): The month in YYYY-MM-DD format (e.g., "2025-05-01").
category_id (string, required): The ID of the category.
Example MCP Input:
JSON

{
  "month": "2025-05-01",
  "category_id": "c1a2b3d4-e5f6..."
}
Success Response: A YNAB Category object, with attributes reflecting their values for the specified month.
JSON

{
  "id": "c1a2b3d4-e5f6...",
  "category_group_id": "g1a2b3d4...",
  "name": "Dining Out",
  "budgeted": "150.00", // Budgeted amount for May 2025
  "activity": "-75.20",  // Activity for May 2025
  "balance": "74.80",   // Balance for May 2025
  // ... other category fields
}
4. update_category
Description: Updates attributes of an existing category (e.g., its name or note).
YNAB API: PATCH /budgets/{budget_id}/categories/{category_id}
MCP Command Example: update_category category_id=cat_id_123 name="New Category Name" note="Updated note."
Parameters:
budgetId (string, optional): The ID of the budget. Defaults to YNAB_BUDGET_ID.
category_id (string, required): The ID of the category to update.
name (string, optional): The new name for the category.
note (string, optional): The new note for the category. Can be an empty string or null to clear the note (behavior depends on YNAB API, usually empty string clears).
Example MCP Input:
JSON

{
  "category_id": "c1a2b3d4-e5f6...",
  "name": "Updated Groceries",
  "note": "All organic now."
}
Success Response: The updated YNAB Category object.
JSON

{
  "id": "c1a2b3d4-e5f6...",
  "name": "Updated Groceries",
  "note": "All organic now.",
  // ... other category fields
}
5. update_month_category
Description: Updates the budgeted amount for a specific category in a specific month.
YNAB API: PATCH /budgets/{budget_id}/months/{month}/categories/{category_id}
MCP Command Example: update_month_category month=2025-06-01 category_id=cat_id_123 budgeted=200000
Parameters:
budgetId (string, optional): The ID of the budget. Defaults to YNAB_BUDGET_ID.
month (string, required): The month in YYYY-MM-DD format.
category_id (string, required): The ID of the category.
budgeted (number, required): The new budgeted amount in milliunits. (e.g., $200.00 should be input as 200000).
Example MCP Input:
JSON

{
  "month": "2025-06-01",
  "category_id": "c1a2b3d4-e5f6...",
  "budgeted": 200000 // Represents $200.00
}
Success Response: The updated YNAB Category object for the specified month.
JSON

{
  "id": "c1a2b3d4-e5f6...",
  "name": "Savings Goal",
  "budgeted": "200.00", // Updated budgeted amount for June 2025
  // ... other category fields relevant to the month
}
Epic 2: Core Transaction Endpoint Implementation & Enhancement Tools
6. list_transactions
Description: Lists all transactions for a budget, with optional filtering by date and type.
YNAB API: GET /budgets/{budget_id}/transactions
MCP Command Example: list_transactions since_date=2025-05-01 type=unapproved
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
since_date (string, optional, format YYYY-MM-DD): Returns transactions on or after this date.
type (string, optional, enum: uncategorized, unapproved): Filters by transaction type. If omitted, returns all types (excluding deleted).
Example MCP Input:
JSON

{
  "since_date": "2025-05-01",
  "type": "unapproved"
}
Success Response: An array of YNAB TransactionDetail objects (with amounts converted to currency strings).
JSON

{
  "transactions": [
    {
      "id": "t1...",
      "date": "2025-05-02",
      "amount": "-25.50",
      "payee_name": "Coffee Shop",
      "approved": false,
      // ... other TransactionDetail fields
    }
  ],
  "transaction_count": 1
}
7. get_transaction_by_id
Description: Retrieves the complete details for a single specific transaction by its ID.
YNAB API: GET /budgets/{budget_id}/transactions/{transaction_id}
MCP Command Example: get_transaction_by_id transaction_id=txn_abc123
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
transaction_id (string, required): The ID of the transaction.
Example MCP Input:
JSON

{ "transaction_id": "t1a2b3c4-d5e6..." }
Success Response: A single YNAB TransactionDetail object (with amounts converted, including subtransactions).
JSON

{
  "id": "t1a2b3c4-d5e6...",
  "date": "2025-05-10",
  "amount": "-100.00",
  "payee_name": "Supermarket",
  "approved": true,
  "subtransactions": [
    { "id": "st1...", "amount": "-60.00", "category_name": "Groceries" },
    { "id": "st2...", "amount": "-40.00", "category_name": "Household" }
  ]
  // ... other TransactionDetail fields
}
8. create_transaction (Enhanced)
Description: Creates a new single transaction, with support for all available YNAB API parameters including subtransactions (splits). Amounts are input in currency units.
YNAB API: POST /budgets/{budget_id}/transactions
MCP Command Example (Simple): create_transaction accountId=acc_id date=2025-05-18 amount=12.34 payeeName="Lunch Place" categoryId=cat_food
MCP Command Example (Split): create_transaction accountId=acc_id date=2025-05-18 amount=100 payeeName="Electronics Store" subtransactions='[{"amount": 60, "categoryId": "cat_electronics"}, {"amount": 40, "categoryId": "cat_software"}]'
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
accountId (string, required): Account ID for the transaction.
date (string, required, format YYYY-MM-DD).
amount (number, required): Total transaction amount in currency units (e.g., 12.34 for $12.34).
payeeId (string, optional): ID of the payee.
payeeName (string, optional): Name of the payee (max 50 chars). One of payeeId or payeeName is typically needed unless it's a transfer.
categoryId (string, optional): Category ID for the transaction (not used if subtransactions are provided with their own categories).
memo (string, optional, max 200 chars).
cleared (string, optional, enum: "cleared", "uncleared", "reconciled"). Maps to ynab.TransactionClearedStatus.
approved (boolean, optional, defaults to false).
flagColor (string, optional, enum: "red", "orange", "yellow", "green", "blue", "purple"). Maps to ynab.TransactionFlagColor.
import_id (string, optional, max 36 chars): For matching with bank imports.
subtransactions (array, optional): Array of subtransaction objects:
amount (number, required): Amount of the subtransaction in currency units.
payeeId (string, optional).
payeeName (string, optional, max 50 chars).
categoryId (string, optional).
memo (string, optional, max 200 chars).
Example MCP Input (Split Transaction):
JSON

{
  "accountId": "acc_id_xyz",
  "date": "2025-05-18",
  "amount": 100.00,
  "payeeName": "Electronics Store",
  "subtransactions": [
    { "amount": 60.00, "categoryId": "cat_electronics_guid", "memo": "New Gadget" },
    { "amount": 40.00, "categoryId": "cat_software_guid", "memo": "Accessory App" }
  ]
}
Success Response:
JSON

{
  "success": true,
  "transactionId": "new_txn_guid",
  "message": "Transaction created successfully",
  // May also include transaction_ids, duplicate_import_ids, etc. from YNAB's response.
  // The current CreateTransactionTool returns transaction (singular), the YNAB API may return more.
  // YNAB POST /transactions returns { data: { transaction_ids: string[], transaction: TransactionDetail (if single), transactions: TransactionDetail[] (if multiple, less common here), duplicate_import_ids: string[] } }
  // For a single transaction creation, it returns the full TransactionDetail object in `response.data.transaction`.
  "transaction": { /* Full TransactionDetail of the created transaction */ }
}
9. update_transaction
Description: Updates any mutable field of an existing transaction, including its subtransactions.
YNAB API: PUT /budgets/{budget_id}/transactions/{transaction_id}
MCP Command Example: update_transaction transaction_id=txn_abc123 memo="Updated item" amount=55.00
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
transaction_id (string, required): The ID of the transaction to update.
All other fields from the enhanced create_transaction input schema are optional and can be provided to update the transaction. (e.g., accountId, date, amount, payeeId, payeeName, categoryId, memo, cleared, approved, flagColor, import_id, subtransactions).
Example MCP Input:
JSON

{
  "transaction_id": "t1a2b3c4-d5e6...",
  "memo": "Corrected memo and amount",
  "amount": 55.00, // New total amount in currency units
  "approved": true
}
Success Response: The updated YNAB TransactionDetail object (with amounts converted).
JSON

{
  "id": "t1a2b3c4-d5e6...",
  "memo": "Corrected memo and amount",
  "amount": "-55.00",
  "approved": true,
  // ... other TransactionDetail fields
}
10. delete_transaction
Description: Deletes a specific transaction by its ID.
YNAB API: DELETE /budgets/{budget_id}/transactions/{transaction_id}
MCP Command Example: delete_transaction transaction_id=txn_abc123
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
transaction_id (string, required): The ID of the transaction to delete.
Example MCP Input:
JSON

{ "transaction_id": "t1a2b3c4-d5e6..." }
Success Response: The YNAB TransactionDetail of the deleted transaction (with amounts converted).
JSON

{
  "id": "t1a2b3c4-d5e6...",
  "deleted": true,
  // ... other fields of the deleted transaction
}
11. list_account_transactions
Description: Lists all transactions for a specific account within a budget.
YNAB API: GET /budgets/{budget_id}/accounts/{account_id}/transactions
MCP Command Example: list_account_transactions account_id=acc_xyz since_date=2025-04-01
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
account_id (string, required): The ID of the account.
since_date (string, optional, format YYYY-MM-DD).
type (string, optional, enum: uncategorized, unapproved).
Success Response: An array of YNAB TransactionDetail objects (amounts converted).
12. list_category_transactions
Description: Lists all transactions for a specific category within a budget.
YNAB API: GET /budgets/{budget_id}/categories/{category_id}/transactions
MCP Command Example: list_category_transactions category_id=cat_xyz since_date=2025-01-01
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
category_id (string, required): The ID of the category.
since_date (string, optional, format YYYY-MM-DD).
type (string, optional, enum: uncategorized, unapproved).
Success Response: An array of YNAB HybridTransaction objects (amounts converted). Note: HybridTransaction is used by this specific YNAB endpoint.
13. list_payee_transactions
Description: Lists all transactions for a specific payee within a budget.
YNAB API: GET /budgets/{budget_id}/payees/{payee_id}/transactions
MCP Command Example: list_payee_transactions payee_id=payee_xyz
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
payee_id (string, required): The ID of the payee.
since_date (string, optional, format YYYY-MM-DD).
type (string, optional, enum: uncategorized, unapproved).
Success Response: An array of YNAB HybridTransaction objects (amounts converted).
Epic 3: Bulk Transaction Operations Tools
14. create_bulk_transactions
Description: Creates multiple new transactions in a single API call. Subtransactions are not supported for individual items in this bulk call. Amounts are input in currency units.
YNAB API: POST /budgets/{budget_id}/transactions/bulk
MCP Command Example: create_bulk_transactions transactions='[{"accountId": "id1", "date": "2025-05-18", "amount": 10, "payeeName": "P1"}, {"accountId": "id2", "date": "2025-05-19", "amount": 20, "payeeName": "P2"}]'
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
transactions (array, required): An array of transaction objects to create. Each object should follow the structure of SaveTransaction (similar to create_transaction input, but without subtransactions field).
accountId (string, required)
date (string, required, format YYYY-MM-DD)
amount (number, required, in currency units)
payeeId (string, optional)
payeeName (string, optional)
categoryId (string, optional)
memo (string, optional)
cleared (string, optional)
approved (boolean, optional)
flagColor (string, optional)
import_id (string, optional)
Example MCP Input:
JSON

{
  "transactions": [
    { "accountId": "acc_id1", "date": "2025-05-18", "amount": 10.50, "payeeName": "Vendor A", "categoryId": "cat_id1" },
    { "accountId": "acc_id1", "date": "2025-05-19", "amount": 22.00, "payeeName": "Vendor B", "categoryId": "cat_id2", "approved": true }
  ]
}
Success Response: YNAB BulkResponse object.
JSON

{
  "bulk": {
    "transaction_ids": ["t1_guid", "t2_guid"],
    "duplicate_import_ids": []
  }
}
15. update_bulk_transactions
Description: Updates multiple existing transactions in a single API call (e.g., for bulk approval or categorization). Subtransactions are not updated via this endpoint. Amounts are input in currency units.
YNAB API: PATCH /budgets/{budget_id}/transactions (Note: YNAB API uses PATCH for bulk updates, not PUT)
MCP Command Example: update_bulk_transactions transactions='[{"id": "txn1", "approved": true}, {"id": "txn2", "categoryId": "cat_id_new"}]'
Parameters:
budgetId (string, optional): Defaults to YNAB_BUDGET_ID.
transactions (array, required): An array of transaction objects to update. Each object must include id (the transaction ID) and any fields to be updated (from SaveTransaction structure, excluding subtransactions).
id (string, required)
... (other optional fields like accountId, date, amount, payeeId, payeeName, categoryId, memo, cleared, approved, flagColor, import_id)
Example MCP Input:
JSON

{
  "transactions": [
    { "id": "t1a2b3c4...", "approved": true, "categoryId": "cat_id_food" },
    { "id": "t5x6y7z8...", "memo": "Updated bulk memo", "amount": 75.00 }
  ]
}
Success Response: YNAB BulkResponse object.
JSON

{
  "bulk": {
    "transaction_ids": ["t1a2b3c4...", "t5x6y7z8..."],
    "duplicate_import_ids": []
  }
}
Change Log
Change	Date	Version	Description	Author
Initial draft	2025-05-18	0.1	Initial API reference for new and enhanced MCP tools.	3-Architect