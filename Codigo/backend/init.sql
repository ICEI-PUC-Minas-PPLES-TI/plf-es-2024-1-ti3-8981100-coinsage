--
-- PostgreSQL database dump
--

-- Dumped from database version 13.14 (Debian 13.14-1.pgdg120+2)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)

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
-- Name analysis; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.analysis (
    uuid uuid NOT NULL,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    date timestamp without time zone,
    ended boolean
);

ALTER TABLE public.analysis OWNER TO coinsage;

--
-- Name: analysis_currency_stage_four; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.analysis_currency_stage_four (
    uuid uuid NOT NULL,
    uuid_analysis uuid,
    uuid_currency uuid,
    mon_semester_variation_per numeric(15,8),
    mon_quarter_variation_per numeric(15,8),
    mon_mon_variation_per numeric(15,8),
    mon_week_variation_per numeric(15,8),
    variation_consistent boolean,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);


ALTER TABLE public.analysis_currency_stage_four OWNER TO coinsage;

--
-- Name: analysis_currency_stage_one; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.analysis_currency_stage_one (
    uuid uuid NOT NULL,
    uuid_analysis uuid,
    uuid_currency uuid,
    ranking integer,
    week_increase_percentage numeric(15,8),
    increase_date timestamp without time zone,
    closing_price numeric(15,8),
    last_week_closing_price numeric(15,8),
    open_price numeric(15,8),
    ema8 numeric(15,8),
    ema8_greater_open boolean,
    ema8_less_close boolean,
    week_increase_volume numeric(15,8),
    increase_volume_day timestamp without time zone,
    volumes_relation numeric(15,8),
    expressive_volume_increase boolean,
    ema_aligned boolean,
    buying_signal boolean,
    today timestamp without time zone,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    market_cap numeric(24,4),
    increase_volume numeric(18,8),
    today_volume numeric(18,8),
    volume_before_increase numeric(18,8),
    current_price numeric(15,8)
);


ALTER TABLE public.analysis_currency_stage_one OWNER TO coinsage;

--
-- Name: analysis_currency_stage_three; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.analysis_currency_stage_three (
    uuid uuid NOT NULL,
    uuid_analysis uuid,
    uuid_currency uuid,
    year_mon_variation numeric(15,8),
    semester_mon_variation numeric(15,8),
    quarter_mon_variation numeric(15,8),
    month_week_variation numeric(15,8),
    week_mon_variation numeric(15,8),
    variation_consistent boolean,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);


ALTER TABLE public.analysis_currency_stage_three OWNER TO coinsage;

--
-- Name: analysis_currency_stage_two; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.analysis_currency_stage_two (
    uuid uuid NOT NULL,
    uuid_analysis uuid,
    uuid_currency uuid,
    year_variation_per numeric(15,8),
    semester_variation_per numeric(15,8),
    quarter_variation_per numeric(15,8),
    month_variation_per numeric(15,8),
    week_variation_per numeric(15,8),
    variation_greater_bitcoin boolean,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);


ALTER TABLE public.analysis_currency_stage_two OWNER TO coinsage;

--
-- Name: analysis_info_schedule; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.analysis_info_schedule (
    id integer NOT NULL,
    last_update_time timestamp without time zone,
    next_scheduled_time timestamp without time zone NOT NULL,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    uuid_analysis uuid
);


ALTER TABLE public.analysis_info_schedule OWNER TO coinsage;

--
-- Name: analysis_info_schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: coinsage
--

CREATE SEQUENCE public.analysis_info_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.analysis_info_schedule_id_seq OWNER TO coinsage;

--
-- Name: analysis_info_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: coinsage
--

ALTER SEQUENCE public.analysis_info_schedule_id_seq OWNED BY public.analysis_info_schedule.id;


--
-- Name: currencies_info_schedule; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.currencies_info_schedule (
    id integer NOT NULL,
    last_update_time timestamp without time zone,
    next_scheduled_time timestamp without time zone NOT NULL,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);


ALTER TABLE public.currencies_info_schedule OWNER TO coinsage;

--
-- Name: currencies_info_schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: coinsage
--

CREATE SEQUENCE public.currencies_info_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.currencies_info_schedule_id_seq OWNER TO coinsage;

--
-- Name: currencies_info_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: coinsage
--

ALTER SEQUENCE public.currencies_info_schedule_id_seq OWNED BY public.currencies_info_schedule.id;


--
-- Name: currency_base_info; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.currency_base_info (
    uuid uuid NOT NULL,
    symbol character varying(100),
    cmc_id integer,
    cmc_slug character varying(100),
    logo character varying(1000),
    name character varying(100),
    description character varying(5000),
    _technical_doc text,
    _urls text,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);


ALTER TABLE public.currency_base_info OWNER TO coinsage;

--
-- Name: setor; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.setor (
    uuid uuid NOT NULL,
    name character varying(500),
    title character varying(500),
    coins_quantity integer,
    cmc_id character varying(200),
    active boolean,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);


ALTER TABLE public.setor OWNER TO coinsage;

--
-- Name: setor_currency_base_info; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.setor_currency_base_info (
    uuid uuid NOT NULL,
    uuid_setor uuid,
    uuid_currency uuid,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);


ALTER TABLE public.setor_currency_base_info OWNER TO coinsage;

--
-- Name: wallet_transaction; Type: TABLE; Schema: public; Owner: coinsage
--

CREATE TABLE public.wallet_transaction (
    uuid uuid NOT NULL,
    quantity numeric(20,8),
    amount numeric(20,8),
    date timestamp without time zone NOT NULL,
    price_on_purchase numeric(15,8) NOT NULL,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    uuid_currency uuid
);


ALTER TABLE public.wallet_transaction OWNER TO coinsage;

--
-- Name: analysis_info_schedule id; Type: DEFAULT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_info_schedule ALTER COLUMN id SET DEFAULT nextval('public.analysis_info_schedule_id_seq'::regclass);


--
-- Name: currencies_info_schedule id; Type: DEFAULT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.currencies_info_schedule ALTER COLUMN id SET DEFAULT nextval('public.currencies_info_schedule_id_seq'::regclass);

--
-- Name: analysis; Type: DEFAULT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis
    ADD CONSTRAINT analysis_pkey PRIMARY KEY (uuid);

--
-- Name: analysis_currency_stage_four analysis_currency_stage_four_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_four
    ADD CONSTRAINT analysis_currency_stage_four_pkey PRIMARY KEY (uuid);


--
-- Name: analysis_currency_stage_one analysis_currency_stage_one_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_one
    ADD CONSTRAINT analysis_currency_stage_one_pkey PRIMARY KEY (uuid);


--
-- Name: analysis_currency_stage_three analysis_currency_stage_three_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_three
    ADD CONSTRAINT analysis_currency_stage_three_pkey PRIMARY KEY (uuid);


--
-- Name: analysis_currency_stage_two analysis_currency_stage_two_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_two
    ADD CONSTRAINT analysis_currency_stage_two_pkey PRIMARY KEY (uuid);


--
-- Name: analysis_info_schedule analysis_info_schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_info_schedule
    ADD CONSTRAINT analysis_info_schedule_pkey PRIMARY KEY (id);


--
-- Name: currencies_info_schedule currencies_info_schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.currencies_info_schedule
    ADD CONSTRAINT currencies_info_schedule_pkey PRIMARY KEY (id);


--
-- Name: currency_base_info currency_base_info_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.currency_base_info
    ADD CONSTRAINT currency_base_info_pkey PRIMARY KEY (uuid);


--
-- Name: currency_base_info currency_base_info_symbol_key; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.currency_base_info
    ADD CONSTRAINT currency_base_info_symbol_key UNIQUE (symbol);


--
-- Name: setor_currency_base_info setor_currency_base_info_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.setor_currency_base_info
    ADD CONSTRAINT setor_currency_base_info_pkey PRIMARY KEY (uuid);


--
-- Name: setor setor_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.setor
    ADD CONSTRAINT setor_pkey PRIMARY KEY (uuid);


--
-- Name: wallet_transaction wallet_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.wallet_transaction
    ADD CONSTRAINT wallet_transaction_pkey PRIMARY KEY (uuid);


--
-- Name: ix_analysis_info_schedule_id; Type: INDEX; Schema: public; Owner: coinsage
--

CREATE INDEX ix_analysis_info_schedule_id ON public.analysis_info_schedule USING btree (id);


--
-- Name: ix_currencies_info_schedule_id; Type: INDEX; Schema: public; Owner: coinsage
--

CREATE INDEX ix_currencies_info_schedule_id ON public.currencies_info_schedule USING btree (id);


--
-- Name: analysis_currency_stage_four analysis_currency_stage_four_uuid_analysis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_four
    ADD CONSTRAINT analysis_currency_stage_four_uuid_analysis_fkey FOREIGN KEY (uuid_analysis) REFERENCES public.analysis(uuid);


--
-- Name: analysis_currency_stage_four analysis_currency_stage_four_uuid_currency_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_four
    ADD CONSTRAINT analysis_currency_stage_four_uuid_currency_fkey FOREIGN KEY (uuid_currency) REFERENCES public.currency_base_info(uuid);


--
-- Name: analysis_currency_stage_one analysis_currency_stage_one_uuid_analysis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_one
    ADD CONSTRAINT analysis_currency_stage_one_uuid_analysis_fkey FOREIGN KEY (uuid_analysis) REFERENCES public.analysis(uuid);


--
-- Name: analysis_currency_stage_one analysis_currency_stage_one_uuid_currency_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_one
    ADD CONSTRAINT analysis_currency_stage_one_uuid_currency_fkey FOREIGN KEY (uuid_currency) REFERENCES public.currency_base_info(uuid);


--
-- Name: analysis_currency_stage_three analysis_currency_stage_three_uuid_analysis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_three
    ADD CONSTRAINT analysis_currency_stage_three_uuid_analysis_fkey FOREIGN KEY (uuid_analysis) REFERENCES public.analysis(uuid);


--
-- Name: analysis_currency_stage_three analysis_currency_stage_three_uuid_currency_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_three
    ADD CONSTRAINT analysis_currency_stage_three_uuid_currency_fkey FOREIGN KEY (uuid_currency) REFERENCES public.currency_base_info(uuid);


--
-- Name: analysis_currency_stage_two analysis_currency_stage_two_uuid_analysis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_two
    ADD CONSTRAINT analysis_currency_stage_two_uuid_analysis_fkey FOREIGN KEY (uuid_analysis) REFERENCES public.analysis(uuid);


--
-- Name: analysis_currency_stage_two analysis_currency_stage_two_uuid_currency_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_currency_stage_two
    ADD CONSTRAINT analysis_currency_stage_two_uuid_currency_fkey FOREIGN KEY (uuid_currency) REFERENCES public.currency_base_info(uuid);


--
-- Name: analysis_info_schedule analysis_info_schedule_uuid_analysis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.analysis_info_schedule
    ADD CONSTRAINT analysis_info_schedule_uuid_analysis_fkey FOREIGN KEY (uuid_analysis) REFERENCES public.analysis(uuid);


--
-- Name: setor_currency_base_info setor_currency_base_info_uuid_currency_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.setor_currency_base_info
    ADD CONSTRAINT setor_currency_base_info_uuid_currency_fkey FOREIGN KEY (uuid_currency) REFERENCES public.currency_base_info(uuid);


--
-- Name: setor_currency_base_info setor_currency_base_info_uuid_setor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.setor_currency_base_info
    ADD CONSTRAINT setor_currency_base_info_uuid_setor_fkey FOREIGN KEY (uuid_setor) REFERENCES public.setor(uuid);


--
-- Name: wallet_transaction wallet_transaction_uuid_currency_fkey; Type: FK CONSTRAINT; Schema: public; Owner: coinsage
--

ALTER TABLE ONLY public.wallet_transaction
    ADD CONSTRAINT wallet_transaction_uuid_currency_fkey FOREIGN KEY (uuid_currency) REFERENCES public.currency_base_info(uuid);


--
-- PostgreSQL database dump complete
--
