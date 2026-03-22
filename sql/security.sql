-- =========================
-- RBAC SETUP

-- Create roles
CREATE ROLE analyst;
CREATE ROLE app_user;


-- =========================
-- ANALYST ROLE (READ ONLY)

GRANT CONNECT ON DATABASE neondb TO analyst;

GRANT USAGE ON SCHEMA public TO analyst;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;


-- =========================
-- APP USER ROLE (READ + WRITE)

GRANT CONNECT ON DATABASE neondb TO app_user;

GRANT USAGE ON SCHEMA public TO app_user;

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_user;


-- =========================
-- FUTURE TABLES PERMISSIONS

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO analyst;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE ON TABLES TO app_user;