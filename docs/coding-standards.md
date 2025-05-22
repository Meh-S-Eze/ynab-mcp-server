ynab-mcp-server API Enhancement Coding Standards and Patterns
This document outlines coding standards, patterns, and best practices to be followed for the ynab-mcp-server API Enhancement project, ensuring consistency and maintainability.

1. Architectural / Design Patterns Adopted
Tool-Based Architecture (via mcp-framework): Each piece of functionality corresponding to a YNAB API endpoint is implemented as a discrete "Tool" class extending MCPTool.
Rationale: Modularity, clear separation of concerns, and alignment with the mcp-framework.
Dependency Injection (Implicit): The ynab.API instance is created within each tool's constructor. While not formal DI, it centralizes API client creation. Environment variables are accessed via process.env.
Schema-First Input Validation: Tool inputs are defined and validated using zod schemas.
Rationale: Ensures type safety and robust input validation before processing.
Service Facade (YNAB SDK): The ynab SDK acts as a facade to the underlying YNAB REST API, abstracting direct HTTP calls.
2. Coding Standards
Primary Language: TypeScript (^5.3.3 as per package.json).
Primary Runtime: Node.js (>=20.0.0 as per mcp-framework requirements).
Style Guide & Linter:
While not explicitly defined in package.json (e.g., ESLint, Prettier), the existing code demonstrates a consistent style. Adhere to this style.
Recommendation: Consider adding Prettier and ESLint with a standard configuration (e.g., eslint-config-airbnb-typescript or eslint:recommended + plugin:@typescript-eslint/recommended) to enforce consistency automatically.
Naming Conventions:
Tool Names (MCP Exposed): snake_case (e.g., list_categories, create_transaction) as requested for user-facing tool invocation.
File Names: PascalCaseTool.ts for tool classes (e.g., ListCategoriesTool.ts).
Classes & Interfaces: PascalCase (e.g., ListCategoriesTool, CreateTransactionInput).
Methods & Functions: camelCase (e.g., execute, transformTransactions).
Variables & Parameters: camelCase (e.g., budgetId, milliunitAmount).
Constants: UPPER_SNAKE_CASE if applicable (though less common in this project's style).
Type Aliases/Interfaces for Zod Schemas: PascalCase suffixed with Input or Output if not directly the main interface (e.g. ListCategoriesInput).
File Structure: Adhere to the layout defined in docs/project-structure.md. New tools go into src/tools/.
Asynchronous Operations: Consistently use async/await for all asynchronous operations, especially YNAB API calls.
Type Safety:
Leverage TypeScript's strict mode (enabled in tsconfig.json).
Define clear interfaces for function/method parameters and return types.
Use Zod for runtime validation of external inputs to tools.
YNAB SDK types (e.g., ynab.TransactionDetail, ynab.Category) should be used where appropriate.
Comments & Documentation:
Each tool class must have a name (string literal, snake_case) and description (string literal, user-friendly) property.
The schema object within each tool must have a description for each parameter.
Use JSDoc-style comments for public methods and complex internal logic.
Code should be as self-documenting as possible.
Dependency Management:
Use npm for package management.
Keep dependencies updated, regularly review for security vulnerabilities.
Avoid adding unnecessary dependencies.
Modularity:
Each tool should be self-contained as much as possible, with its logic primarily within its execute method.
Helper/utility functions specific to a tool can be private methods within the tool class. Truly general utilities (if any arise) could be in a src/common/ or src/utils/ directory.
3. Error Handling Strategy
General Approach:
Use try...catch blocks within the execute method of tools to handle errors from YNAB API calls or other internal logic.
Throw standard Error objects for input validation failures not caught by Zod or for unexpected conditions (e.g., throw new Error("No budget ID provided...")).
The mcp-framework will likely catch unhandled exceptions from execute and translate them into an MCP error response.
Logging:
Use the logger instance imported from mcp-framework for server-side logging.
logger.info() for informational messages (e.g., "Listing budgets").
logger.error() for caught errors, including stringified error objects for detail.
Avoid logging sensitive information directly unless necessary for debugging and properly secured.
Specific Handling Patterns:
YNAB API Errors: The ynab SDK typically throws errors that can be caught. Inspect these errors for details (e.g., error.error.detail from YNAB's error response structure). Relay a user-friendly and informative message back to the MCP client.
TypeScript

try {
  // ... YNAB API call
} catch (error: any) { // Or a more specific type if known from ynab-sdk-js
  logger.error(`Error interacting with YNAB API for ${this.name}: ${JSON.stringify(error)}`);
  let detail = "An unexpected error occurred with the YNAB API.";
  if (error && error.error && error.error.detail) {
    detail = error.error.detail;
  } else if (error instanceof Error) {
    detail = error.message;
  }
  return `YNAB API Error: ${detail}`; // Or return an error object
}
Input Validation: Zod handles initial input validation. If further custom validation is needed within execute, throw an Error with a clear message.
Return Values on Error: Tools should return a string message (as seen in existing tools) or a structured object indicating failure, e.g., { success: false, error: "message" }. Consistency is key. The current pattern seems to be returning a string directly for errors or an object for success. This should be standardized. Recommendation: Standardize on returning an object like { success: boolean, data?: any, error?: string } for all tools. For now, follow the mixed pattern if strict consistency with existing tools is paramount. Given the epics, a structured success object is often used (e.g. for create_transaction).
4. YNAB Specific Patterns
API Client Initialization: this.api = new ynab.API(process.env.YNAB_API_TOKEN || ""); in the constructor of each tool.
Budget ID Handling: Prioritize input.budgetId if provided, otherwise use this.budgetId (from process.env.YNAB_BUDGET_ID). If neither is available, throw/return an error.
Milliunit Conversion:
For amounts sent to YNAB (e.g., creating/updating transactions, budgeting): Convert currency units (e.g., dollars) from tool input to milliunits (Math.round(input.amount * 1000)). Clearly document in tool schema descriptions that input amounts are in currency units.
For amounts received from YNAB: Convert milliunits back to currency units for display/return to the user (e.g., (transaction.amount / 1000).toFixed(2)).
Date Formatting: YNAB API typically uses ISO 8601 date strings (YYYY-MM-DD). Ensure tool inputs requiring dates specify this format in their Zod schema description and that dates are passed correctly.
Rate Limiting: Be mindful of the YNAB API rate limit (200 requests/hour/token). Bulk operations should be preferred where available and applicable. Tools that might perform many individual calls in rapid succession (if any were designed) would need careful consideration, though current tools are single-call.
5. Security Best Practices
API Token: The YNAB_API_TOKEN is sensitive and handled via environment variables. It's correctly not logged or exposed directly to the MCP client.
Input Sanitization/Validation: Zod provides primary input validation. Avoid constructing API query parameters or other sensitive strings directly from unvalidated input if Zod isn't covering a specific case (though it generally should).
Dependency Security: Regularly audit dependencies for known vulnerabilities (e.g., using npm audit).
Least Privilege: The YNAB API token likely has full access. This is a personal tool, so the risk profile is different, but be aware.
Change Log
Change	Date	Version	Description	Author
Initial draft	2025-05-18	0.1	Initial coding standards for API enhancement.	3-Architect