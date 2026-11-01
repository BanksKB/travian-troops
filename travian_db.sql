--
-- PostgreSQL database dump
--

\restrict emRcL9zR5R8EPMUk8w6cI19Wgk2aFdBquLQsTEkv1LObvp3RWxdpPKxPdQ7yhZh

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: plemena; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plemena (
    id_plemena integer NOT NULL,
    naziv character varying(50) NOT NULL,
    opis text
);


ALTER TABLE public.plemena OWNER TO postgres;

--
-- Name: plemena_id_plemena_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.plemena ALTER COLUMN id_plemena ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plemena_id_plemena_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: vojne_jedinice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vojne_jedinice (
    id_jedinice integer NOT NULL,
    id_plemena integer NOT NULL,
    naziv character varying(100) NOT NULL,
    napad integer NOT NULL,
    obrana_pjesadija integer NOT NULL,
    obrana_konjica integer NOT NULL,
    brzina integer NOT NULL,
    nosivost integer NOT NULL,
    drvo integer NOT NULL,
    glina integer NOT NULL,
    zeljezo integer NOT NULL,
    zito integer NOT NULL,
    potrosnja_zita integer NOT NULL,
    vrijeme_treniranja integer,
    tip_jedinice character varying(20) NOT NULL,
    CONSTRAINT chk_tip_jedinice CHECK (((tip_jedinice)::text = ANY ((ARRAY['Infantry'::character varying, 'Cavalry'::character varying])::text[])))
);


ALTER TABLE public.vojne_jedinice OWNER TO postgres;

--
-- Name: vojne_jedinice_id_jedinice_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.vojne_jedinice ALTER COLUMN id_jedinice ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.vojne_jedinice_id_jedinice_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: plemena; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.plemena (id_plemena, naziv, opis) FROM stdin;
1	Romans	Roman civilization with balanced military units.
2	Teutons	Germanic tribe specializing in aggressive infantry.
3	Gauls	Celtic tribe specializing in defense and cavalry.
4	Egyptians	Tribe with strong defensive capabilities.
5	Huns	Nomadic tribe specializing in fast cavalry.
\.


--
-- Data for Name: vojne_jedinice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vojne_jedinice (id_jedinice, id_plemena, naziv, napad, obrana_pjesadija, obrana_konjica, brzina, nosivost, drvo, glina, zeljezo, zito, potrosnja_zita, vrijeme_treniranja, tip_jedinice) FROM stdin;
1	1	Equites Imperatoris	120	65	50	14	100	550	440	320	100	3	2640	Cavalry
2	1	Legionnaire	40	35	50	6	50	120	100	150	30	1	1600	Infantry
3	2	Teutonic Knight	150	50	75	9	80	450	515	480	80	3	2960	Cavalry
4	2	Clubswinger	40	20	5	7	60	95	75	40	40	1	720	Infantry
5	3	Theutates Thunder	100	25	40	19	75	350	450	230	60	2	2480	Cavalry
6	3	Phalanx	15	40	50	7	35	100	130	55	30	1	1040	Infantry
7	4	Anhur Guard	50	110	50	15	50	360	330	280	120	2	2560	Cavalry
8	4	Slave Militia	10	30	20	7	15	45	60	30	15	1	530	Infantry
9	5	Steppe Rider	120	30	15	16	75	290	370	190	45	2	2400	Cavalry
10	5	Mercenary	35	40	30	6	50	130	80	40	40	1	810	Infantry
\.


--
-- Name: plemena_id_plemena_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.plemena_id_plemena_seq', 6, true);


--
-- Name: vojne_jedinice_id_jedinice_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vojne_jedinice_id_jedinice_seq', 10, true);


--
-- Name: plemena plemena_naziv_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plemena
    ADD CONSTRAINT plemena_naziv_key UNIQUE (naziv);


--
-- Name: plemena plemena_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plemena
    ADD CONSTRAINT plemena_pkey PRIMARY KEY (id_plemena);


--
-- Name: vojne_jedinice uq_jedinica_pleme; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vojne_jedinice
    ADD CONSTRAINT uq_jedinica_pleme UNIQUE (id_plemena, naziv);


--
-- Name: vojne_jedinice vojne_jedinice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vojne_jedinice
    ADD CONSTRAINT vojne_jedinice_pkey PRIMARY KEY (id_jedinice);


--
-- Name: vojne_jedinice fk_pleme; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vojne_jedinice
    ADD CONSTRAINT fk_pleme FOREIGN KEY (id_plemena) REFERENCES public.plemena(id_plemena);


--
-- PostgreSQL database dump complete
--

\unrestrict emRcL9zR5R8EPMUk8w6cI19Wgk2aFdBquLQsTEkv1LObvp3RWxdpPKxPdQ7yhZh

