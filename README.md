NetControlSuite v2

NetControlSuite is a modular, vendor-agnostic Network Lifecycle, Automation, and Event Intelligence platform designed to manage network infrastructure in a structured, auditable, and scalable manner.

It unifies:

Device Discovery

Registry & Lifecycle Management

Configuration Backup & Comparison

Command Execution

Inventory & Commercial Tracking

Event Processing & Correlation

Alerting & Governance

📌 Project Vision

NetControlSuite aims to provide:

A Unified Network Control & Governance Platform that combines automation, monitoring, configuration intelligence, and commercial lifecycle tracking into a single structured system.

Unlike traditional tools that focus on only automation or monitoring, NetControlSuite integrates:

Operational control

State awareness

Change detection

Lifecycle governance

Alert correlation

🚀 Key Features
1️⃣ Device Discovery & Provisioning

Subnet scanning

Approval-based onboarding

UUID-based device identity

Site-based registry structure

Lifecycle states (ACTIVE / DECOMMISSIONED)

2️⃣ Unified Device Registry

Each site maintains a structured device_registry.json containing:

UUID device_id

mgmt_ip

protocol (SSH/Telnet)

authentication data

lifecycle status

metadata timestamps

The registry acts as the single source of truth.

3️⃣ Execution Planner

All execution modules (Backup, Inventory, Command Executor) rely on:

Centralized device selection logic

Lifecycle enforcement

Mode-based filtering:

all

site

device_ids

mgmt_ips

Prevents duplication of selection logic.

4️⃣ Configuration Backup

Multi-vendor CLI support

Enable mode handling

Raw session logging

Versioned configuration storage

Structured backup history

Diff reports (TXT & HTML)

Config Compare Phase

Detects configuration drift

Identifies changes between versions

Supports compliance validation

Enables governance-level monitoring

5️⃣ Command Executor

Controlled execution of command sets

Execution history tracking

Per-device logging

Structured reporting

6️⃣ Inventory Management

Vendor detection (priority-based resolution)

Adapter-based parsing model

Field-level source tracking (manual vs auto)

Change detection log

Contract monitoring

Inventory tracks:

Hostname

Vendor

Platform

Model

Serial number

OS version

Hardware version

Commercial contract metadata

7️⃣ Event Processing Engine

Structured event ingestion

Event normalization

Device-based event association

Event history logging

8️⃣ Correlation Phase

Reduces noise by:

Grouping related events

Identifying potential root causes

Preventing alert storms

Example:
Multiple interface-down events → Single correlated incident

9️⃣ Alerting System

Event-driven alert generation

Severity handling

Flap tracking

Escalation readiness

Integration-ready architecture

Alerts may originate from:

Device down

Config drift

Inventory failure

Contract expiry

Correlated event clusters

🏗 Architecture Overview

NetControlSuite follows a layered modular architecture:

API Layer (FastAPI + Swagger)
        ↓
Control Layer (ExecutionPlanner, Alert Engine, Correlation)
        ↓
Module Layer
  - Discovery
  - Provisioning
  - Config Backup
  - Command Executor
  - Inventory
  - Events
        ↓
Core Layer
  - Registry
  - Protocol Engines (SSH/Telnet)
  - Diff Engine
        ↓
Data Layer (Structured File-Based Storage)
📂 Current Project Structure (Full)
│   NetCS_Dir_Stru.txt
│   README.md
│   
├───backend
│   │   main.py
│   │   
│   ├───api
│   │   │   __init__.py
│   │   │   
│   │   ├───routes
│   │   │   │   alerts.py
│   │   │   │   command_executor.py
│   │   │   │   command_executor_history.py
│   │   │   │   config_backup.py
│   │   │   │   config_compare.py
│   │   │   │   credentials.py
│   │   │   │   discovery.py
│   │   │   │   execution.py
│   │   │   │   history.py
│   │   │   │   inventory.py
│   │   │   │   modules.py
│   │   │   │   org.py
│   │   │   │   provisioning.py
│   │   │   │   __init__.py
│   │   │   │   
│   │   │   ├───depricated
│   │   │   │       device_registry.py
│   │   │   │       inventory.py
│   │   │   │       
│   │   │   └───__pycache__
│   │   │           command_executor.cpython-312.pyc
│   │   │           command_executor_history.cpython-312.pyc
│   │   │           config_backup.cpython-312.pyc
│   │   │           credentials.cpython-312.pyc
│   │   │           device_registry.cpython-312.pyc
│   │   │           discovery.cpython-312.pyc
│   │   │           execution.cpython-312.pyc
│   │   │           history.cpython-312.pyc
│   │   │           inventory.cpython-312.pyc
│   │   │           modules.cpython-312.pyc
│   │   │           org.cpython-312.pyc
│   │   │           orgs.cpython-312.pyc
│   │   │           provisioning.cpython-312.pyc
│   │   │           __init__.cpython-312.pyc
│   │   │           
│   │   └───__pycache__
│   │           __init__.cpython-312.pyc
│   │           
│   ├───core
│   │   │   app_config.py
│   │   │   bootstrap.py
│   │   │   client_settings.py
│   │   │   context.py
│   │   │   credentials.py
│   │   │   diff_engine.py
│   │   │   execution_planner.py
│   │   │   execution_tracker.py
│   │   │   job_manager.py
│   │   │   org_manager.py
│   │   │   org_service.py
│   │   │   path_resolver.py
│   │   │   security.py
│   │   │   site_manager.py
│   │   │   
│   │   ├───logging
│   │   │   │   base_logger.py
│   │   │   │   command_executor_logger.py
│   │   │   │   config_backup_logger.py
│   │   │   │   discovery_logger.py
│   │   │   │   retention_manager.py
│   │   │   │   
│   │   │   └───__pycache__
│   │   │           base_logger.cpython-312.pyc
│   │   │           command_executor_logger.cpython-312.pyc
│   │   │           config_backup_logger.cpython-312.pyc
│   │   │           discovery_logger.cpython-312.pyc
│   │   │           retention_manager.cpython-312.pyc
│   │   │           
│   │   ├───protocols
│   │   │   │   session_base.py
│   │   │   │   ssh_engine.py
│   │   │   │   telnet_engine.py
│   │   │   │   
│   │   │   └───__pycache__
│   │   │           session_base.cpython-312.pyc
│   │   │           ssh_engine.cpython-312.pyc
│   │   │           telnet_engine.cpython-312.pyc
│   │   │           
│   │   └───__pycache__
│   │           app_config.cpython-312.pyc
│   │           bootstrap.cpython-312.pyc
│   │           client_settings.cpython-312.pyc
│   │           context.cpython-312.pyc
│   │           credentials.cpython-312.pyc
│   │           device_registry.cpython-312.pyc
│   │           diff_engine.cpython-312.pyc
│   │           execution_logger.cpython-312.pyc
│   │           execution_planner.cpython-312.pyc
│   │           execution_tracker.cpython-312.pyc
│   │           job_manager.cpython-312.pyc
│   │           org_service.cpython-312.pyc
│   │           path_resolver.cpython-312.pyc
│   │           security.cpython-312.pyc
│   │           
│   ├───modules
│   │   ├───command_executor
│   │   │   │   service.py
│   │   │   │   ssh_command_client.py
│   │   │   │   telnet_command_client.py
│   │   │   │   utils.py
│   │   │   │   
│   │   │   └───__pycache__
│   │   │           credentials.cpython-312.pyc
│   │   │           service.cpython-312.pyc
│   │   │           ssh_command_client.cpython-312.pyc
│   │   │           telnet_command_client.cpython-312.pyc
│   │   │           utils.cpython-312.pyc
│   │   │           
│   │   ├───config_backup
│   │   │   │   service.py
│   │   │   │   settings.py
│   │   │   │   ssh_client.py
│   │   │   │   telnet_client.py
│   │   │   │   utils.py
│   │   │   │   
│   │   │   └───__pycache__
│   │   │           credentials.cpython-312.pyc
│   │   │           service.cpython-312.pyc
│   │   │           settings.cpython-312.pyc
│   │   │           ssh_client.cpython-312.pyc
│   │   │           telnet_client.cpython-312.pyc
│   │   │           utils.cpython-312.pyc
│   │   │           
│   │   ├───config_compare
│   │   │       service.py
│   │   │       
│   │   ├───discovery
│   │   │   │   service.py
│   │   │   │   
│   │   │   └───__pycache__
│   │   │           service.cpython-312.pyc
│   │   │           
│   │   ├───events
│   │   │   │   alert_store.py
│   │   │   │   device_resolver.py
│   │   │   │   event_store.py
│   │   │   │   settings_service.py
│   │   │   │   
│   │   │   ├───correlation
│   │   │   │       engine.py
│   │   │   │       rules.py
│   │   │   │       
│   │   │   └───listener
│   │   │           syslog_listener.py
│   │   │           
│   │   └───inventory
│   │       │   arp_utils.py
│   │       │   change_detector.py
│   │       │   contract_monitor.py
│   │       │   contract_notifier.py
│   │       │   contract_scheduler.py
│   │       │   mini_executor.py
│   │       │   oui_db.json
│   │       │   service.py
│   │       │   vendor_detection.py
│   │       │   
│   │       ├───adapters
│   │       │   │   allied.py
│   │       │   │   base.py
│   │       │   │   cisco.py
│   │       │   │   dlink.py
│   │       │   │   generic.py
│   │       │   │   tplink.py
│   │       │   │   __init__.py
│   │       │   │   
│   │       │   └───__pycache__
│   │       │           allied.cpython-312.pyc
│   │       │           base.cpython-312.pyc
│   │       │           cisco.cpython-312.pyc
│   │       │           dlink.cpython-312.pyc
│   │       │           generic.cpython-312.pyc
│   │       │           tplink.cpython-312.pyc
│   │       │           __init__.cpython-312.pyc
│   │       │           
│   │       ├───tools
│   │       │       build_oui_db.py
│   │       │       oui.csv
│   │       │       
│   │       └───__pycache__
│   │               arp_utils.cpython-312.pyc
│   │               change_detector.cpython-312.pyc
│   │               contract_monitor.cpython-312.pyc
│   │               contract_notifier.cpython-312.pyc
│   │               contract_scheduler.cpython-312.pyc
│   │               mini_executor.cpython-312.pyc
│   │               service.cpython-312.pyc
│   │               vendor_detection.cpython-312.pyc
│   │               
│   └───__pycache__
│           main.cpython-312.pyc
│           
├───data
│   │   app.key
│   │   
│   └───orgs
│       └───org_001
│           │   org.json
│           │   
│           └───sites
│               └───site_001
│                   │   device_registry.json
│                   │   site.json
│                   │   
│                   ├───command_executor
│                   │   │   commands.txt
│                   │   │   settings.json
│                   │   │   
│                   │   ├───credentials
│                   │   │       creds.enc
│                   │   │       
│                   │   ├───debug_raw
│                   │   │   └───23-02-2026
│                   │   │           192.168.9.15-10.57.30-ssh.raw
│                   │   │           192.168.9.3-10.57.30-ssh.raw
│                   │   │           
│                   │   ├───execution_logs
│                   │   ├───logs
│                   │   │       execution.log
│                   │   │       
│                   │   ├───outputs
│                   │   │   └───5aa88066-860e-4d23-b72f-5bbb742ad51d
│                   │   │           2320be86-2684-4ef8-bf9c-88dc6a45024d.txt
│                   │   │           6e1721b0-36da-4eea-999b-fc7ff8cc0022.txt
│                   │   │           
│                   │   └───reports
│                   ├───config_backup
│                   │   │   commands.txt
│                   │   │   settings.json
│                   │   │   
│                   │   ├───backups
│                   │   │   ├───21-02-2026
│                   │   │   │       !enable-14_v1.txt
│                   │   │   │       4e053e30-14e3-4e76-a0cb-6bce2720318c-5_v1.txt
│                   │   │   │       L1-PoE-3_v1.txt
│                   │   │   │       L1-PoE-3_v2.txt
│                   │   │   │       L5-DATA-4_v1.txt
│                   │   │   │       L5-DATA-4_v2.txt
│                   │   │   │       TEST-PROBUS-15_v1.txt
│                   │   │   │       TEST-PROBUS-15_v2.txt
│                   │   │   │       
│                   │   │   └───23-02-2026
│                   │   │           e6d90449-f572-41b7-80b2-cc893a787b59-14_v1.txt
│                   │   │           e6d90449-f572-41b7-80b2-cc893a787b59-14_v2.txt
│                   │   │           
│                   │   ├───credentials
│                   │   │       creds.enc
│                   │   │       
│                   │   ├───debug_raw
│                   │   │   ├───21-02-2026
│                   │   │   │       192.168.9.14-16.22.16-ssh.raw
│                   │   │   │       192.168.9.15-16.24.35-ssh.raw
│                   │   │   │       192.168.9.3-16.21.58-ssh.raw
│                   │   │   │       192.168.9.3-16.55.51-ssh.raw
│                   │   │   │       192.168.9.4-16.58.01-telnet.raw
│                   │   │   │       192.168.9.5-17.29.11-ssh.raw
│                   │   │   │       
│                   │   │   └───23-02-2026
│                   │   │           192.168.9.14-10.51.41-telnet.raw
│                   │   │           
│                   │   ├───execution_logs
│                   │   │       10957b96-6701-405b-b595-85c70d5095af.json
│                   │   │       
│                   │   ├───logs
│                   │   │   ├───21-02-2026
│                   │   │   │       auth.log
│                   │   │   │       
│                   │   │   └───23-02-2026
│                   │   │           auth.log
│                   │   │           
│                   │   └───reports
│                   │       ├───21-02-2026
│                   │       │       4e053e30-14e3-4e76-a0cb-6bce2720318c_5_diff.html
│                   │       │       4e053e30-14e3-4e76-a0cb-6bce2720318c_5_diff.txt
│                   │       │       e6d90449-f572-41b7-80b2-cc893a787b59_14_diff.html
│                   │       │       e6d90449-f572-41b7-80b2-cc893a787b59_14_diff.txt
│                   │       │       L1-PoE_3_diff.html
│                   │       │       L1-PoE_3_diff.txt
│                   │       │       L5-DATA_4_diff.html
│                   │       │       L5-DATA_4_diff.txt
│                   │       │       TEST-PROBUS_15_diff.html
│                   │       │       TEST-PROBUS_15_diff.txt
│                   │       │       
│                   │       └───23-02-2026
│                   │               e6d90449-f572-41b7-80b2-cc893a787b59_14_diff.html
│                   │               e6d90449-f572-41b7-80b2-cc893a787b59_14_diff.txt
│                   │               
│                   └───discovery
│                       ├───logs
│                       │       8ba20718-0696-49ca-9e3f-41f4768e687e.json
│                       │       
│                       └───scans
│                           └───8ba20718-0696-49ca-9e3f-41f4768e687e
│                                   scan_metadata.json
│                                   scan_results.json
│                                   
├───prompts
│       login_password.txt
│       login_username.txt
│       
└───resources
        commands.txt
        ip_list.txt
        login_password.txt
        login_username.txt
        
👥 Intended Users
Network Operators

Run backups

Execute commands

Review alerts

Network Engineers

Analyze configuration drift

Review change logs

Validate device inventory

NOC Teams

Monitor correlated events

Respond to alerts

IT Governance / Procurement

Track support contracts

Monitor hardware lifecycle

Review compliance status

🖥 API Interface

NetControlSuite uses FastAPI and provides interactive API documentation via Swagger:

http://127.0.0.1:8000/docs

Modules exposed include:

Discovery

Provisioning

Config Backup

Command Executor

Inventory

Alerts

Events

⚙️ Deployment
Current Model

Python 3.12

FastAPI

Uvicorn ASGI server

On-premise deployment

File-based structured storage

Run locally:

uvicorn backend.main:app --reload
🔐 Design Principles

Modular architecture

UUID-based identity

Lifecycle enforcement

Vendor-agnostic adapters

State-aware automation

Structured logging

Governance-ready design

Separation of API and core logic

🛣 Roadmap
Phase 2

Vendor-specific CLI abstraction

Enhanced prompt detection

ANSI stripping

Retry logic

Phase 3

Stand-alone dashboard UI App

RBAC (Role-Based Access Control)

Scheduled jobs (backup, inventory, compliance)

Alert escalation pipeline

Phase 4

Database-backed storage (PostgreSQL/SQLite)

Multi-tenant scaling

External integrations (SIEM/NMS)

🎯 Long-Term Vision

NetControlSuite aims to evolve into:

A Unified Network Lifecycle & Event Intelligence Platform combining Automation, Monitoring, Governance, and Commercial Control.

📜 License

(Under development phase. We will update later)