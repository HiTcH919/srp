-- SQL Schema for Service Management System
-- This schema is designed for a relational database like PostgreSQL or SQLite.
-- For SQLite, AUTOINCREMENT is implicit for INTEGER PRIMARY KEY.
-- For PostgreSQL, use SERIAL or BIGSERIAL for auto-incrementing primary keys.

-- ============================================================================
-- Core Application Tables
-- ============================================================================

-- Users Table: Stores user accounts for the system.
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- Service Order Management Tables
-- ============================================================================

-- ServiceOrders Table: Main table for service order details.
DROP TABLE IF EXISTS service_orders;
CREATE TABLE service_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_name TEXT NOT NULL,
    service_date DATE,
    service_time TIME,
    sector TEXT, -- e.g., شرق, وسط, غرب, خارج المحافظة
    police_station_department TEXT,
    general_notes TEXT,
    created_by_user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Consider a trigger to update this
    status TEXT DEFAULT 'Draft', -- e.g., Draft, Active, Completed, Cancelled
    FOREIGN KEY (created_by_user_id) REFERENCES users (id)
);

-- Officers Table: Stores information about officers associated with a service order.
DROP TABLE IF EXISTS officers;
CREATE TABLE officers (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    officer_type TEXT, -- e.g., general_supervisor (مشرف عام), system_supervisor (مشرف منظومة), detective_supervisor (مشرف مباحث)
    rank TEXT,
    name TEXT,
    phone TEXT,
    unit TEXT, -- (القسم / الوحده)
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- SecurityForcesGroups Table: Details of security forces groups for a service order.
DROP TABLE IF EXISTS security_forces_groups;
CREATE TABLE security_forces_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    force_type TEXT, -- e.g., central (مركزي), security_forces (قوات أمن)
    group_leader_type TEXT, -- e.g., officer (ضابط), individual (فرد)
    group_leader_rank TEXT,
    group_leader_name TEXT,
    group_leader_phone TEXT,
    group_count INTEGER,
    vehicle_type TEXT,
    vehicle_number TEXT,
    vehicle_driver_rank TEXT,
    vehicle_driver_name TEXT,
    vehicle_driver_phone TEXT,
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- FemaleStaffMembers Table: Female staff members assigned to a service order.
DROP TABLE IF EXISTS female_staff_members;
CREATE TABLE female_staff_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    is_officer_in_charge BOOLEAN DEFAULT FALSE, -- مسئولة المأمورية
    rank TEXT,
    name TEXT,
    phone TEXT,
    specialization TEXT, -- (التخصص) for officer_in_charge
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- Vehicles Table: Vehicles used in a service order.
DROP TABLE IF EXISTS vehicles;
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    vehicle_category TEXT, -- e.g., emergency_car (سيارة النجدة), other_vehicle (مركبات أخرى)
    -- Fields for 'emergency_car'
    chief_type TEXT, -- (ضابط / فرد) (Officer / Individual) for emergency_car
    chief_rank TEXT,
    chief_name TEXT,
    chief_phone TEXT,
    driver_license_number TEXT, -- for emergency_car driver
    -- Fields for 'other_vehicle'
    capacity_load TEXT, -- (الحمولة / السعة) for other_vehicle
    purpose TEXT, -- (الغرض من الاستخدام) for other_vehicle
    -- Common fields
    vehicle_number TEXT, -- رقم المركبة
    vehicle_type TEXT, -- نوع المركبة
    driver_rank TEXT, -- رتبة السائق
    driver_name TEXT, -- اسم السائق
    driver_phone TEXT, -- هاتف السائق
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- ServiceOrderClauses Table: Specific clauses or instructions for a service order.
DROP TABLE IF EXISTS service_order_clauses;
CREATE TABLE service_order_clauses (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    clause_type TEXT, -- e.g., dispatch (بند القيام), delivery (بند التسليم), return (بند العودة)
    clause_number TEXT, -- رقم البند
    clause_document TEXT, -- مستند البند
    additional_details TEXT,
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- JurisdictionInfo Table: Information about the jurisdiction related to the service order.
DROP TABLE IF EXISTS jurisdiction_info;
CREATE TABLE jurisdiction_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    accompanying_entity TEXT, -- الجهة المصاحبة
    responsible_person_title TEXT, -- وظيفة المسئول
    responsible_person_name TEXT, -- اسم المسئول
    responsible_person_phone TEXT, -- هاتف المسئول
    responsible_person_email TEXT, -- بريد المسئول
    special_notes TEXT, -- ملاحظات خاصة
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- DeporteesAccused Table: Information about deportees or accused individuals in a service order.
DROP TABLE IF EXISTS deportees_accused;
CREATE TABLE deportees_accused (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    name TEXT,
    case_number TEXT, -- رقم القضية
    national_id TEXT, -- الرقم القومي
    charge TEXT, -- التهمة
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- Documents Table: Stores paths or references to uploaded documents related to service orders.
DROP TABLE IF EXISTS documents;
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    service_order_id INTEGER NOT NULL,
    file_name TEXT NOT NULL, -- Original file name
    file_path TEXT NOT NULL, -- Path to the stored file (e.g., in a specific upload directory)
    document_type TEXT, -- e.g., service_order_image, additional_document, clause_scan
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_order_id) REFERENCES service_orders (id) ON DELETE CASCADE
);

-- ============================================================================
-- Phonebook Table
-- ============================================================================

-- Contacts Table: For the general phonebook feature.
DROP TABLE IF EXISTS contacts;
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Or SERIAL PRIMARY KEY for PostgreSQL
    rank TEXT,
    name TEXT NOT NULL,
    primary_phone TEXT NOT NULL,
    secondary_phone TEXT,
    email TEXT,
    workplace TEXT, -- جهة العمل
    department TEXT, -- القسم / الإدارة
    position TEXT, -- المنصب
    category_officer BOOLEAN DEFAULT FALSE, -- ضابط
    category_security BOOLEAN DEFAULT FALSE, -- أفراد أمن
    category_driver BOOLEAN DEFAULT FALSE, -- سائقين
    category_female_staff BOOLEAN DEFAULT FALSE, -- عنصر نسائي
    category_favorite BOOLEAN DEFAULT FALSE, -- مفضل
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Consider a trigger to update this
);

-- ============================================================================
-- Indexes for Performance
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_service_orders_status ON service_orders (status);
CREATE INDEX IF NOT EXISTS idx_service_orders_service_date ON service_orders (service_date);
CREATE INDEX IF NOT EXISTS idx_service_orders_created_by_user_id ON service_orders (created_by_user_id);

CREATE INDEX IF NOT EXISTS idx_officers_service_order_id ON officers (service_order_id);
CREATE INDEX IF NOT EXISTS idx_security_forces_groups_service_order_id ON security_forces_groups (service_order_id);
CREATE INDEX IF NOT EXISTS idx_female_staff_members_service_order_id ON female_staff_members (service_order_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_service_order_id ON vehicles (service_order_id);
CREATE INDEX IF NOT EXISTS idx_service_order_clauses_service_order_id ON service_order_clauses (service_order_id);
CREATE INDEX IF NOT EXISTS idx_jurisdiction_info_service_order_id ON jurisdiction_info (service_order_id);
CREATE INDEX IF NOT EXISTS idx_deportees_accused_service_order_id ON deportees_accused (service_order_id);
CREATE INDEX IF NOT EXISTS idx_documents_service_order_id ON documents (service_order_id);

CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts (name);
CREATE INDEX IF NOT EXISTS idx_contacts_primary_phone ON contacts (primary_phone);
CREATE INDEX IF NOT EXISTS idx_contacts_workplace ON contacts (workplace);

-- ============================================================================
-- Triggers (Example for PostgreSQL to update 'updated_at' timestamps)
-- ============================================================================
-- CREATE OR REPLACE FUNCTION update_modified_column()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW.updated_at = now();
--     RETURN NEW;
-- END;
-- $$ language 'plpgsql';

-- CREATE TRIGGER update_service_orders_modtime
-- BEFORE UPDATE ON service_orders
-- FOR EACH ROW
-- EXECUTE FUNCTION update_modified_column();

-- CREATE TRIGGER update_contacts_modtime
-- BEFORE UPDATE ON contacts
-- FOR EACH ROW
-- EXECUTE FUNCTION update_modified_column();

-- For SQLite, updated_at timestamps are typically handled by the application logic upon update.
-- Alternatively, for newer SQLite versions (3.38.0+), you can use:
-- CREATE TRIGGER update_service_orders_updated_at AFTER UPDATE ON service_orders
-- BEGIN
--     UPDATE service_orders SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
-- END;
-- CREATE TRIGGER update_contacts_updated_at AFTER UPDATE ON contacts
-- BEGIN
--     UPDATE contacts SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
-- END;

PRAGMA foreign_keys=ON; -- Enforce foreign key constraints in SQLite
