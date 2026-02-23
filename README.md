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
📂 Project Structure (Simplified)
backend/
  api/
    routes/
      discovery.py
      provisioning.py
      config_backup.py
      inventory.py
      command_executor.py
      alerts.py

  core/
    execution_planner.py
    protocol_engines/
    registry utilities

  modules/
    discovery/
    config_backup/
    inventory/
    command_executor/
    alerts/
    events/

data/
  orgs/
    org_001/
      sites/
        site_001/
          device_registry.json
          config_backup/
          inventory/
          command_executor/
          events/
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

Stand-alone UI Application

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

(Under development phase)