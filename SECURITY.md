# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Updates

Security updates are released as soon as possible after a vulnerability is confirmed and a fix is available. We follow these principles:

- **Critical vulnerabilities**: Patched within 24-48 hours
- **High severity**: Patched within 1 week
- **Medium/Low severity**: Patched in next regular release

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing the project maintainers directly. Include as much information as possible:

### What to Include

1. **Type of vulnerability** (e.g., SQL injection, XSS, authentication bypass)
2. **Full path** to the vulnerable file(s)
3. **Location** of the affected source code (tag/branch/commit or direct URL)
4. **Step-by-step instructions** to reproduce the issue
5. **Proof-of-concept or exploit code** (if possible)
6. **Impact assessment** - what an attacker could do
7. **Suggested fix** (if you have one)

### What to Expect

After submitting a vulnerability report:

1. **Acknowledgment**: We'll acknowledge receipt within 48 hours
2. **Assessment**: We'll assess the vulnerability and determine severity
3. **Updates**: We'll provide regular updates on the status
4. **Fix timeline**: We'll provide an estimated timeline for the fix
5. **Disclosure**: We'll coordinate responsible disclosure with you

### Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 5 business days
- **Resolution**: Depends on severity (see Security Updates above)

## Security Best Practices

When using Perplexity Bridge Pro, follow these security best practices:

### API Keys and Secrets

- **Never commit API keys** to version control
- **Use environment variables** for all secrets (`.env` file)
- **Rotate keys regularly** (at least every 90 days)
- **Use strong, unique values** for `BRIDGE_SECRET`
- **Limit API key permissions** to minimum necessary

### Deployment

- **Use HTTPS** in production environments
- **Configure CORS** restrictively (don't use `allow_origins=["*"]` in production)
- **Enable rate limiting** to prevent abuse
- **Monitor logs** for suspicious activity
- **Keep dependencies updated** (use Dependabot)

### Network Security

- **Firewall configuration**: Restrict access to port 7860 as needed
- **Reverse proxy**: Use nginx or similar for production
- **IP whitelisting**: Restrict access to known IPs if possible
- **DDoS protection**: Use CloudFlare or similar services

### Access Control

- **Require authentication** for all sensitive endpoints
- **Validate API keys** on every request
- **Implement rate limiting** per IP and per key
- **Log authentication failures** for monitoring

## Known Security Considerations

### API Key Exposure

The application requires API keys for:
- Perplexity AI API (`PERPLEXITY_API_KEY`)
- Bridge authentication (`BRIDGE_SECRET`)
- GitHub Copilot API (`GITHUB_COPILOT_API_KEY`, optional)

**Risk**: Exposed API keys can lead to unauthorized access and API abuse.

**Mitigation**:
- Store keys in `.env` file (never in code)
- Add `.env` to `.gitignore`
- Use different keys for development and production
- Monitor API usage for anomalies

### Rate Limiting

Default rate limit: 10 requests per minute per IP.

**Risk**: Insufficient rate limiting could allow abuse or DoS attacks.

**Mitigation**:
- Adjust rate limits based on your use case
- Implement per-key rate limiting for production
- Monitor for rate limit violations

### Terminal Execution (if enabled)

The `/v1/terminal` endpoint allows command execution (if implemented).

**Risk**: Command injection vulnerabilities could allow arbitrary code execution.

**Mitigation**:
- Command allowlist enforcement
- Path restriction validation
- Timeout handling
- Input sanitization
- Disable if not needed

### CORS Configuration

Default CORS allows localhost origins.

**Risk**: Overly permissive CORS could allow unauthorized cross-origin requests.

**Mitigation**:
- Configure specific allowed origins in production
- Never use `allow_origins=["*"]` in production
- Use environment variables for production domains

### Dependency Vulnerabilities

Third-party dependencies may contain vulnerabilities.

**Mitigation**:
- Regular dependency updates (Dependabot configured)
- Security scanning (CodeQL configured)
- Monitor security advisories
- Use pinned versions for reproducibility

## Security Features

### Built-in Security

- **API key authentication**: Required for sensitive endpoints
- **Rate limiting**: SlowAPI integration for DoS prevention
- **Input validation**: Pydantic models for request validation
- **CORS configuration**: Middleware for cross-origin control
- **Logging**: Comprehensive logging for audit trails

### CI/CD Security

- **CodeQL scanning**: Automated security analysis
- **Dependabot**: Automated dependency updates
- **Pre-commit hooks**: Code quality and security checks
- **Type checking**: MyPy for type safety

## Compliance and Standards

This project follows security best practices including:

- **OWASP Top 10**: Protection against common web vulnerabilities
- **SANS Top 25**: Protection against common software errors
- **CWE/SANS**: Common Weakness Enumeration coverage
- **Secure coding practices**: Input validation, output encoding, authentication

## Security Audit History

| Date       | Type           | Findings | Status   |
|------------|----------------|----------|----------|
| 2026-01-20 | Internal Audit | 0 High   | Complete |

## Contact

For security-related questions or concerns that are not vulnerabilities:

- Create a GitHub issue with the `security` label
- For sensitive matters, contact maintainers directly

## Acknowledgments

We appreciate the security research community's efforts in responsibly disclosing vulnerabilities. Contributors who report valid security issues will be acknowledged (with permission) in:

- Security advisory documentation
- Release notes for the fix
- Project acknowledgments

Thank you for helping keep Perplexity Bridge Pro secure! 🔒
