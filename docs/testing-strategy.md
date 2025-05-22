ynab-mcp-server API Enhancement Testing Strategy
This document outlines the strategy for testing the new and enhanced MCP tools within the ynab-mcp-server API Enhancement project. The project uses vitest as its testing framework, as indicated by vitest.config.ts and package.json.

1. Overall Philosophy & Goals
Goal 1: Ensure Correctness: Verify that each MCP tool correctly interacts with the YNAB API (or a mock thereof) and processes data according to its specified requirements (Epics and ACs).
Goal 2: Prevent Regressions: Establish a suite of tests that can be run to quickly identify if new changes break existing functionality.
Goal 3: Confidence in Refactoring: Allow developers (the primary user) to refactor code with confidence, knowing that tests will catch unintended side effects.
Goal 4: Validate Input Handling: Ensure robust handling of valid and invalid inputs to tools.
Focus: Testing will primarily focus on the individual logic of each tool, its interaction with the YNAB API interface, and input/output correctness.
2. Testing Levels
2.1 Unit Tests
Scope: Test individual functions or methods within a tool class in isolation. This is particularly relevant for:
Data transformation logic (e.g., converting milliunits to currency strings, formatting output).
Complex conditional logic within the execute method if not directly tied to API calls.
Helper methods within tool classes.
Tools: vitest.
Mocking/Stubbing:
The YNAB API (this.api calls) must be mocked for unit tests to avoid actual API calls and to provide controlled responses. vitest.spyOn or vi.fn() can be used to mock methods of the ynab.API instance.
process.env for YNAB_API_TOKEN and YNAB_BUDGET_ID can be managed using vitest.stubEnv or similar mechanisms if tests need to vary these.
Location: src/tools/__tests__/ToolName.test.ts or alongside source files (src/tools/ToolName.test.ts). The current vitest.config.ts includes src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}.
Expectations:
Cover critical logic paths within helper functions or data transformations.
Fast execution.
Each new tool should have unit tests for any significant non-API-interaction logic.
2.2 Integration Tests (Tool-Level against Mocked API)
Scope: Test each MCP tool's execute method as a whole, from input processing (Zod handles initial validation) to interaction with a mocked YNAB API, and finally to the structure/content of its return value.
Tools: vitest.
Mocking/Stubbing:
Mock the YNAB API client (this.api) methods to simulate various API responses (success, specific data, error conditions like "not found", "invalid token", rate limits).
This allows testing of the tool's response to different API outcomes and its error handling logic.
Location: Same as unit tests.
Expectations:
For each tool, have test cases covering:
Successful execution with valid inputs and expected API responses.
Handling of missing optional parameters (e.g., using YNAB_BUDGET_ID).
Correct error message propagation when the mocked YNAB API returns an error.
Correct data transformation of API responses.
Adherence to Acceptance Criteria defined in the Epics.
These will form the bulk of the automated tests.
2.3 End-to-End (E2E) / Manual Testing (MCP Client to Live API - Caution Advised)
Scope: Testing the full flow from an MCP client (e.g., mcp-cli, or the npm run debug inspector) to the live ynab-mcp-server interacting with the actual YNAB API.
Tools: Manual execution using an MCP client.
Environment: Requires a valid YNAB_API_TOKEN and potentially a dedicated test budget in YNAB to avoid impacting real financial data.
Expectations:
Due to the nature of this being a personal tool and the risks of interacting with a live financial API (especially for write operations), extensive automated E2E tests against the live API are not recommended as part of the primary CI/CD or frequent testing loop.
Manual E2E testing by the developer is crucial before considering a feature complete, especially for new tools or significant changes. This involves:
Running the server locally.
Using an MCP client to invoke the tool with various parameters.
Verifying the changes/data in the YNAB UI or via subsequent GET tool calls.
For read-only (GET) tools, automated E2E tests against the live YNAB API could be considered if a stable test budget is maintained, but this adds complexity and potential for flakiness due to API rate limits or external service changes.
Key Scenarios for Manual E2E:
Creating, reading, updating, and deleting categories.
Creating, reading, updating (including splits), and deleting transactions.
Bulk operations.
Edge cases for date formats, amounts, and optional parameters.
3. Test Data Management
Unit/Integration Tests:
Mocked request/response data for YNAB API calls will be defined directly within test files (e.g., sample Category objects, TransactionDetail objects, error responses).
Input data for tools will also be defined in test files.
Manual E2E Tests:
A dedicated test budget in YNAB is highly recommended to avoid corrupting real financial data. This budget can be pre-populated with sample categories, accounts, and transactions relevant to the scenarios being tested.
Be prepared to clean up or reset this test budget periodically.
4. CI/CD Integration
The package.json includes test: "vitest" and test:coverage: "vitest run --coverage".
Unit and integration tests (against mocked API) should be run automatically in any CI environment (e.g., GitHub Actions) on every push/PR.
Builds should fail if tests fail.
Coverage reports should be generated and reviewed.
5. Specific Testing Considerations for New Tools
Parameter Validation: While Zod handles schema validation, test how tools react to scenarios just outside Zod's scope if applicable, or how Zod errors are presented to the user by mcp-framework.
Milliunit Conversion: Explicitly test the correctness of currency-to-milliunit and milliunit-to-currency conversions.
Subtransactions: For create_transaction and update_transaction, thoroughly test the creation and modification of split transactions.
Bulk Operations: Test with empty arrays, arrays with one item, and arrays with multiple items. Test error handling if one item in a bulk request fails.
Idempotency: For update/create operations where import_id is used, test YNAB's idempotency behavior and ensure the tool handles duplicate import_id responses correctly (as per YNAB API spec).
Change Log
Change	Date	Version	Description	Author
Initial draft	2025-05-18	0.1	Initial testing strategy for API enhancement project.	3-Architect