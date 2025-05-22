ynab-mcp-server API Enhancement Architecture Document
1. Technical Summary
This document outlines the architecture for the ynab-mcp-server API Enhancement project. The system is a Model Context Protocol (MCP) server built using the TypeScript language and the mcp-framework. Its primary purpose is to provide a comprehensive set of tools for interacting with the You Need A Budget (YNAB) API, specifically focusing on category and transaction management. The architecture emphasizes adding new, discrete tools that correspond to YNAB API v1 endpoints, ensuring full coverage as per the project goals. Configuration is handled via environment variables for the YNAB API token and an optional default budget ID.

2. High-Level Overview
The ynab-mcp-server acts as an intermediary between an MCP client (e.g., an AI agent or a CLI) and the YNAB API. Users interact with the server by invoking specific "tools" (MCP commands) with required parameters. Each tool is responsible for a specific YNAB API interaction, processing the input, calling the YNAB API via the official ynab-sdk-js, and then formatting the API response back to the MCP client. The architecture is stateless from the perspective of individual tool invocations, relying on the YNAB API as the source of truth.

Code snippet

graph TD
    MCPClientInterface["MCP Client (e.g., AI Agent, CLI)"] -- MCP Request (tool_name, params) --> YNABMCPServer["YNAB MCP Server (mcp-framework)"];
    subgraph YNABMCPServer
        ToolDispatcher["Tool Dispatcher"] -- Loads/Executes Tool --> SpecificToolInstance["Specific Tool Instance (e.g., ListCategoriesTool)"];
    end
    SpecificToolInstance -- Uses ynab-sdk-js --> YNABAPI["YNAB API v1"];
    YNABAPI -- API Response --> SpecificToolInstance;
    SpecificToolInstance -- Formats Result --> ToolDispatcher;
    ToolDispatcher -- MCP Response (result/error) --> MCPClientInterface;

    Environment["Environment Variables (YNAB_API_TOKEN, YNAB_BUDGET_ID)"] --> SpecificToolInstance;
3. Component View
The system is composed of the following key components:

MCP Server (mcp-framework):
Responsibility: Manages the Model Context Protocol, listens for incoming tool requests, dispatches requests to the appropriate tool, and sends responses back to the client.
Implementation: Provided by the mcp-framework library. The src/index.ts initializes and starts this server.
MCP Tools (e.g., ListCategoriesTool.ts, CreateTransactionTool.ts):
Responsibility: Each tool encapsulates the logic for a specific YNAB API interaction. This includes defining its name, description, input schema (using Zod), and the execution logic to call the YNAB API and process its response.
Implementation: TypeScript classes located in src/tools/, extending MCPTool from mcp-framework. Each tool instantiates ynab.API for YNAB communication.
YNAB SDK (ynab package):
Responsibility: Provides the necessary functions to authenticate with and make calls to the YNAB REST API. Handles low-level HTTP requests and response parsing.
Implementation: The official ynab JavaScript/TypeScript library.
Zod Schemas:
Responsibility: Define the expected structure, types, and validation rules for the input parameters of each MCP tool.
Implementation: Defined within each tool class using the zod library.
Environment Configuration:
Responsibility: Provides sensitive (API token) and default (budget ID) configuration to the tools.
Implementation: Standard Node.js process.env variables, typically loaded from a .env file during local development (though not explicitly managed by the server itself).
<!-- end list -->

Code snippet

graph TD
    subgraph "ynab-mcp-server Application"
        ServerCore["MCPServer (src/index.ts)"]
        ToolsDir["src/tools/"]

        subgraph ToolsDir
            ToolBase["MCPTool (mcp-framework)"]
            ListCategoriesTool["ListCategoriesTool.ts"]
            GetCategoryTool["GetCategoryTool.ts"]
            UpdateCategoryTool["UpdateCategoryTool.ts"]
            ListTransactionsTool["ListTransactionsTool.ts"]
            CreateTransactionTool["CreateTransactionTool.ts"]
            UpdateTransactionTool["UpdateTransactionTool.ts"]
            DeleteTransactionTool["DeleteTransactionTool.ts"]
            BulkTools["CreateBulkTransactionsTool.ts, UpdateBulkTransactionsTool.ts"]
            OtherTools["... (all other tools)"]
        end

        ToolBase <|-- ListCategoriesTool
        ToolBase <|-- GetCategoryTool
        ToolBase <|-- UpdateCategoryTool
        ToolBase <|-- ListTransactionsTool
        ToolBase <|-- CreateTransactionTool
        ToolBase <|-- UpdateTransactionTool
        ToolBase <|-- DeleteTransactionTool
        ToolBase <|-- BulkTools
        ToolBase <|-- OtherTools

        ServerCore --> ToolsDir

        ListCategoriesTool -- Uses --> YNABSDK["ynab.API (ynab SDK)"]
        GetCategoryTool -- Uses --> YNABSDK
        UpdateCategoryTool -- Uses --> YNABSDK
        ListTransactionsTool -- Uses --> YNABSDK
        CreateTransactionTool -- Uses --> YNABSDK
        UpdateTransactionTool -- Uses --> YNABSDK
        DeleteTransactionTool -- Uses --> YNABSDK
        BulkTools -- Uses --> YNABSDK
        OtherTools -- Uses --> YNABSDK

        ListCategoriesTool -- Defines --> ZodSchema1["Zod Input Schema"]
        GetCategoryTool -- Defines --> ZodSchema2["Zod Input Schema"]
        UpdateCategoryTool -- Defines --> ZodSchema3["Zod Input Schema"]
        ListTransactionsTool -- Defines --> ZodSchema4["Zod Input Schema"]
        CreateTransactionTool -- Defines --> ZodSchema5["Zod Input Schema"]
        UpdateTransactionTool -- Defines --> ZodSchema6["Zod Input Schema"]
        DeleteTransactionTool -- Defines --> ZodSchema7["Zod Input Schema"]
        BulkTools -- Defines --> ZodSchema8["Zod Input Schema"]
        OtherTools -- Defines --> ZodSchemaN["Zod Input Schema"]

    end

    YNABSDK -- Interacts with --> YNAB_API_Service["YNAB API (External Service)"]
    EnvironmentVars["Environment Variables (YNAB_API_TOKEN, YNAB_BUDGET_ID)"] --> YNABSDK
    EnvironmentVars --> ToolsDir
4. Key Architectural Decisions & Patterns
Framework Choice: Utilization of mcp-framework to handle MCP boilerplate and tool management. This is an existing decision being continued.
Tool-Based Architecture: Each distinct YNAB API endpoint interaction is encapsulated within its own MCP tool. This promotes modularity and clear separation of concerns.
Stateless Tools: Tools are designed to be stateless regarding YNAB data, fetching current data from the YNAB API on each execution. The YNAB API is the single source of truth.
Configuration via Environment Variables: YNAB_API_TOKEN and YNAB_BUDGET_ID are sourced from process.env, consistent with current practice.
Direct YNAB SDK Usage: Tools directly use the ynab SDK for API interactions.
Schema Definition with Zod: Input schemas for tools are defined using zod for robust validation, as established in the existing tools.
Error Handling: Errors from the YNAB API or internal tool logic are caught within the execute method of each tool and returned as part of the MCP response, typically as a string message or an object with an error property. logger from mcp-framework is used for server-side logging.
Naming Convention for Tools: New tools will follow the snake_case convention for their name property, as requested (e.g., list_categories, get_transaction_by_id). File names remain PascalCaseTool.ts.
5. Infrastructure and Deployment Overview
Cloud Provider(s): N/A (Primarily for local execution).
Core Services Used: N/A.
Infrastructure as Code (IaC): N/A.
Deployment Strategy: Local execution via npm run start or globally installed npx ynab-mcp-server after publishing. The smithery.yaml file defines how the server is started for clients like Claude Desktop using Smithery.
Environments: Primarily local development.
6. Key Reference Documents
docs/prd.md (Project Brief: ynab-mcp-server API Enhancement)
Epic files (Provided separately, detailing stories for new tools)
docs/tech-stack.md
docs/project-structure.md
docs/coding-standards.md
docs/api-reference.md (MCP Tool Reference)
docs/data-models.md
docs/environment-vars.md
docs/testing-strategy.md
YNAB API Documentation: https://api.ynab.com/
YNAB OpenAPI Specification: https://api.ynab.com/papi/open_api_spec.yaml
7. Change Log
Change	Date	Version	Description	Author
Initial draft	2025-05-18	0.1	Initial architecture document for API enhancement.	3-Architect