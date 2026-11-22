-- schema.sql
-- Simply Renewable (Calgary, AB): residential solar & Canada Greener Homes energy proposals, equipment stock, and change requests.

CREATE TABLE IF NOT EXISTS proposals (
    proposal_id   TEXT PRIMARY KEY,
    client_name   TEXT NOT NULL,
    system_type   TEXT NOT NULL,
    status        TEXT NOT NULL CHECK (status IN ('site_survey','permitting','scheduled','installed')),
    install_date  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipment (
    item_name     TEXT PRIMARY KEY,
    category      TEXT NOT NULL,
    price         REAL NOT NULL CHECK (price >= 0),
    stock         INTEGER NOT NULL CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS change_requests (
    number        INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id   TEXT NOT NULL,
    new_value     TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'waiting' CHECK (status IN ('waiting','approved','rejected'))
);

INSERT OR IGNORE INTO proposals (proposal_id, client_name, system_type, status, install_date) VALUES
    ('SR201', 'Marc Bouchard', '9.4kW Rooftop Solar', 'site_survey', '2026-12-04'),
    ('SR202', 'Priya Nair', '11.2kW Rooftop Solar', 'permitting', '2026-12-14'),
    ('SR203', 'Greg Kowalski', '7.2kW Rooftop Solar', 'scheduled', '2026-12-02'),
    ('SR204', 'Rachelle Tremblay', '8.8kW Rooftop Solar', 'site_survey', '2026-12-17'),
    ('SR205', 'David Chen', '8.6kW Rooftop Solar', 'installed', '2026-11-12'),
    ('SR206', 'Tessa MacDonald', '10.0kW Rooftop Solar', 'scheduled', '2026-12-09');

INSERT OR IGNORE INTO equipment (item_name, category, price, stock) VALUES
    ('420W Bifacial Solar Panel', 'solar_panel', 265.00, 64),
    ('400W Monocrystalline Panel', 'solar_panel', 245.00, 50),
    ('Hybrid String Inverter 10kW', 'inverter', 2150.00, 0),
    ('IQ8 Microinverter', 'inverter', 175.00, 48),
    ('200A Main Breaker Upgrade', 'electrical', 2450.00, 3),
    ('Critter Guard Mesh Kit', 'protection', 320.00, 15);
    
