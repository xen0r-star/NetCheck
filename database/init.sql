-- Database: PostgreSQL

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashpassword TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'membre' NOT NULL CHECK (role IN ('membre', 'admin')),
    is_temporary BOOLEAN DEFAULT false NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    failed_attempts INTEGER DEFAULT 0 NOT NULL,
    locked_until TIMESTAMP WITHOUT TIME ZONE,
    last_login TIMESTAMP WITHOUT TIME ZONE
);

INSERT INTO public.users (username, hashpassword, role, is_temporary, is_active, locked_until) VALUES 
    ('User1', '$2b$13$bHlfV9VzzlDnd67MQoJtFOnjus0tPTc24YLoZ8uCYRjmQuZLbjiCi', 'admin',  false,  true, NULL),
    ('User2', '$2b$13$bHlfV9VzzlDnd67MQoJtFOnjus0tPTc24YLoZ8uCYRjmQuZLbjiCi', 'membre', false,  true, NULL),
    ('User3', '$2b$13$bHlfV9VzzlDnd67MQoJtFOnjus0tPTc24YLoZ8uCYRjmQuZLbjiCi', 'membre', true,   true, NULL),
    ('User4', '$2b$13$bHlfV9VzzlDnd67MQoJtFOnjus0tPTc24YLoZ8uCYRjmQuZLbjiCi', 'membre', false,  true, '2026-12-31 23:59:59'),
    ('User5', '$2b$13$bHlfV9VzzlDnd67MQoJtFOnjus0tPTc24YLoZ8uCYRjmQuZLbjiCi', 'membre', false, false, NULL);
