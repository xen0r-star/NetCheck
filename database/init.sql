--
-- PostgreSQL database dump
--

\restrict HHDkjdeZOU5XCCprdSuyHbA1rcObpUEI7hSvfsKsvLlb1nCFRkAe9sEvONPiK5e

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    hashpassword text NOT NULL,
    role character varying(20) DEFAULT 'user'::character varying NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users (id, username, hashpassword, role) VALUES (1, 'Jacky', '$2b$13$AcnWmh014VNHVQxSQRAN3uLPx.RlOr0yTikFeTypJaWp3q6ZbTNse', 'member');
INSERT INTO public.users (id, username, hashpassword, role) VALUES (2, 'Jojo', '$2b$13$x.ibgBxbdPTx4Zo09tx8huwBQGLuE1g2EU78tqEUPIvhlUlDuNmEe', 'member');
INSERT INTO public.users (id, username, hashpassword, role) VALUES (3, 'Didier', '$2b$13$ihfEB1dhEzXPdmnIxteJveeYMRolPGfVUHQUg1PtehcvHzGzvd5BC', 'member');
INSERT INTO public.users (id, username, hashpassword, role) VALUES (4, 'Michel', '$2b$13$trTxHQq36FhR7CTS.dm7B.yol3qgZ51kXN1tDOlkB4a6bWc.i6fOK', 'admin');


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- PostgreSQL database dump complete
--

\unrestrict HHDkjdeZOU5XCCprdSuyHbA1rcObpUEI7hSvfsKsvLlb1nCFRkAe9sEvONPiK5e

