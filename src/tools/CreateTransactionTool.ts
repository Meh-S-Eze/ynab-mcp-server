import { MCPTool } from "mcp-framework";
import { z } from "zod";
import * as ynab from "ynab";

interface CreateTransactionInput {
  budgetId: string;
  accountId: string;
  date: string;
  amount: number;
  payeeId?: string;
  payeeName?: string;
  categoryId?: string;
  memo?: string;
  cleared?: boolean;
  approved?: boolean;
  flagColor?: string;
}

class CreateTransactionTool extends MCPTool<CreateTransactionInput> {
  name = "create_transaction";
  description = "Creates a new transaction in your YNAB budget. Either payee_id or payee_name must be provided in addition to the other required fields.";

  private api: ynab.API;

  constructor() {
    super();
    this.api = new ynab.API(process.env.YNAB_API_TOKEN || "");
  }

  schema = {
    budgetId: {
      type: z.string(),
      description: "The id of the budget to create the transaction in",
    },
    accountId: {
      type: z.string(),
      description: "The id of the account to create the transaction in",
    },
    date: {
      type: z.string(),
      description: "The date of the transaction in ISO format (e.g. 2024-03-24)",
    },
    amount: {
      type: z.number(),
      description: "The amount in milliunits (e.g. 10.99 should be provided as 10990)",
    },
    payeeId: {
      type: z.string().optional(),
      description: "The id of the payee (optional if payee_name is provided)",
    },
    payeeName: {
      type: z.string().optional(),
      description: "The name of the payee (optional if payee_id is provided)",
    },
    categoryId: {
      type: z.string().optional(),
      description: "The category id for the transaction (optional)",
    },
    memo: {
      type: z.string().optional(),
      description: "A memo/note for the transaction (optional)",
    },
    cleared: {
      type: z.boolean().optional(),
      description: "Whether the transaction is cleared (optional, defaults to false)",
    },
    approved: {
      type: z.boolean().optional(),
      description: "Whether the transaction is approved (optional, defaults to false)",
    },
    flagColor: {
      type: z.string().optional(),
      description: "The transaction flag color (red, orange, yellow, green, blue, purple) (optional)",
    },
  };

  async execute(input: CreateTransactionInput) {
    if(!input.payeeId && !input.payeeName) {
      throw new Error("Either payee_id or payee_name must be provided");
    }

    try {
      const transaction: ynab.PostTransactionsWrapper = {
        transaction: {
          account_id: input.accountId,
          date: input.date,
          amount: input.amount,
          payee_id: input.payeeId,
          payee_name: input.payeeName,
          category_id: input.categoryId,
          memo: input.memo,
          cleared: input.cleared ? ynab.TransactionClearedStatus.Cleared : ynab.TransactionClearedStatus.Uncleared,
          approved: input.approved ?? false,
          flag_color: input.flagColor as ynab.TransactionFlagColor,
        }
      };

      const response = await this.api.transactions.createTransaction(
        input.budgetId,
        transaction
      );

      if (!response.data.transaction) {
        throw new Error("Failed to create transaction - no transaction data returned");
      }

      return {
        success: true,
        transactionId: response.data.transaction.id,
        message: "Transaction created successfully",
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error occurred",
      };
    }
  }
}

export default CreateTransactionTool;
