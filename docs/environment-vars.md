ynab-mcp-server API Enhancement Environment Variables
This document lists the environment variables used by the ynab-mcp-server API Enhancement application.

Configuration Loading Mechanism
Environment variables are accessed directly via process.env within the Node.js runtime. For local development, these can be set using a .env file loaded by a library like dotenv (though dotenv is not explicitly listed as a direct dependency in the provided package.json, it's a common practice; mcp-framework or its dependencies might handle this, or it's assumed to be managed by the development environment/scripts). The smithery.yaml also defines how these are passed when using Smithery.

Required Variables
Variable Name	Description	Example / Default Value	Required?	Sensitive? (Yes/No)
YNAB_API_TOKEN	Your Personal Access Token for the YNAB API. Used to authenticate all requests to the YNAB API.	abc123xyz789_your_personal_access_token	Yes	Yes
YNAB_BUDGET_ID	The ID of the default YNAB budget to use if a specific budgetId is not provided as a parameter to a tool.	your_budget_id_guid (e.g., a1b2c3d4-e5f6...)	No	No

## Additional Notes from Architecture Part 8

### Secrets Management:

The YNAB_API_TOKEN is a sensitive credential and must not be hardcoded into the source code or committed to version control.
For local development, use a .env file (added to .gitignore) or your shell's environment variable mechanisms.
When deploying or sharing (e.g., via Smithery), the environment variable mechanism of the host or client platform should be used to securely provide this token.

### .env.example:
It is recommended to maintain an .env.example file in the repository with placeholder values to guide users on the required environment variables:

```plaintext
# .env.example
YNAB_API_TOKEN="your_ynab_personal_access_token_here"
YNAB_BUDGET_ID="your_optional_default_budget_id_here"
```

### Validation:

Tools that require YNAB_API_TOKEN (all tools interacting with the YNAB API) initialize the ynab.API client with process.env.YNAB_API_TOKEN || "". If the token is missing, the YNAB SDK will fail API calls. Some tools also have explicit checks (e.g., ListBudgetsTool).
Tools that use YNAB_BUDGET_ID as a default check for its presence if a budgetId parameter is not supplied, and provide an error message if neither is available.

### Change Log (from Architecture Part 8)
Change	Date	Version	Description	Author
Initial draft	2025-05-18	0.1	Documenting existing env var usage.	3-Architect