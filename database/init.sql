CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashpassword TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user' NOT NULL CHECK (role IN ('user', 'admin')),
    is_temporary BOOLEAN DEFAULT false NOT NULL,
    failed_attempts INTEGER DEFAULT 0 NOT NULL,
    locked_until TIMESTAMP WITHOUT TIME ZONE,
    last_login TIMESTAMP WITHOUT TIME ZONE
);

INSERT INTO public.users (username, hashpassword, role) VALUES 
    ('Jacky', '$2b$13$AcnWmh014VNHVQxSQRAN3uLPx.RlOr0yTikFeTypJaWp3q6ZbTNse', 'user'),
    ('Jojo', '$2b$13$x.ibgBxbdPTx4Zo09tx8huwBQGLuE1g2EU78tqEUPIvhlUlDuNmEe', 'user'),
    ('Didier', '$2b$13$ihfEB1dhEzXPdmnIxteJveeYMRolPGfVUHQUg1PtehcvHzGzvd5BC', 'user'),
    ('Michel', '$2b$13$trTxHQq36FhR7CTS.dm7B.yol3qgZ51kXN1tDOlkB4a6bWc.i6fOK', 'admin');

