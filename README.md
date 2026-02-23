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
│                   │   │   │       4e053e30-14e3-4e76-a0cb-6bce2720318c-5_v2.txt
│                   │   │   │       4e053e30-14e3-4e76-a0cb-6bce2720318c-5_v3.txt
│                   │   │   │       e6d90449-f572-41b7-80b2-cc893a787b59-14_v1.txt
│                   │   │   │       e6d90449-f572-41b7-80b2-cc893a787b59-14_v2.txt
│                   │   │   │       e6d90449-f572-41b7-80b2-cc893a787b59-14_v3.txt
│                   │   │   │       e6d90449-f572-41b7-80b2-cc893a787b59-14_v4.txt
│                   │   │   │       e6d90449-f572-41b7-80b2-cc893a787b59-14_v5.txt
│                   │   │   │       L1-PoE-3_v1.txt
│                   │   │   │       L1-PoE-3_v2.txt
│                   │   │   │       L1-PoE-3_v3.txt
│                   │   │   │       L5-DATA-4_v1.txt
│                   │   │   │       L5-DATA-4_v2.txt
│                   │   │   │       L5-DATA-4_v3.txt
│                   │   │   │       TEST-PROBUS-15_v1.txt
│                   │   │   │       TEST-PROBUS-15_v2.txt
│                   │   │   │       TEST-PROBUS-15_v3.txt
│                   │   │   │       TEST-PROBUS-15_v4.txt
│                   │   │   │       TEST-PROBUS-15_v5.txt
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
│                   │   │   │       192.168.9.14-16.56.09-ssh.raw
│                   │   │   │       192.168.9.14-17.26.27-ssh.raw
│                   │   │   │       192.168.9.14-17.53.03-ssh.raw
│                   │   │   │       192.168.9.14-17.56.11-ssh.raw
│                   │   │   │       192.168.9.14-18.02.59-telnet.raw
│                   │   │   │       192.168.9.15-16.24.35-ssh.raw
│                   │   │   │       192.168.9.15-16.58.28-ssh.raw
│                   │   │   │       192.168.9.15-17.29.18-ssh.raw
│                   │   │   │       192.168.9.15-17.38.05-ssh.raw
│                   │   │   │       192.168.9.15-17.48.08-ssh.raw
│                   │   │   │       192.168.9.3-16.21.58-ssh.raw
│                   │   │   │       192.168.9.3-16.55.51-ssh.raw
│                   │   │   │       192.168.9.3-17.26.09-ssh.raw
│                   │   │   │       192.168.9.4-16.24.07-telnet.raw
│                   │   │   │       192.168.9.4-16.58.01-telnet.raw
│                   │   │   │       192.168.9.4-17.28.50-telnet.raw
│                   │   │   │       192.168.9.5-16.24.29-ssh.raw
│                   │   │   │       192.168.9.5-16.58.22-ssh.raw
│                   │   │   │       192.168.9.5-17.29.11-ssh.raw
│                   │   │   │       
│                   │   │   └───23-02-2026
│                   │   │           192.168.9.14-10.43.51-telnet.raw
│                   │   │           192.168.9.14-10.51.41-telnet.raw
│                   │   │           
│                   │   ├───execution_logs
│                   │   │       10957b96-6701-405b-b595-85c70d5095af.json
│                   │   │       1a0968fe-ac5b-48e9-a6d8-5ee465a397cf.json
│                   │   │       2ed93b17-afa5-43fd-8231-a073cd057058.json
│                   │   │       38dbce95-4676-498e-a93f-16e149b300cd.json
│                   │   │       39396ebb-7524-4ccf-95ca-f92ffa80e363.json
│                   │   │       5b7867de-fa5d-42cf-8cd9-dc838530b258.json
│                   │   │       6574aeee-12b8-4b27-9c9a-4e26526efe1b.json
│                   │   │       96d45f84-3bee-4005-9247-30bee22bb217.json
│                   │   │       bc46d5e6-9db0-48d3-81ea-2d17daea1d4c.json
│                   │   │       f006329e-5c2a-46ab-adb2-3fe8ae632456.json
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
        
