# CRUSH.md

This file contains guidelines for agentic coding agents (such as yourself) that operate in this repository.

## Commands

- **Build:** `terraform validate`
- **Lint:** `terraform fmt --check`
- **Test:** `terraform test`

## Code Style

- **Formatting:** Use `terraform fmt` to format your code.
- **Naming Conventions:** Use `snake_case` for all variables and resources.
- **Types:** Use specific types whenever possible.
- **Error Handling:** Use `try()` for expressions that might fail.
- **Imports:** Use `terraform get` to download and update modules.
