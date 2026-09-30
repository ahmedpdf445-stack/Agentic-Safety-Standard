# Security Overview

## Principles

- default deny
- least privilege
- explicit capabilities
- allowlist over denylist when practical
- deterministic governance over uncertain model output
- fail closed on budget and policy failures

## Threats addressed

- prompt injection
- tool injection
- command injection
- path traversal
- arbitrary code execution
- SSRF and untrusted destinations
- secret leakage
- privilege escalation
- malicious tool outputs
- resource exhaustion
- policy bypass

## Boundaries

- Filesystem: canonical path resolution and root restrictions
- Network: denied by default and require explicit capability
- Execution: sandbox blocks unsupported tools and dangerous command patterns
- Permissions: explicit allowlist and default deny

## Risk classification

The project follows a practical governance posture rather than claiming full secure enclaves or impossible guarantees. The implementation is designed to reduce risk where the system is explicitly within its trust boundaries.
