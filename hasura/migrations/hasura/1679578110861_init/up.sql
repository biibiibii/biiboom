SET check_function_bodies = false;
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;
COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';
CREATE TABLE public.match_rule (
    id character varying NOT NULL,
    container character varying NOT NULL,
    title character varying NOT NULL,
    url character varying NOT NULL,
    "desc" character varying,
    _created_at timestamp with time zone DEFAULT now() NOT NULL,
    _updated_at timestamp with time zone,
    extra jsonb,
    note character varying,
    rule_type character varying,
    posted_at character varying
);
COMMENT ON TABLE public.match_rule IS 'xpath/json/xml rule';
COMMENT ON COLUMN public.match_rule.id IS 'create from hash: container title url desc extra rule_type';
CREATE SEQUENCE public.match_rule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.match_rule_id_seq OWNED BY public.match_rule.id;
CREATE TABLE public.node (
    id character varying NOT NULL,
    title character varying,
    url character varying NOT NULL,
    _updated_at timestamp with time zone DEFAULT now(),
    _created_at timestamp with time zone,
    extra json,
    site_id character varying NOT NULL,
    "desc" character varying,
    posted_at timestamp with time zone
);
COMMENT ON COLUMN public.node.id IS 'create from hash: site_id url';
CREATE SEQUENCE public.node_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.node_id_seq OWNED BY public.node.id;
CREATE TABLE public.site (
    id character varying NOT NULL,
    url character varying NOT NULL,
    jump_base_url character varying NOT NULL,
    _created_at timestamp with time zone DEFAULT now() NOT NULL,
    _updated_at timestamp with time zone,
    rule_id character varying NOT NULL,
    name character varying,
    language character varying,
    tags jsonb,
    sub_name character varying,
    update_rate integer DEFAULT 3600,
    next_update_time integer DEFAULT 0,
    original_url character varying
);
COMMENT ON COLUMN public.site.id IS 'create from hash: url';
ALTER TABLE ONLY public.match_rule
    ADD CONSTRAINT match_rule_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.node
    ADD CONSTRAINT node_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.site
    ADD CONSTRAINT site_1_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.node
    ADD CONSTRAINT node_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.site(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.site
    ADD CONSTRAINT site_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES public.match_rule(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
