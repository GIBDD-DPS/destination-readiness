-- Prizolov Lab / Destination Readiness / v0.1.0-draft
-- Автор: Dm.Andreyanov
-- Принцип: одна таблица на тип данных, не на "город" — сохраняет типизацию
-- и честные NULL/not_applicable вместо JSON-помойки.

-- ============ Справочники ============

CREATE TABLE destinations (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    population INTEGER,
    lat DECIMAL,
    lon DECIMAL
);

CREATE TABLE operators (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- ============ Ось 1 — Infrastructure Load ============

CREATE TABLE axis_infrastructure_load (
    destination_id UUID REFERENCES destinations(id),
    month DATE,
    tourist_count INTEGER,
    accommodation_occupancy DECIMAL,
    transit_strain DECIMAL,
    computed_score DECIMAL,
    data_snapshot_date DATE,
    source TEXT,
    PRIMARY KEY (destination_id, month)
);

-- ============ Ось 2 — Regulatory Risk ============

CREATE TABLE axis_regulatory_risk (
    destination_id UUID REFERENCES destinations(id),
    as_of_date DATE,
    active_restrictions_score DECIMAL,
    pending_legislation_score DECIMAL,
    historical_volatility_score DECIMAL,
    computed_score DECIMAL,
    reason_ru TEXT,
    reason_en TEXT,
    source_url TEXT,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id, as_of_date)
);

-- ============ Ось 3 — Wait Time ============

CREATE TABLE axis_wait_time (
    destination_id UUID REFERENCES destinations(id),
    venue_name TEXT,
    venue_type TEXT,
    peak_wait_minutes DECIMAL,
    acceptable_threshold_minutes DECIMAL,
    computed_score DECIMAL,
    is_applicable BOOLEAN DEFAULT TRUE,
    data_snapshot_date DATE,
    source TEXT,
    PRIMARY KEY (destination_id, venue_name)
);

-- ============ Ось 4 — Local Sentiment ============

CREATE TABLE axis_local_sentiment (
    destination_id UUID REFERENCES destinations(id),
    quarter DATE,
    protest_activity_score DECIMAL,
    media_tone_score DECIMAL,
    petition_signal_score DECIMAL,
    computed_score DECIMAL,
    reason_ru TEXT,
    reason_en TEXT,
    cited_articles JSONB,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id, quarter)
);

-- ============ Ось 5 — Price Volatility ============

CREATE TABLE axis_price_volatility (
    destination_id UUID REFERENCES destinations(id),
    month DATE,
    accommodation_volatility DECIMAL,
    flight_volatility DECIMAL,
    absolute_price_tier INTEGER,
    booking_window_sensitivity DECIMAL,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id, month)
);

-- ============ Ось 6 — Health & Safety ============

CREATE TABLE axis_health_safety (
    destination_id UUID REFERENCES destinations(id),
    month DATE,
    medical_access_gap DECIMAL,
    seasonal_disease_risk DECIMAL,
    insurance_mandate_flag BOOLEAN,
    computed_score DECIMAL,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id, month)
);

-- B2B-расширение
CREATE TABLE axis_duty_of_care (
    destination_id UUID REFERENCES destinations(id),
    accredited_hospitals JSONB,
    cashless_partner_coverage BOOLEAN,
    evacuation_time_hours DECIMAL,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id)
);

-- ============ Ось 7 — Payment Friction ============

CREATE TABLE axis_payment_friction (
    destination_id UUID REFERENCES destinations(id),
    card_acceptance_gap DECIMAL,
    atm_fee_burden DECIMAL,
    airport_exchange_markup DECIMAL,
    computed_score DECIMAL,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id)
);

-- ============ Ось 8 — Weather Risk ============

CREATE TABLE axis_weather_risk (
    destination_id UUID REFERENCES destinations(id),
    date DATE,
    extreme_event_probability DECIMAL,
    comfort_deviation DECIMAL,
    computed_score DECIMAL,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id, date)
);

-- ============ Ось 9 — Profile Barriers ============

CREATE TABLE axis_profile_barriers (
    destination_id UUID REFERENCES destinations(id),
    profile TEXT CHECK (profile IN ('solo', 'family', 'mobility')),
    barrier_name TEXT,
    severity TEXT,
    reason_ru TEXT,
    reason_en TEXT,
    source TEXT,
    data_snapshot_date DATE,
    PRIMARY KEY (destination_id, profile, barrier_name)
);

-- ============ Ось 10 — Supplier Reliability (B2B) ============

CREATE TABLE axis_supplier_reliability (
    operator_id UUID REFERENCES operators(id),
    destination_id UUID REFERENCES destinations(id),
    period_start DATE,
    period_end DATE,
    operational_cancellation_rate DECIMAL,
    staff_turnover_proxy DECIMAL,
    overbooking_incident_rate DECIMAL,
    computed_score DECIMAL,
    PRIMARY KEY (operator_id, destination_id, period_start)
);

CREATE TABLE operator_incident_log (
    id UUID PRIMARY KEY,
    operator_id UUID REFERENCES operators(id),
    destination_id UUID REFERENCES destinations(id),
    incident_date DATE,
    incident_type TEXT,
    severity TEXT
);

-- ============ Ось 11 — Group Capacity (B2B) ============

CREATE TABLE venue_bookings (
    venue_name TEXT,
    destination_id UUID REFERENCES destinations(id),
    date DATE,
    daily_capacity INTEGER,
    booked_count INTEGER,
    PRIMARY KEY (venue_name, date)
);

-- ============ Ось 12 — Labor Action Risk (B2B) ============

CREATE TABLE axis_labor_action_risk (
    destination_id UUID REFERENCES destinations(id),
    as_of_date DATE,
    historical_strike_frequency DECIMAL,
    active_dispute_signal DECIMAL,
    computed_score DECIMAL,
    reason_ru TEXT,
    reason_en TEXT,
    source_url TEXT,
    PRIMARY KEY (destination_id, as_of_date)
);

-- ============ Ось 13 — Currency Lock Risk (B2B) ============

CREATE TABLE axis_currency_lock_risk (
    sales_currency TEXT,
    cost_currency TEXT,
    as_of_date DATE,
    pair_volatility_annualized DECIMAL,
    avg_lag_days INTEGER,
    exposure_score DECIMAL,
    PRIMARY KEY (sales_currency, cost_currency, as_of_date)
);

-- ============ Trip Cost & Feasibility (персональный блок) ============

CREATE TABLE visa_requirements (
    nationality TEXT,
    destination_country TEXT,
    required BOOLEAN,
    cost DECIMAL,
    processing_days INTEGER,
    max_stay_days INTEGER,
    updated_at DATE,
    PRIMARY KEY (nationality, destination_country)
);

-- ============ i18n ============

CREATE TABLE axis_reasons_i18n (
    axis_reason_id UUID PRIMARY KEY,
    lang TEXT CHECK (lang IN ('ru', 'en')),
    description TEXT,
    reason TEXT
);

-- ============ Trust tier — для интерпретирующих осей ============

CREATE TABLE source_trust_state (
    source_id UUID PRIMARY KEY,
    axis TEXT CHECK (axis IN ('regulatory_risk', 'local_sentiment', 'labor_action_risk')),
    tier TEXT CHECK (tier IN ('learning', 'calibrating', 'trusted', 'autonomous')) DEFAULT 'learning',
    reviewed_count INTEGER DEFAULT 0,
    agreement_count INTEGER DEFAULT 0,
    rolling_agreement_rate DECIMAL,
    last_demoted_at DATE,
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE review_queue (
    id UUID PRIMARY KEY,
    source_id UUID REFERENCES source_trust_state(source_id),
    axis TEXT,
    extracted_text TEXT,
    source_url TEXT,
    classification TEXT,
    confidence DECIMAL,
    human_verdict TEXT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT now()
);

-- Prizolov Lab / Destination Readiness / v0.1.0-draft
