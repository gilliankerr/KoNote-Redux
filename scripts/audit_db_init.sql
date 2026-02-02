-- Audit database initialisation
-- Restrict the app user to INSERT-only on the audit_log table.
-- This makes the audit trail tamper-resistant from the application layer.

-- After Django migrations create the audit_log table, run:
-- REVOKE UPDATE, DELETE ON audit_log FROM audit_writer;

-- For now, the audit_writer role is created by Docker Compose.
-- The REVOKE commands should be run after the first migration.
-- A post-migration script handles this automatically.

-- Create a read-only role for the admin audit viewer
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'audit_reader') THEN
        CREATE ROLE audit_reader WITH LOGIN PASSWORD 'audit_read_pass';
    END IF;
END
$$;
