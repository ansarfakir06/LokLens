-- ============================================================================
-- LokLens Database Schema (schema.sql)
-- Tagline: A Lens Through Development
-- 
-- Relational schema designed for civic accountability & manifesto tracking.
-- Supports: Multiple Indian States, Administrations, Manifestos, and Sources.
-- ============================================================================

CREATE DATABASE IF NOT EXISTS loklens_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE loklens_db;

-- ----------------------------------------------------------------------------
-- 1. STATES TABLE
-- Stores supported Indian States and Union Territories.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS states (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    has_data BOOLEAN DEFAULT FALSE,
    unverified_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 2. ADMINISTRATIONS TABLE
-- Stores governing parties, election terms, and ruling administrations.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS administrations (
    id VARCHAR(50) PRIMARY KEY,
    state_id VARCHAR(50) NOT NULL,
    party_name VARCHAR(150) NOT NULL,
    term_years VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES states(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 3. MANIFESTOS TABLE
-- Stores party election manifesto documents linked to an administration.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS manifestos (
    id VARCHAR(50) PRIMARY KEY,
    administration_id VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    document_path VARCHAR(255),
    published_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (administration_id) REFERENCES administrations(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 4. PROMISES TABLE
-- Stores election manifesto promises, categorized with on-ground scheme details.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS promises (
    id VARCHAR(50) PRIMARY KEY,
    manifesto_id VARCHAR(50) NOT NULL,
    state_id VARCHAR(50) NOT NULL,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    category_label VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    status_label VARCHAR(100) NOT NULL,
    summary TEXT,
    manifesto_quote TEXT NOT NULL,
    implementation_details TEXT,
    target_metric VARCHAR(255),
    delivered_metric VARCHAR(255),
    metric_type VARCHAR(150),
    reporting_period VARCHAR(150),
    last_updated VARCHAR(100),
    data_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manifesto_id) REFERENCES manifestos(id) ON DELETE CASCADE,
    FOREIGN KEY (state_id) REFERENCES states(id) ON DELETE CASCADE,
    INDEX idx_state_category (state_id, category)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 5. SOURCES TABLE
-- Stores official primary documents, gazettes, and department orders.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sources (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    source_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 6. PROMISE_SOURCES (Many-to-Many Junction Table)
-- Connects promises to multiple documented official sources.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS promise_sources (
    promise_id VARCHAR(50) NOT NULL,
    source_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (promise_id, source_id),
    FOREIGN KEY (promise_id) REFERENCES promises(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
-- SEED DATA (Karnataka 2023 Manifestos & 5 Flagship Guarantees)
-- ============================================================================

-- 1. Seed States
INSERT INTO states (id, name, has_data, unverified_message) VALUES
('karnataka', 'Karnataka', TRUE, NULL),
('tamil-nadu', 'Tamil Nadu', FALSE, 'We have not yet compiled verified manifesto promises and government execution orders for Tamil Nadu. LokLens adheres to strict data verification rules and does not publish unverified or placeholder data.'),
('telangana', 'Telangana', FALSE, 'Manifesto data for Telangana is currently in the research pipeline. Official party manifestos and state government department budget reports are undergoing verification.'),
('andhra-pradesh', 'Andhra Pradesh', FALSE, 'Assembly election manifesto promises and implementation records for Andhra Pradesh are pending source compilation. Check back soon for verified records.'),
('maharashtra', 'Maharashtra', FALSE, 'Manifesto tracking records for Maharashtra are pending source documentation. We only publish records supported by downloadable official government gazettes.')
ON DUPLICATE KEY UPDATE name=VALUES(name), has_data=VALUES(has_data), unverified_message=VALUES(unverified_message);

-- 2. Seed Administration
INSERT INTO administrations (id, state_id, party_name, term_years) VALUES
('karnataka-inc-2023', 'karnataka', 'Indian National Congress (INC)', '2023–2028')
ON DUPLICATE KEY UPDATE party_name=VALUES(party_name), term_years=VALUES(term_years);

-- 3. Seed Manifesto
INSERT INTO manifestos (id, administration_id, title, subtitle, document_path, published_year) VALUES
('manifesto-ka-2023', 'karnataka-inc-2023', 'Karnataka Congress Assembly Election Manifesto 2023', '5 Flagship Guarantees — Verified against Official Departmental Orders', 'Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf', 2023)
ON DUPLICATE KEY UPDATE title=VALUES(title), subtitle=VALUES(subtitle), document_path=VALUES(document_path);

-- 4. Seed Sources
INSERT INTO sources (id, title, url, source_type) VALUES
('src-manifesto-2023', 'Karnataka Congress Assembly Election Manifesto 2023 (Official PDF)', 'Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf', 'Manifesto Document'),
('src-energy-go-2023', 'Energy Department Government Order (G.O. EN 22 PSR 2023)', 'https://karnataka.gov.in', 'Official Government Gazette'),
('src-wcd-portal-2023', 'Women & Child Development Department Scheme Guidelines', 'https://karnataka.gov.in', 'Department Portal'),
('src-food-supplies-2023', 'Food, Civil Supplies & Consumer Affairs Dept Orders', 'https://ahara.kar.nic.in', 'Department Order'),
('src-sevasindhu-2024', 'Skill Development, Entrepreneurship and Livelihood Dept Order', 'https://sevasindhuservices.karnataka.gov.in', 'Official Government Portal'),
('src-ksrtc-order-2023', 'Transport Department Notification & Corporation Guidelines', 'https://ksrtc.in', 'Transport Corporation Order')
ON DUPLICATE KEY UPDATE title=VALUES(title), url=VALUES(url), source_type=VALUES(source_type);

-- 5. Seed Promises (5 Karnataka Guarantees)
INSERT INTO promises (
    id, manifesto_id, state_id, name, category, category_label, status, status_label,
    summary, manifesto_quote, implementation_details, target_metric, delivered_metric,
    metric_type, reporting_period, last_updated, data_notes
) VALUES
(
    'gruha-jyothi', 'manifesto-ka-2023', 'karnataka', 'Gruha Jyothi', 'energy', '⚡ Energy',
    'delivered', 'Delivered / Active',
    '200 units of free electricity to all eligible domestic households.',
    '200 units of free electricity to all the houses.',
    'Provides up to 200 units of zero-cost electricity per month to eligible domestic households. The sanctioned quota is calculated based on each household''s past 12-month average consumption plus a 10% buffer.',
    'Up to 200 units / month per domestic account', 'Zero-bill benefit applied across all ESCOMs',
    'Electricity Consumption & Consumer Accounts', 'Ongoing (Launched August 2023)',
    'Official Karnataka Gazette (June 2023)',
    'Electricity schemes are measured in energy units (kWh) and beneficiary consumer accounts, not construction percentages. We do not invent percentage completion figures.'
),
(
    'gruha-lakshmi', 'manifesto-ka-2023', 'karnataka', 'Gruha Lakshmi', 'women', '👩 Women Welfare',
    'delivered', 'Delivered / Active',
    '₹2,000 monthly direct financial assistance to the woman head of every family.',
    '₹2,000 every month to each woman head of the family.',
    'Direct Benefit Transfer (DBT) of ₹2,000 deposited monthly into the bank account of the woman designated as head of household on Antyodaya, BPL, and APL ration cards. Excludes income-tax payees and GST filers.',
    '₹2,000 / month per eligible family', 'Monthly Direct Benefit Transfer (DBT)',
    'Direct Financial Transfer / Enrolled Women Heads', 'Monthly rounds (Launched August 2023)',
    'Dept of Women & Child Development (2024)',
    'Financial transfer schemes are measured in monthly disbursement cycles and verified bank accounts, not physical infrastructure milestones.'
),
(
    'anna-bhagya', 'manifesto-ka-2023', 'karnataka', 'Anna Bhagya', 'food', '🌾 Food Security',
    'adjusted', 'Partly Cash / Active',
    '10 kg of food grains per person per month for BPL families.',
    '10 Kgs of food grains to every person in BPL family.',
    'Targeted 10 kg free food grains per beneficiary. Due to initial interstate grain procurement constraints, the state delivers 5 kg physical rice plus cash compensation of ₹170 (₹34 per kg for the balance 5 kg) directly to the beneficiary''s bank account.',
    '10 kg food grains / person / month', '5 kg physical rice + ₹170 cash equivalent via DBT',
    'Food Grains (kg) & Cash Assistance (₹)', 'Ongoing monthly allocations (Launched July 2023)',
    'Food & Civil Supplies Department (2024)',
    'Status is transparently designated ''Partly Cash / Active'' because the government substituted 5 kg of grain with direct cash compensation due to supply constraints.'
),
(
    'yuvanidhi', 'manifesto-ka-2023', 'karnataka', 'Yuvanidhi', 'youth', '🎓 Youth & Jobs',
    'delivered', 'Delivered / Active',
    'Monthly unemployment stipend: ₹3,000 for degree graduates, ₹1,500 for diploma holders.',
    '₹3,000 per month for two years to unemployed graduates and ₹1,500 per month for two years to unemployed diploma holders.',
    'Direct financial allowance to unemployed graduates (₹3,000/mo) and diploma holders (₹1,500/mo) who graduated in 2022-2023 and remained unemployed 180 days after graduation. Paid for up to 24 months or until employment is found.',
    '₹3,000 (degree) / ₹1,500 (diploma) per month for 2 years', 'Monthly DBT allowance for verified applicants',
    'Direct Financial Support / Unemployed Youth', 'Monthly disbursements (Launched January 2024)',
    'Skill Development & Livelihood Dept (2024)',
    'Beneficiaries must submit periodic self-declarations on the Seva Sindhu portal confirming continued unemployment and non-enrollment in higher education.'
),
(
    'shakti', 'manifesto-ka-2023', 'karnataka', 'Shakti', 'transport', '🚌 Transport',
    'delivered', 'Delivered / Active',
    'Free zero-fare bus travel for women across state transport corporation buses.',
    'Free travel to all women throughout the state in regular KSRTC / BMTC buses.',
    'Zero-fare bus transit for women domiciled in Karnataka across state transport corporations (KSRTC, BMTC, NWKRTC, KKRTC) in non-luxury regular and express bus routes.',
    '100% free bus travel for women in ordinary state buses', 'Zero-fare tickets issued across 4 state RTC corporations',
    'Passenger Trips & Corporation Reimbursements', 'Continuous (Launched June 2023)',
    'Transport Department G.O. (June 2023)',
    'Bus transit progress is measured through zero-fare passenger trips logged and state treasury corporation reimbursements.'
)
ON DUPLICATE KEY UPDATE 
    name=VALUES(name), category=VALUES(category), status=VALUES(status),
    summary=VALUES(summary), manifesto_quote=VALUES(manifesto_quote),
    implementation_details=VALUES(implementation_details), target_metric=VALUES(target_metric),
    delivered_metric=VALUES(delivered_metric), data_notes=VALUES(data_notes);

-- 6. Link Promises to Sources
INSERT IGNORE INTO promise_sources (promise_id, source_id) VALUES
('gruha-jyothi', 'src-manifesto-2023'),
('gruha-jyothi', 'src-energy-go-2023'),
('gruha-lakshmi', 'src-manifesto-2023'),
('gruha-lakshmi', 'src-wcd-portal-2023'),
('anna-bhagya', 'src-manifesto-2023'),
('anna-bhagya', 'src-food-supplies-2023'),
('yuvanidhi', 'src-manifesto-2023'),
('yuvanidhi', 'src-sevasindhu-2024'),
('shakti', 'src-manifesto-2023'),
('shakti', 'src-ksrtc-order-2023');
