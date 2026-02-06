# KoNote2 UX Walkthrough Report

**Generated:** 2026-02-06 11:36:07  
**Command:** `pytest tests/ux_walkthrough/ -v`

## Summary

| Metric | This Run | Previous |
|--------|----------|----------|
| Pages visited | 96 | 96 (same) |
| Critical issues | 1 | 1 (same) |
| Warnings | 81 | 81 (same) |
| Info items | 26 | 26 (same) |

## Critical Issues

- **[Program Manager] Target metrics** `/plans/targets/1/metrics/`
  Server error (500) on HTMX partial

## Warning Issues

- **[Front Desk (FR)] Home page (FR)** `/`
  Heading level skipped: <h1> followed by <h4>

- **[Front Desk (FR)] Client detail (FR)** `/clients/1/`
  Page has no <h1> element

- **[Front Desk (FR)] Programs list (FR)** `/programs/`
  Heading level skipped: <h1> followed by <h3>

- **[Front Desk] Home page** `/`
  Heading level skipped: <h1> followed by <h4>

- **[Front Desk] Client list** `/clients/`
  Heading level skipped: <h1> followed by <h3>

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  Page has no <title> or title is empty

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  No <main> landmark element found

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  No <nav> element found on full page

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  No <html> element found

- **[Front Desk] Client detail** `/clients/1/`
  Page has no <h1> element

- **[Front Desk] Plan section create (403)** `/plans/client/1/sections/create/`
  403 page has very little content — may not be helpful

- **[Front Desk] Plan section create (403)** `/plans/client/1/sections/create/`
  403 page has no links — user may be stuck

- **[Front Desk] Programs list** `/programs/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Form validation — empty quick note** `/notes/client/1/quick/`
  Expected form errors but none found (no .errorlist elements)

- **[Direct Service] Form validation — empty quick note** `/notes/client/1/quick/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Home page** `/`
  Heading level skipped: <h1> followed by <h4>

- **[Direct Service] Client list** `/clients/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Create client form** `/clients/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Create client submit** `/clients/create/`
  Page has no <h1> element

- **[Direct Service] Client detail** `/clients/1/`
  Page has no <h1> element

- **[Direct Service] Edit client form** `/clients/1/edit/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Edit client submit** `/clients/1/edit/`
  Page has no <h1> element

- **[Direct Service] Consent submit** `/clients/1/consent/`
  Page has no <h1> element

- **[Direct Service] Quick note form** `/notes/client/1/quick/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Quick note submit** `/notes/client/1/quick/`
  Page has no <h1> element

- **[Direct Service] Full note form** `/notes/client/1/new/`
  Heading level skipped: <h2> followed by <h4>

- **[Direct Service] Notes timeline** `/notes/client/1/`
  Page has no <h1> element

- **[Direct Service] Plan view (read-only)** `/plans/client/1/`
  Page has no <h1> element

- **[Direct Service] Section create (403)** `/plans/client/1/sections/create/`
  403 page has very little content — may not be helpful

- **[Direct Service] Section create (403)** `/plans/client/1/sections/create/`
  403 page has no links — user may be stuck

- **[Direct Service] Events tab** `/events/client/1/`
  Page has no <h1> element

- **[Direct Service] Event create form** `/events/client/1/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Alert create form** `/events/client/1/alerts/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Direct Service] Client analysis** `/reports/client/1/analysis/`
  Page has no <h1> element

- **[Direct Service] Programs list** `/programs/`
  Heading level skipped: <h1> followed by <h3>

- **[Program Manager] Home page** `/`
  Heading level skipped: <h1> followed by <h4>

- **[Program Manager] Client list** `/clients/`
  Heading level skipped: <h1> followed by <h3>

- **[Program Manager] Client detail** `/clients/1/`
  Page has no <h1> element

- **[Program Manager] Notes timeline** `/notes/client/1/`
  Page has no <h1> element

- **[Program Manager] Quick note form** `/notes/client/1/quick/`
  Heading level skipped: <h1> followed by <h3>

- **[Program Manager] Full note form** `/notes/client/1/new/`
  Heading level skipped: <h2> followed by <h4>

- **[Program Manager] Plan view (editable)** `/plans/client/1/`
  Page has no <h1> element

- **[Program Manager] Section create form** `/plans/client/1/sections/create/`
  Page has no <h1> element

- **[Program Manager] Section create submit** `/plans/client/1/sections/create/`
  Page has no <h1> element

- **[Program Manager] Target create form** `/plans/sections/1/targets/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Program Manager] Target create submit** `/plans/sections/1/targets/create/`
  Page has no <h1> element

- **[Program Manager] Metrics export form** `/reports/export/`
  Heading level skipped: <h1> followed by <h3>

- **[Program Manager] CMT export form** `/reports/cmt-export/`
  Heading level skipped: <h1> followed by <h3>

- **[Program Manager] Events tab** `/events/client/1/`
  Page has no <h1> element

- **[Program Manager] Event create form** `/events/client/1/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Program Manager] Client analysis** `/reports/client/1/analysis/`
  Page has no <h1> element

- **[Executive] Programs list** `/programs/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Admin settings dashboard** `/admin/settings/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Terminology settings** `/admin/settings/terminology/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Feature toggles** `/admin/settings/features/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Instance settings** `/admin/settings/instance/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create metric form** `/plans/admin/metrics/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Programs list** `/programs/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create program form** `/programs/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] User list** `/admin/users/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create user form** `/admin/users/new/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Invite list** `/auth/invites/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create invite form** `/auth/invites/new/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Audit log** `/admin/audit/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Registration links** `/admin/registration/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create registration link** `/admin/registration/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Custom field admin** `/clients/admin/fields/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create field group** `/clients/admin/fields/groups/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create field definition** `/clients/admin/fields/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Event types list** `/events/admin/types/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Create event type** `/events/admin/types/create/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Note templates** `/admin/settings/note-templates/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Client data export form** `/reports/client-data-export/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Export links management** `/reports/export-links/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin] Diagnose charts** `/admin/settings/diagnose-charts/`
  Page has no <h1> element

- **[Admin] Pending submissions** `/admin/submissions/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin+PM] Client detail** `/clients/1/`
  Page has no <h1> element

- **[Admin+PM] Notes timeline** `/notes/client/1/`
  Page has no <h1> element

- **[Admin+PM] Plan view** `/plans/client/1/`
  Page has no <h1> element

- **[Admin+PM] Admin settings** `/admin/settings/`
  Heading level skipped: <h1> followed by <h3>

- **[Admin+PM] User list** `/admin/users/`
  Heading level skipped: <h1> followed by <h3>

## Info Issues

- **[Front Desk (FR)] Programs list (FR)** `/programs/`
  Table missing <caption> or aria-label

- **[Front Desk] Client list** `/clients/`
  Table missing <caption> or aria-label

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  No headings found on page

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  No <meta name="viewport"> tag found

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  No skip navigation link found

- **[Front Desk] Search for client** `/clients/search/?q=Jane`
  Table missing <caption> or aria-label

- **[Front Desk] Programs list** `/programs/`
  Table missing <caption> or aria-label

- **[Direct Service] Client list** `/clients/`
  Table missing <caption> or aria-label

- **[Direct Service] Client detail** `/clients/1/`
  "Note" button/link expected but not found for Direct Service

- **[Direct Service] Programs list** `/programs/`
  Table missing <caption> or aria-label

- **[Program Manager] Client list** `/clients/`
  Table missing <caption> or aria-label

- **[Executive] Programs list** `/programs/`
  Table missing <caption> or aria-label

- **[Admin] Terminology settings** `/admin/settings/terminology/`
  Table missing <caption> or aria-label

- **[Admin] Feature toggles** `/admin/settings/features/`
  Table missing <caption> or aria-label

- **[Admin] Programs list** `/programs/`
  Table missing <caption> or aria-label

- **[Admin] Program detail** `/programs/1/`
  Table missing <caption> or aria-label

- **[Admin] User list** `/admin/users/`
  Table missing <caption> or aria-label

- **[Admin] Invite list** `/auth/invites/`
  Table missing <caption> or aria-label

- **[Admin] Custom field admin** `/clients/admin/fields/`
  Table missing <caption> or aria-label

- **[Admin] Custom field admin** `/clients/admin/fields/`
  <th> missing scope attribute: "Field"

- **[Admin] Event types list** `/events/admin/types/`
  Table missing <caption> or aria-label

- **[Admin] Note templates** `/admin/settings/note-templates/`
  Table missing <caption> or aria-label

- **[Admin] Note templates** `/admin/settings/note-templates/`
  <th> missing scope attribute: "Name"

- **[Admin] Diagnose charts** `/admin/settings/diagnose-charts/`
  Table missing <caption> or aria-label

- **[Admin] Diagnose charts** `/admin/settings/diagnose-charts/`
  <th> missing scope attribute: "Library metrics"

- **[Admin+PM] User list** `/admin/users/`
  Table missing <caption> or aria-label

## Known Limitations

- Colour contrast not tested (requires browser rendering)
- Focus management after HTMX swaps not tested
- Visual layout / responsive behaviour not tested

## Per-Role Walkthrough Results

### Front Desk (FR)

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Home page (FR) | `/` | 200 | 1 issue(s) |
| Client detail (FR) | `/clients/1/` | 200 | 1 issue(s) |
| Programs list (FR) | `/programs/` | 200 | 2 issue(s) |

### Front Desk

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Home page | `/` | 200 | 1 issue(s) |
| Client list | `/clients/` | 200 | 2 issue(s) |
| Search for client | `/clients/search/?q=Jane` | 200 | 8 issue(s) |
| Client detail | `/clients/1/` | 200 | 1 issue(s) |
| Custom fields display | `/clients/1/custom-fields/display/` | 200 | None |
| Custom fields edit | `/clients/1/custom-fields/edit/` | 200 | None |
| Consent display | `/clients/1/consent/display/` | 200 | None |
| Create client (403) | `/clients/create/` | 403 | None |
| Notes list (403) | `/notes/client/1/` | 403 | None |
| Plan section create (403) | `/plans/client/1/sections/create/` | 403 | 2 issue(s) |
| Programs list | `/programs/` | 200 | 2 issue(s) |

### Direct Service

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Form validation errors | `/notes/client/1/quick/` | 200 | 2 issue(s) |
| Home page | `/` | 200 | 1 issue(s) |
| Client list | `/clients/` | 200 | 2 issue(s) |
| Create client form | `/clients/create/` | 200 | 1 issue(s) |
| Create client submit | `/clients/create/` | 200 | 1 issue(s) |
| Client detail | `/clients/1/` | 200 | 2 issue(s) |
| Edit client form | `/clients/1/edit/` | 200 | 1 issue(s) |
| Edit client submit | `/clients/1/edit/` | 200 | 1 issue(s) |
| Consent edit form | `/clients/1/consent/edit/` | 200 | None |
| Consent submit | `/clients/1/consent/` | 200 | 1 issue(s) |
| Custom fields edit | `/clients/1/custom-fields/edit/` | 200 | None |
| Quick note form | `/notes/client/1/quick/` | 200 | 1 issue(s) |
| Quick note submit | `/notes/client/1/quick/` | 200 | 1 issue(s) |
| Full note form | `/notes/client/1/new/` | 200 | 1 issue(s) |
| Notes timeline | `/notes/client/1/` | 200 | 1 issue(s) |
| Note detail | `/notes/1/` | 200 | None |
| Plan view (read-only) | `/plans/client/1/` | 200 | 1 issue(s) |
| Section create (403) | `/plans/client/1/sections/create/` | 403 | 2 issue(s) |
| Events tab | `/events/client/1/` | 200 | 1 issue(s) |
| Event create form | `/events/client/1/create/` | 200 | 1 issue(s) |
| Alert create form | `/events/client/1/alerts/create/` | 200 | 1 issue(s) |
| Client analysis | `/reports/client/1/analysis/` | 200 | 1 issue(s) |
| Programs list | `/programs/` | 200 | 2 issue(s) |

### Program Manager

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Home page | `/` | 200 | 1 issue(s) |
| Client list | `/clients/` | 200 | 2 issue(s) |
| Client detail | `/clients/1/` | 200 | 1 issue(s) |
| Notes timeline | `/notes/client/1/` | 200 | 1 issue(s) |
| Quick note form | `/notes/client/1/quick/` | 200 | 1 issue(s) |
| Full note form | `/notes/client/1/new/` | 200 | 1 issue(s) |
| Plan view (editable) | `/plans/client/1/` | 200 | 1 issue(s) |
| Section create form | `/plans/client/1/sections/create/` | 200 | 1 issue(s) |
| Section create submit | `/plans/client/1/sections/create/` | 200 | 1 issue(s) |
| Target create form | `/plans/sections/1/targets/create/` | 200 | 1 issue(s) |
| Target create submit | `/plans/sections/1/targets/create/` | 200 | 1 issue(s) |
| Target metrics | `/plans/targets/1/metrics/` | 500 | 1 issue(s) |
| Section status | `/plans/sections/1/status/` | 200 | None |
| Target status | `/plans/targets/1/status/` | 200 | None |
| Target history | `/plans/targets/1/history/` | 200 | None |
| Metrics export form | `/reports/export/` | 200 | 1 issue(s) |
| CMT export form | `/reports/cmt-export/` | 200 | 1 issue(s) |
| Events tab | `/events/client/1/` | 200 | 1 issue(s) |
| Event create form | `/events/client/1/create/` | 200 | 1 issue(s) |
| Client analysis | `/reports/client/1/analysis/` | 200 | 1 issue(s) |

### Executive

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Executive dashboard | `/clients/executive/` | 200 | None |
| Client list redirect | `/clients/` | 200 | None |
| Client detail redirect | `/clients/1/` | 200 | None |
| Programs list | `/programs/` | 200 | 2 issue(s) |
| Notes redirect | `/notes/client/1/` | 200 | None |

### Admin

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Client detail without program role (403) | `/clients/1/` | 403 | None |
| Admin settings dashboard | `/admin/settings/` | 200 | 1 issue(s) |
| Terminology settings | `/admin/settings/terminology/` | 200 | 2 issue(s) |
| Feature toggles | `/admin/settings/features/` | 200 | 2 issue(s) |
| Instance settings | `/admin/settings/instance/` | 200 | 1 issue(s) |
| Metrics library | `/plans/admin/metrics/` | 200 | None |
| Create metric form | `/plans/admin/metrics/create/` | 200 | 1 issue(s) |
| Programs list | `/programs/` | 200 | 2 issue(s) |
| Create program form | `/programs/create/` | 200 | 1 issue(s) |
| Program detail | `/programs/1/` | 200 | 1 issue(s) |
| User list | `/admin/users/` | 200 | 2 issue(s) |
| Create user form | `/admin/users/new/` | 200 | 1 issue(s) |
| Invite list | `/auth/invites/` | 200 | 2 issue(s) |
| Create invite form | `/auth/invites/new/` | 200 | 1 issue(s) |
| Audit log | `/admin/audit/` | 200 | 1 issue(s) |
| Registration links | `/admin/registration/` | 200 | 1 issue(s) |
| Create registration link | `/admin/registration/create/` | 200 | 1 issue(s) |
| Custom field admin | `/clients/admin/fields/` | 200 | 3 issue(s) |
| Create field group | `/clients/admin/fields/groups/create/` | 200 | 1 issue(s) |
| Create field definition | `/clients/admin/fields/create/` | 200 | 1 issue(s) |
| Event types list | `/events/admin/types/` | 200 | 2 issue(s) |
| Create event type | `/events/admin/types/create/` | 200 | 1 issue(s) |
| Note templates | `/admin/settings/note-templates/` | 200 | 3 issue(s) |
| Client data export form | `/reports/client-data-export/` | 200 | 1 issue(s) |
| Export links management | `/reports/export-links/` | 200 | 1 issue(s) |
| Diagnose charts | `/admin/settings/diagnose-charts/` | 200 | 3 issue(s) |
| Pending submissions | `/admin/submissions/` | 200 | 1 issue(s) |

### Non-admin spot check

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Admin settings (403) | `/admin/settings/` | 403 | None |
| User list (403) | `/admin/users/` | 403 | None |

### Admin+PM

| Step | URL | Status | Issues |
|------|-----|--------|--------|
| Client detail | `/clients/1/` | 200 | 1 issue(s) |
| Notes timeline | `/notes/client/1/` | 200 | 1 issue(s) |
| Plan view | `/plans/client/1/` | 200 | 1 issue(s) |
| Admin settings | `/admin/settings/` | 200 | 1 issue(s) |
| User list | `/admin/users/` | 200 | 2 issue(s) |

## Recommendations

### Immediate (Critical)

1. Fix: Server error (500) on HTMX partial on `/plans/targets/1/metrics/`

### Short-term (Warnings)

- **Heading structure:** 49 pages with heading issues.
- Page has no <h1> element (`/clients/1/`)
- Page has no <title> or title is empty (`/clients/search/?q=Jane`)
- No <main> landmark element found (`/clients/search/?q=Jane`)
- No <nav> element found on full page (`/clients/search/?q=Jane`)
- No <html> element found (`/clients/search/?q=Jane`)
- Page has no <h1> element (`/clients/1/`)
- 403 page has very little content — may not be helpful (`/plans/client/1/sections/create/`)
- 403 page has no links — user may be stuck (`/plans/client/1/sections/create/`)
- Expected form errors but none found (no .errorlist elements) (`/notes/client/1/quick/`)
- Page has no <h1> element (`/clients/create/`)
- Page has no <h1> element (`/clients/1/`)
- Page has no <h1> element (`/clients/1/edit/`)
- Page has no <h1> element (`/clients/1/consent/`)
- Page has no <h1> element (`/notes/client/1/quick/`)
- Page has no <h1> element (`/notes/client/1/`)
- Page has no <h1> element (`/plans/client/1/`)
- 403 page has very little content — may not be helpful (`/plans/client/1/sections/create/`)
- 403 page has no links — user may be stuck (`/plans/client/1/sections/create/`)
- Page has no <h1> element (`/events/client/1/`)
- Page has no <h1> element (`/reports/client/1/analysis/`)
- Page has no <h1> element (`/clients/1/`)
- Page has no <h1> element (`/notes/client/1/`)
- Page has no <h1> element (`/plans/client/1/`)
- Page has no <h1> element (`/plans/client/1/sections/create/`)
- Page has no <h1> element (`/plans/client/1/sections/create/`)
- Page has no <h1> element (`/plans/sections/1/targets/create/`)
- Page has no <h1> element (`/events/client/1/`)
- Page has no <h1> element (`/reports/client/1/analysis/`)
- Page has no <h1> element (`/admin/settings/diagnose-charts/`)
- Page has no <h1> element (`/clients/1/`)
- Page has no <h1> element (`/notes/client/1/`)
- Page has no <h1> element (`/plans/client/1/`)

---

_Generated by `tests/ux_walkthrough/` — automated UX walkthrough_
