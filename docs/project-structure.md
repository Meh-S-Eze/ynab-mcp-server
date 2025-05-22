ynab-mcp-server API Enhancement Project Structure
This document outlines the directory and file structure for the ynab-mcp-server API Enhancement project, building upon the existing structure.

Plaintext

ynab-mcp-server/
├── .cursor/                    # Cursor AI rules (existing)
│   └── rules/
│       └── ynabapi.mdc
├── .vscode/                    # VSCode specific settings (e.g., launch.json)
├── dist/                       # Compiled JavaScript output (git-ignored)
│   ├── index.js                # Main server entry point (compiled)
│   └── tools/                  # Compiled tools
├── docs/                       # Project documentation (THIS DIRECTORY)
│   ├── architecture.md         # Main architecture document
│   ├── tech-stack.md           # Technology stack
│   ├── project-structure.md    # This file
│   ├── coding-standards.md     # Coding standards and patterns
│   ├── api-reference.md        # MCP Tool API Reference
│   ├── data-models.md          # Data models and schemas
│   ├── environment-vars.md     # Environment variable documentation
│   └── testing-strategy.md     # Testing strategy
├── node_modules/               # Project dependencies (git-ignored)
├── src/                        # Application source code
│   ├── index.ts                # Main server entry point
│   └── tools/                  # MCP Tool implementations
│       ├── ApproveTransactionTool.ts
│       ├── BudgetSummaryTool.ts
│       ├── CreateTransactionTool.ts
│       ├── GetUnapprovedTransactionsTool.ts
│       ├── ListBudgetsTool.ts
│       │
│       ├── ListCategoriesTool.ts               # NEW (Epic 1)
│       ├── GetCategoryTool.ts                  # NEW (Epic 1)
│       ├── GetCategoryByMonthTool.ts           # NEW (Epic 1)
│       ├── UpdateCategoryTool.ts               # NEW (Epic 1)
│       ├── UpdateMonthCategoryTool.ts          # NEW (Epic 1)
│       │
│       ├── ListTransactionsTool.ts             # NEW (Epic 2)
│       ├── GetTransactionByIdTool.ts         # NEW (Epic 2)
│       ├── UpdateTransactionTool.ts            # NEW (Epic 2, enhances ApproveTransactionTool)
│       ├── DeleteTransactionTool.ts            # NEW (Epic 2)
│       ├── ListAccountTransactionsTool.ts      # NEW (Epic 2)
│       ├── ListCategoryTransactionsTool.ts     # NEW (Epic 2)
│       ├── ListPayeeTransactionsTool.ts        # NEW (Epic 2)
│       │
│       ├── CreateBulkTransactionsTool.ts       # NEW (Epic 3)
│       └── UpdateBulkTransactionsTool.ts       # NEW (Epic 3)
│
├── .gitignore                  # Git ignore rules
├── CHANGELOG.md                # Project changelog
├── package-lock.json           # Exact dependency versions
├── package.json                # Project manifest, dependencies, and scripts
├── README.md                   # Main project README (to be updated per Epic 4)
├── smithery.yaml               # Smithery configuration
├── tsconfig.json               # TypeScript compiler configuration
└── vitest.config.ts            # Vitest testing configuration
Key Directory Descriptions:
.cursor/: Contains rules for AI-assisted development (Cursor).
.vscode/: Workspace settings for Visual Studio Code, like launch.json for debugging.
dist/: Output directory for compiled TypeScript code. This directory is typically git-ignored.
docs/: Contains all architectural and project documentation, including this file.
node_modules/: Stores all npm dependencies. Git-ignored.
src/: Contains all the TypeScript source code for the server.
src/index.ts: The main entry point for the MCP server application. It initializes and starts the MCPServer.
src/tools/: This directory houses all the individual MCP tool implementations. Each tool is a .ts file, typically defining a class that extends MCPTool.
Root Directory Files:
.gitignore: Specifies intentionally untracked files that Git should ignore.
CHANGELOG.md: Records notable changes for each version.
package.json: Defines project metadata, dependencies, and npm scripts.
package-lock.json: Records the exact versions of dependencies.
README.md: Provides an overview of the project, setup instructions, and (to be updated) documentation for available tools.
smithery.yaml: Configuration for Smithery integration.
tsconfig.json: Configuration file for the TypeScript compiler.
vitest.config.ts: Configuration for the Vitest test runner.
Notes:
New tools as defined in the Epics will be added as new .ts files within the src/tools/ directory, following the existing naming convention (PascalCaseTool.ts).
The CreateTransactionTool.ts will be enhanced as per Epic 2.3.
The ApproveTransactionTool.ts might be deprecated or refactored if its functionality is fully covered by the more comprehensive UpdateTransactionTool.ts (from Epic 2.4). This decision should be confirmed during development.
Change Log
Change	Date	Version	Description	Author
Initial draft	2025-05-18	0.1	Initial project structure for API enhancement.	3-Architect