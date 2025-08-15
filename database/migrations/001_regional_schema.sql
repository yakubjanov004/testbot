BEGIN;

-- ===== Shared types =====
DO $$ BEGIN
  CREATE TYPE user_role_enum AS ENUM (
    'admin','manager','junior_manager','controller','technician',
    'warehouse','call_center','call_center_supervisor','client','blocked'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE document_type_enum AS ENUM ('connection','technical_service','staff_created');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ===== Core =====
CREATE TABLE IF NOT EXISTS users (
  id            SERIAL PRIMARY KEY,
  telegram_id   BIGINT UNIQUE NOT NULL,
  full_name     TEXT,
  username      TEXT,
  phone         TEXT,
  role          user_role_enum NOT NULL DEFAULT 'client',
  abonent_id    VARCHAR(50),
  language      VARCHAR(2) NOT NULL DEFAULT 'uz' CHECK (language IN ('uz','ru')),
  is_active     BOOLEAN NOT NULL DEFAULT true,
  address       TEXT,
  permissions   JSONB NOT NULL DEFAULT '{}'::jsonb,
  last_activity TIMESTAMPTZ,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_role        ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_phone       ON users(phone);

CREATE TABLE IF NOT EXISTS role_permissions (
  id                     SERIAL PRIMARY KEY,
  role                   user_role_enum UNIQUE NOT NULL,
  application_types      JSONB NOT NULL DEFAULT '[]'::jsonb,
  workflow_actions       JSONB NOT NULL DEFAULT '[]'::jsonb,
  inbox_access           BOOLEAN NOT NULL DEFAULT true,
  client_search_access   BOOLEAN NOT NULL DEFAULT false,
  inventory_access       BOOLEAN NOT NULL DEFAULT false,
  reporting_access       BOOLEAN NOT NULL DEFAULT false,
  admin_functions        JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS system_settings (
  id            SERIAL PRIMARY KEY,
  setting_key   VARCHAR(100) UNIQUE NOT NULL,
  setting_value TEXT NOT NULL,
  description   TEXT,
  updated_by    INT REFERENCES users(id),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ===== Workflow =====
CREATE TABLE IF NOT EXISTS service_requests (
  id                      VARCHAR(36) PRIMARY KEY,
  workflow_type           VARCHAR(50) NOT NULL CHECK (workflow_type IN ('connection_request','technical_service','call_center_direct')),
  client_id               INT REFERENCES users(id),
  role_current            user_role_enum NOT NULL,
  current_status          VARCHAR(50) NOT NULL,
  priority                VARCHAR(20) NOT NULL DEFAULT 'medium' CHECK (priority IN ('low','medium','high','urgent')),
  description             TEXT,
  location                TEXT,
  contact_info            JSONB NOT NULL DEFAULT '{}'::jsonb,
  state_data              JSONB NOT NULL DEFAULT '{}'::jsonb,
  equipment_used          JSONB NOT NULL DEFAULT '[]'::jsonb,
  inventory_updated       BOOLEAN NOT NULL DEFAULT false,
  completion_rating       INT CHECK (completion_rating BETWEEN 1 AND 5),
  feedback_comments       TEXT,
  current_assignee_id     INT REFERENCES users(id),
  current_assignee_role   user_role_enum,
  created_by_staff        BOOLEAN NOT NULL DEFAULT false,
  staff_creator_id        INT REFERENCES users(id),
  staff_creator_role      user_role_enum,
  creation_source         VARCHAR(50) NOT NULL DEFAULT 'client',
  client_notified_at      TIMESTAMPTZ,
  diagnosis               TEXT,
  service_order_number    VARCHAR(50),
  accepted_by_fio         VARCHAR(255),
  approvers               JSONB NOT NULL DEFAULT '[]'::jsonb,
  installation_date       TIMESTAMPTZ,
  installed_by            INT REFERENCES users(id),
  diagnosis_date          TIMESTAMPTZ,
  diagnosed_by            INT REFERENCES users(id),
  rated_at                TIMESTAMPTZ,
  assigned_technician_id  INT REFERENCES users(id),
  ready_to_install        BOOLEAN NOT NULL DEFAULT false,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_sr_client_id           ON service_requests(client_id);
CREATE INDEX IF NOT EXISTS idx_sr_role_current        ON service_requests(role_current);
CREATE INDEX IF NOT EXISTS idx_sr_current_status      ON service_requests(current_status);
CREATE INDEX IF NOT EXISTS idx_sr_workflow_type       ON service_requests(workflow_type);
CREATE INDEX IF NOT EXISTS idx_sr_created_at          ON service_requests(created_at);
CREATE INDEX IF NOT EXISTS idx_sr_service_order       ON service_requests(service_order_number);
CREATE INDEX IF NOT EXISTS idx_sr_assigned_tech       ON service_requests(assigned_technician_id);

CREATE TABLE IF NOT EXISTS state_transitions (
  id              SERIAL PRIMARY KEY,
  request_id      VARCHAR(36) NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
  from_role       user_role_enum,
  to_role         user_role_enum NOT NULL,
  action          VARCHAR(100) NOT NULL,
  actor_id        INT REFERENCES users(id),
  transition_data JSONB NOT NULL DEFAULT '{}'::jsonb,
  comments        TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_st_request_id   ON state_transitions(request_id);
CREATE INDEX IF NOT EXISTS idx_st_to_role      ON state_transitions(to_role);
CREATE INDEX IF NOT EXISTS idx_st_created_at   ON state_transitions(created_at DESC);

CREATE TABLE IF NOT EXISTS workflow_tracking (
  id                SERIAL PRIMARY KEY,
  request_id        VARCHAR(50) NOT NULL REFERENCES service_requests(id),
  from_role         user_role_enum,
  to_role           user_role_enum NOT NULL,
  user_id           INT NOT NULL REFERENCES users(id),
  transition_time   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  duration_minutes  INT,
  efficiency_score  NUMERIC(5,2),
  notes             TEXT,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_wt_request_id       ON workflow_tracking(request_id);
CREATE INDEX IF NOT EXISTS idx_wt_user_id          ON workflow_tracking(user_id);
CREATE INDEX IF NOT EXISTS idx_wt_from_role        ON workflow_tracking(from_role);
CREATE INDEX IF NOT EXISTS idx_wt_to_role          ON workflow_tracking(to_role);
CREATE INDEX IF NOT EXISTS idx_wt_transition_time  ON workflow_tracking(transition_time);

CREATE TABLE IF NOT EXISTS role_statistics (
  id                     SERIAL PRIMARY KEY,
  role                   user_role_enum NOT NULL,
  period                 VARCHAR(20) NOT NULL,
  date                   DATE NOT NULL,
  total_requests         INT DEFAULT 0,
  completed_requests     INT DEFAULT 0,
  avg_completion_time    NUMERIC(10,2),
  avg_efficiency_score   NUMERIC(5,2),
  avg_quality_rating     NUMERIC(3,2),
  unique_users           INT DEFAULT 0,
  created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(role, period, date)
);
CREATE INDEX IF NOT EXISTS idx_rs_role    ON role_statistics(role);
CREATE INDEX IF NOT EXISTS idx_rs_period  ON role_statistics(period);
CREATE INDEX IF NOT EXISTS idx_rs_date    ON role_statistics(date);

-- ===== Inbox / Transfers =====
CREATE TABLE IF NOT EXISTS inbox_messages (
  id                   SERIAL PRIMARY KEY,
  application_id       VARCHAR(255) NOT NULL,
  application_type     VARCHAR(50) NOT NULL CHECK (application_type IN ('service_request')),
  assigned_role        user_role_enum NOT NULL,
  message_type         VARCHAR(50) NOT NULL DEFAULT 'application' CHECK (message_type IN ('application','transfer','notification','reminder')),
  title                VARCHAR(255),
  description          TEXT,
  priority             VARCHAR(20) NOT NULL DEFAULT 'medium' CHECK (priority IN ('low','medium','high','urgent')),
  is_read              BOOLEAN NOT NULL DEFAULT false,
  recipient_id         INT REFERENCES users(id),
  reply_markup_data    JSONB NOT NULL DEFAULT '{}'::jsonb,
  telegram_message_id  INT,
  reply_button_clicked BOOLEAN NOT NULL DEFAULT false,
  inbox_viewed         BOOLEAN NOT NULL DEFAULT false,
  completed            BOOLEAN NOT NULL DEFAULT false,
  seen_by_users        JSONB NOT NULL DEFAULT '[]'::jsonb,
  metadata             JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_im_role_read       ON inbox_messages(assigned_role, is_read);
CREATE INDEX IF NOT EXISTS idx_im_created_desc    ON inbox_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_im_app             ON inbox_messages(application_id, application_type);

CREATE TABLE IF NOT EXISTS application_transfers (
  id               SERIAL PRIMARY KEY,
  application_id   VARCHAR(255) NOT NULL,
  application_type VARCHAR(50) NOT NULL CHECK (application_type IN ('service_request')),
  from_role        user_role_enum,
  to_role          user_role_enum NOT NULL,
  transferred_by   INT NOT NULL REFERENCES users(id),
  transfer_reason  VARCHAR(255),
  transfer_notes   TEXT,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_at_app          ON application_transfers(application_id, application_type);
CREATE INDEX IF NOT EXISTS idx_at_from_role    ON application_transfers(from_role, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_at_to_role      ON application_transfers(to_role, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_at_by           ON application_transfers(transferred_by, created_at DESC);

-- ===== Time / Statistics =====
CREATE TABLE IF NOT EXISTS time_tracking (
  id               SERIAL PRIMARY KEY,
  request_id       VARCHAR(50) NOT NULL REFERENCES service_requests(id),
  user_id          INT NOT NULL REFERENCES users(id),
  role             user_role_enum NOT NULL,
  action_type      VARCHAR(100) NOT NULL,
  started_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ended_at         TIMESTAMPTZ,
  duration_minutes INT,
  workflow_stage   VARCHAR(100),
  efficiency_score NUMERIC(5,2),
  quality_rating   NUMERIC(3,2),
  notes            TEXT,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (request_id, user_id, action_type)
);
CREATE INDEX IF NOT EXISTS idx_tt_request_id  ON time_tracking(request_id);
CREATE INDEX IF NOT EXISTS idx_tt_user_id     ON time_tracking(user_id);
CREATE INDEX IF NOT EXISTS idx_tt_started_at  ON time_tracking(started_at);

CREATE TABLE IF NOT EXISTS realtime_time_tracking (
  id               SERIAL PRIMARY KEY,
  request_id       VARCHAR(50) NOT NULL,
  user_id          INT,
  role             user_role_enum,
  started_at       TIMESTAMPTZ,
  ended_at         TIMESTAMPTZ,
  duration_minutes INT,
  notes            TEXT,
  efficiency_score NUMERIC(5,2),
  quality_rating   NUMERIC(3,2),
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rtt_efficiency ON realtime_time_tracking(efficiency_score);
CREATE INDEX IF NOT EXISTS idx_rtt_quality    ON realtime_time_tracking(quality_rating);

CREATE TABLE IF NOT EXISTS employee_performance (
  id                   SERIAL PRIMARY KEY,
  user_id              INT NOT NULL REFERENCES users(id),
  date                 DATE NOT NULL,
  role                 user_role_enum NOT NULL,
  total_requests       INT DEFAULT 0,
  completed_requests   INT DEFAULT 0,
  total_time_minutes   INT DEFAULT 0,
  avg_time_per_request NUMERIC(10,2),
  efficiency_score     NUMERIC(5,2),
  quality_rating       NUMERIC(3,2),
  notes                TEXT,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, date)
);
CREATE INDEX IF NOT EXISTS idx_ep_user_date ON employee_performance(user_id, date);
CREATE INDEX IF NOT EXISTS idx_ep_role      ON employee_performance(role);

CREATE TABLE IF NOT EXISTS daily_statistics (
  id                              SERIAL PRIMARY KEY,
  date                            DATE UNIQUE NOT NULL,
  total_requests                  INT DEFAULT 0,
  completed_requests              INT DEFAULT 0,
  cancelled_requests              INT DEFAULT 0,
  pending_requests                INT DEFAULT 0,
  avg_completion_time_minutes     NUMERIC(10,2),
  total_work_hours                NUMERIC(10,2),
  total_employees_worked          INT DEFAULT 0,
  active_employees                INT DEFAULT 0,
  avg_rating                      NUMERIC(3,2),
  total_feedback                  INT DEFAULT 0,
  completion_rate                 NUMERIC(5,2),
  created_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at                      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ds_date ON daily_statistics(date);

CREATE TABLE IF NOT EXISTS excel_exports (
  id                 SERIAL PRIMARY KEY,
  user_id            INT NOT NULL REFERENCES users(id),
  export_type        VARCHAR(100) NOT NULL,
  date_range_start   DATE,
  date_range_end     DATE,
  file_name          VARCHAR(255),
  file_size_bytes    INT,
  file_hash          VARCHAR(64),
  download_count     INT NOT NULL DEFAULT 0,
  last_downloaded_at TIMESTAMPTZ,
  filters_applied    JSONB NOT NULL DEFAULT '{}'::jsonb,
  record_count       INT,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (date_range_start IS NULL OR date_range_end IS NULL OR date_range_start <= date_range_end)
);
CREATE INDEX IF NOT EXISTS idx_exports_user    ON excel_exports(user_id);
CREATE INDEX IF NOT EXISTS idx_exports_type    ON excel_exports(export_type);
CREATE INDEX IF NOT EXISTS idx_exports_range   ON excel_exports(date_range_start, date_range_end);

-- ===== Word documents =====
CREATE TABLE IF NOT EXISTS word_documents (
  id                    SERIAL PRIMARY KEY,
  request_id            VARCHAR(50) NOT NULL REFERENCES service_requests(id),
  document_type         document_type_enum NOT NULL,
  generated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  file_path             VARCHAR(500),
  document_data         JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_by            INT REFERENCES users(id),
  application_date      VARCHAR(20),
  technician_fio        VARCHAR(100),
  contract_number       VARCHAR(50),
  service_order_number  VARCHAR(50),
  organization_name     VARCHAR(200),
  accepted_by_fio       VARCHAR(100),
  diagnosis_result      TEXT,
  installed_equipment   JSONB,
  installation_address  TEXT,
  completion_date       VARCHAR(20),
  client_rating         INT,
  client_comment        TEXT,
  approvers             JSONB,
  service_type          VARCHAR(100),
  problem_description   TEXT,
  work_performed        TEXT,
  replaced_parts        JSONB,
  result                TEXT,
  operator_fio          VARCHAR(100),
  client_fio            VARCHAR(100),
  client_phone          VARCHAR(20),
  consultation_date     VARCHAR(20),
  UNIQUE (request_id, document_type)
);
CREATE INDEX IF NOT EXISTS idx_wd_request_id  ON word_documents(request_id);
CREATE INDEX IF NOT EXISTS idx_wd_doc_type    ON word_documents(document_type);
CREATE INDEX IF NOT EXISTS idx_wd_generated   ON word_documents(generated_at);

-- ===== Inventory / Warehouse =====
CREATE TABLE IF NOT EXISTS materials (
  id           SERIAL PRIMARY KEY,
  name         VARCHAR(255) NOT NULL,
  category     VARCHAR(100) NOT NULL DEFAULT 'general',
  quantity     INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
  unit         VARCHAR(20) NOT NULL DEFAULT 'pcs',
  min_quantity INT NOT NULL DEFAULT 5 CHECK (min_quantity >= 0),
  price        NUMERIC(10,2) NOT NULL DEFAULT 0,
  description  TEXT,
  supplier     VARCHAR(255),
  is_active    BOOLEAN NOT NULL DEFAULT true,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_mat_category ON materials(category);

CREATE TABLE IF NOT EXISTS material_receipts (
  id           SERIAL PRIMARY KEY,
  material_id  INT NOT NULL REFERENCES materials(id),
  quantity     INT NOT NULL CHECK (quantity > 0),
  received_by  INT NOT NULL REFERENCES users(id),
  supplier     TEXT,
  notes        TEXT,
  received_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS issued_items (
  id           SERIAL PRIMARY KEY,
  request_id   VARCHAR(36) REFERENCES service_requests(id),
  material_id  INT NOT NULL REFERENCES materials(id),
  quantity     INT NOT NULL CHECK (quantity > 0),
  issued_by    INT NOT NULL REFERENCES users(id),
  issued_to    INT REFERENCES users(id),
  issued_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ii_request  ON issued_items(request_id);
CREATE INDEX IF NOT EXISTS idx_ii_material ON issued_items(material_id);

CREATE TABLE IF NOT EXISTS inventory_transactions (
  id             SERIAL PRIMARY KEY,
  request_id     VARCHAR(50) REFERENCES service_requests(id),
  material_id    INT REFERENCES materials(id),
  change_type    VARCHAR(20) NOT NULL CHECK (change_type IN ('reserve','consume','return','in','out','adjustment')),
  quantity       INT NOT NULL,
  unit_price     NUMERIC(10,2),
  total_price    NUMERIC(12,2),
  performed_by   INT REFERENCES users(id),
  performed_role user_role_enum,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_it_request   ON inventory_transactions(request_id);
CREATE INDEX IF NOT EXISTS idx_it_material  ON inventory_transactions(material_id);
CREATE INDEX IF NOT EXISTS idx_it_created   ON inventory_transactions(created_at DESC);

CREATE TABLE IF NOT EXISTS equipment_requests (
  id            SERIAL PRIMARY KEY,
  technician_id INT NOT NULL REFERENCES users(id),
  equipment_type VARCHAR(100) NOT NULL,
  quantity      INT NOT NULL CHECK (quantity > 0),
  reason        TEXT NOT NULL,
  status        VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','issued','rejected')),
  approved_by   INT REFERENCES users(id),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS technician_locations (
  technician_id INT PRIMARY KEY REFERENCES users(id),
  latitude      NUMERIC(10,8) NOT NULL,
  longitude     NUMERIC(11,8) NOT NULL,
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS request_materials (
  id          SERIAL PRIMARY KEY,
  request_id  VARCHAR(36) NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
  material_id INT NOT NULL REFERENCES materials(id),
  quantity    INT NOT NULL CHECK (quantity > 0),
  unit        VARCHAR(20) NOT NULL DEFAULT 'pcs',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_rm_request  ON request_materials(request_id);
CREATE INDEX IF NOT EXISTS idx_rm_material ON request_materials(material_id);

-- ===== Chat / Call / Help =====
CREATE TABLE IF NOT EXISTS chat_sessions (
  id          SERIAL PRIMARY KEY,
  user_id     INT NOT NULL REFERENCES users(id),
  operator_id INT NOT NULL REFERENCES users(id),
  status      VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active','closed','transferred')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  closed_at   TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_cs_user     ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_cs_operator ON chat_sessions(operator_id);

CREATE TABLE IF NOT EXISTS chat_messages (
  id           SERIAL PRIMARY KEY,
  session_id   INT NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
  sender_id    INT NOT NULL REFERENCES users(id),
  message_text TEXT NOT NULL,
  message_type VARCHAR(20) NOT NULL DEFAULT 'text' CHECK (message_type IN ('text','image','document','location','contact','file')),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_cm_session  ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_cm_sender   ON chat_messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_cm_created  ON chat_messages(created_at);

CREATE TABLE IF NOT EXISTS call_logs (
  id            SERIAL PRIMARY KEY,
  user_id       INT REFERENCES users(id),
  phone_number  TEXT NOT NULL,
  duration      INT NOT NULL DEFAULT 0 CHECK (duration >= 0),
  result        VARCHAR(50) NOT NULL,
  notes         TEXT,
  created_by    INT REFERENCES users(id),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_cl_user     ON call_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_cl_created  ON call_logs(created_at);

CREATE TABLE IF NOT EXISTS help_requests (
  id            SERIAL PRIMARY KEY,
  technician_id INT NOT NULL REFERENCES users(id),
  help_type     VARCHAR(50) NOT NULL,
  description   TEXT NOT NULL,
  status        VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','assigned','in_progress','resolved','cancelled')),
  priority      VARCHAR(10) NOT NULL DEFAULT 'medium' CHECK (priority IN ('low','medium','high','urgent')),
  assigned_to   INT REFERENCES users(id),
  resolution    TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  resolved_at   TIMESTAMPTZ
);

-- ===== Audit / Analytics =====
CREATE TABLE IF NOT EXISTS audit_log (
  id             BIGSERIAL PRIMARY KEY,
  actor_user_id  INT NOT NULL REFERENCES users(id),
  actor_role     user_role_enum NOT NULL,
  action         VARCHAR(100) NOT NULL,
  entity_type    VARCHAR(50),
  entity_id      VARCHAR(100),
  request_id     VARCHAR(36) REFERENCES service_requests(id),
  target_user_id INT REFERENCES users(id),
  channel        VARCHAR(20),
  params         JSONB NOT NULL DEFAULT '{}'::jsonb,
  before_data    JSONB,
  after_data     JSONB,
  status         VARCHAR(20),
  error_message  TEXT,
  source_ip      INET,
  user_agent     TEXT,
  message_id     BIGINT,
  correlation_id UUID,
  session_id     VARCHAR(32),
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_audit_created   ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_actor     ON audit_log(actor_user_id);
CREATE INDEX IF NOT EXISTS idx_audit_action    ON audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_entity    ON audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_request   ON audit_log(request_id);
CREATE INDEX IF NOT EXISTS idx_audit_status    ON audit_log(status);

CREATE TABLE IF NOT EXISTS client_selection_data (
  id              SERIAL PRIMARY KEY,
  search_method   VARCHAR(20) NOT NULL CHECK (search_method IN ('phone','name','id','new')),
  search_value    VARCHAR(255),
  client_id       INT REFERENCES users(id),
  new_client_data JSONB NOT NULL DEFAULT '{}'::jsonb,
  verified        BOOLEAN NOT NULL DEFAULT false,
  created_by      INT NOT NULL,
  session_id      VARCHAR(32),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_csd_method   ON client_selection_data(search_method);
CREATE INDEX IF NOT EXISTS idx_csd_client   ON client_selection_data(client_id);
CREATE INDEX IF NOT EXISTS idx_csd_session  ON client_selection_data(session_id);

CREATE TABLE IF NOT EXISTS application_alerts (
  id               SERIAL PRIMARY KEY,
  alert_id         VARCHAR(255) UNIQUE NOT NULL,
  rule_id          VARCHAR(255) NOT NULL,
  alert_type       VARCHAR(100) NOT NULL,
  severity         VARCHAR(20) NOT NULL CHECK (severity IN ('info','warning','critical')),
  title            VARCHAR(500) NOT NULL,
  message          TEXT NOT NULL,
  data             JSONB NOT NULL DEFAULT '{}'::jsonb,
  channels         JSONB NOT NULL DEFAULT '[]'::jsonb,
  recipients       JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sent_at          TIMESTAMPTZ,
  delivery_status  JSONB NOT NULL DEFAULT '{}'::jsonb,
  acknowledged     BOOLEAN NOT NULL DEFAULT false,
  acknowledged_by  INT,
  acknowledged_at  TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_alerts_alert_id    ON application_alerts(alert_id);
CREATE INDEX IF NOT EXISTS idx_alerts_rule_id     ON application_alerts(rule_id);
CREATE INDEX IF NOT EXISTS idx_alerts_alert_type  ON application_alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_alerts_severity    ON application_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at  ON application_alerts(created_at);

CREATE TABLE IF NOT EXISTS alert_rules (
  id               SERIAL PRIMARY KEY,
  rule_id          VARCHAR(255) UNIQUE NOT NULL,
  name             VARCHAR(255) NOT NULL,
  description      TEXT,
  alert_type       VARCHAR(100) NOT NULL,
  threshold_config JSONB NOT NULL DEFAULT '{}'::jsonb,
  frequency        VARCHAR(50) NOT NULL CHECK (frequency IN ('real_time','hourly','daily','weekly')),
  channels         JSONB NOT NULL DEFAULT '[]'::jsonb,
  recipients       JSONB NOT NULL DEFAULT '[]'::jsonb,
  is_active        BOOLEAN NOT NULL DEFAULT true,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_triggered   TIMESTAMPTZ,
  trigger_count    INT NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_rules_rule_id   ON alert_rules(rule_id);
CREATE INDEX IF NOT EXISTS idx_rules_type      ON alert_rules(alert_type);
CREATE INDEX IF NOT EXISTS idx_rules_active    ON alert_rules(is_active);

CREATE TABLE IF NOT EXISTS application_statistics_cache (
  id               SERIAL PRIMARY KEY,
  cache_key        VARCHAR(255) UNIQUE NOT NULL,
  period_days      INT NOT NULL,
  source_filter    VARCHAR(50),
  role_filter      VARCHAR(50),
  statistics_data  JSONB NOT NULL,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at       TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cache_key     ON application_statistics_cache(cache_key);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON application_statistics_cache(expires_at);

CREATE TABLE IF NOT EXISTS application_tracking_reports (
  id            SERIAL PRIMARY KEY,
  report_id     VARCHAR(255) UNIQUE NOT NULL,
  report_type   VARCHAR(100) NOT NULL,
  period        VARCHAR(50) NOT NULL,
  format_type   VARCHAR(20) NOT NULL,
  generated_by  INT,
  report_data   JSONB NOT NULL,
  summary_data  JSONB NOT NULL DEFAULT '{}'::jsonb,
  file_path     TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at    TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_reports_id    ON application_tracking_reports(report_id);
CREATE INDEX IF NOT EXISTS idx_reports_type  ON application_tracking_reports(report_type);
CREATE INDEX IF NOT EXISTS idx_reports_time  ON application_tracking_reports(created_at);

COMMIT;