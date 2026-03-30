Review the backend service or file: $ARGUMENTS

1. **Locate the target** from $ARGUMENTS.
   It could be a file path, folder, or service name. Read it directly.
   If not found, ask the user for the full path.

2. **Run static checks** (do not execute — analyse statically):

   **ESLint / Prettier / tsconfig**
   - Flag any code that violates common ESLint rules (unused vars, no-explicit-any, etc.)
   - Flag formatting issues that Prettier would catch (indentation, trailing commas, quotes)
   - Flag TypeScript issues: missing types, use of `any`, incorrect tsconfig paths

3. **DDD Pattern Compliance**
   - Verify separation: domain → application → infrastructure → interface
   - Flag any business logic leaking into handlers or infrastructure layer
   - Flag any direct DB calls from use-cases or domain entities
   - Flag missing repository interfaces (direct implementation usage instead of abstraction)

4. **Redundant Code**
   - Identify dead code, unused imports, duplicate logic
   - For each: either suggest removal or highlight with reason

5. **Performance**
   - Flag slow SQL patterns: missing WHERE clauses, SELECT *, N+1 queries, missing indexes
   - Flag unoptimised loops or repeated DB calls that could be batched

6. **Security (OWASP)**
   - SQL injection risks (raw queries without parameterisation)
   - Missing input validation or sanitisation
   - Hardcoded secrets or credentials
   - Overly permissive CORS or IAM policies in serverless.yml
   - Sensitive data exposed in logs or API responses

7. **Mintlify Doc Comments**
   - Flag any exported function, class, or interface missing a JSDoc/Mintlify comment
   - Suggest the comment if missing

8. **OpenAPI / API Documentation**
   - If a new route or endpoint is found, check if `openapi.yaml` has a matching entry
   - If missing, generate the OpenAPI path entry for it

9. **Output the review** in this format:

   ```
   CODE REVIEW: <file or service name>
   =====================================
   Critical (must fix):   [list]
   Warning (should fix):  [list]
   Suggestion (optional): [list]
   Verdict: PASS / NEEDS WORK
   ```

10. **Provide fixes** for all Critical and Warning items.
    Show only the changed sections as diffs, not the entire file.

11. **Flag anything unclear**:
    ```
    QUESTIONS FOR THE DEVELOPER:
    ============================
    - [ ] <question>
    ```
