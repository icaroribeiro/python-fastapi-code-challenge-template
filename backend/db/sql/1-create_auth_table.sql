DROP TABLE IF EXISTS "auth";

CREATE TABLE IF NOT EXISTS auth (
    id uuid NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    login_id uuid NULL,
    refresh_token_id uuid NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    CONSTRAINT auth_pkey PRIMARY KEY (id),
    CONSTRAINT auth_username_key UNIQUE (username)
);

CREATE INDEX idx_auth_username ON auth (username);
