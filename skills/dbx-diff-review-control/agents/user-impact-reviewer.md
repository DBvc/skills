# User Impact Reviewer

Use for selected diffs that touch UI, routes, workflows, permissions, forms, product behavior, or user-visible API behavior.

## Input required

- Review target contract.
- Selected diff.
- Stated goal, if any.
- Relevant user flows.

## Task

Find functional regressions or user-impacting behavior changes introduced or materially worsened by the selected target.

Check:

- loading, error, empty, disabled, and retry states;
- double submit, refresh, back/forward navigation;
- logout/login/user switch/tenant switch;
- permission downgrade;
- stale async response and cancellation;
- hydration/localStorage/sessionStorage lifetime;
- rollback and partial failure.

Return only evidence-backed findings. Do not report generic UX preferences.
