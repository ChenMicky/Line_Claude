# Line Chatbot MCP Setup

This project is configured to use the Line Chatbot MCP (Model Context Protocol) server, which enables Claude to interact with Line messaging features.

## Configuration Files

### 1. `.mcp.json`
Defines the Line Chatbot MCP server configuration:
- **Server Name**: `line-chatbot`
- **Command**: Uses `npx` to run `@line/mcp-server`
- **Environment Variables**:
  - `LINE_CHANNEL_ACCESS_TOKEN`: Your Line channel access token
  - `LINE_CHANNEL_SECRET`: Your Line channel secret

### 2. `.claude/settings.local.json`
Enables the Line Chatbot MCP server for Claude Code sessions:
- `enabledMcpjsonServers`: Includes `"line-chatbot"` to activate the server

## Setup Instructions

### Prerequisites
1. Install Node.js (for running the MCP server via npx)
2. Have a Line Developer account and channel configured

### Environment Variables Setup
Set the required environment variables before running Claude:

```bash
export LINE_CHANNEL_ACCESS_TOKEN="your_line_channel_access_token"
export LINE_CHANNEL_SECRET="your_line_channel_secret"
```

### Verification
To verify the MCP server is properly configured:

1. Start Claude Code in this project directory
2. The Line Chatbot MCP server should be automatically enabled
3. Claude will be able to use Line messaging capabilities

## Usage

Once configured, Claude can:
- Send messages through Line
- Receive and process Line webhook events
- Manage Line messaging features

## Troubleshooting

### Common Issues

1. **MCP Server Not Starting**
   - Ensure Node.js is installed
   - Verify environment variables are set
   - Check that `@line/mcp-server` is available

2. **Authentication Errors**
   - Verify your Line channel credentials
   - Ensure tokens have proper permissions

3. **Claude Can't Access MCP Server**
   - Confirm the server is listed in `enabledMcpjsonServers`
   - Check for any permission conflicts in settings

## Security Notes

- Keep your Line channel credentials secure
- Never commit sensitive tokens to version control
- Use environment variables or secure secret management
- Review Line API permissions regularly