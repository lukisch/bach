# Security Policy

## Important Security Notice

**This MCP server has full filesystem access with the permissions of the running user.**

By design, this server provides LLMs with powerful system access capabilities. Please understand the security implications before using it.

### High-Risk Tools

| Tool | Risk | Description |
|------|------|-------------|
| `fc_execute_command` | **Critical** | Executes arbitrary shell commands |
| `fc_start_process` | **High** | Starts background processes |
| `fc_kill_process` | **High** | Can terminate any accessible process |
| `fc_delete_file` | **High** | Permanently deletes files (no recycle bin) |
| `fc_delete_directory` | **High** | Recursively deletes directories |
| `fc_write_file` | **Medium** | Can overwrite any accessible file |

### Recommendations

1. **Use `fc_safe_delete`** instead of `fc_delete_file`/`fc_delete_directory` when possible - it moves items to the Recycle Bin instead of permanent deletion.

2. **Be cautious with `fc_execute_command`** - it runs commands with your full user permissions. Review commands before approving execution in your MCP client.

3. **Do not expose this server to untrusted networks.** It is designed for local use via stdio transport only.

4. **Review your MCP client's approval settings.** Most MCP clients (like Claude Desktop) prompt before executing destructive operations. Keep these prompts enabled.

### No Sandbox

This server does **not** implement:
- Path restrictions or allowlists
- Command filtering or blocklists
- Rate limiting
- Audit logging

These are intentional design decisions to keep the server simple and flexible. Security is delegated to the MCP client layer.

### Reporting Vulnerabilities

If you discover a security vulnerability, please open an issue on the GitHub repository. For sensitive disclosures, please use GitHub's private vulnerability reporting feature.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.3.x   | Yes       |
| < 1.3   | No        |
