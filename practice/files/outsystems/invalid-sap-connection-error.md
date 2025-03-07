---
summary: OutSystems 11 (O11) triggers an "Invalid SAP Connection" error when no remote functions are linked to a SAP connection.
locale: en-us
guid: 6af39380-3f07-4666-bd86-865b63ed4703
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
tags: sap integration, error handling, configuration, debugging, troubleshooting
audience:
  - mobile developers
  - frontend developers
  - full stack developers
outsystems-tools:
  - service studio
coverage-type:
  - unblock
---

# Invalid SAP Connection Error

The `Invalid SAP Connection` error is issued in the following situation:

* `(<connection name>) must have at least one remote function`
  
    You created a SAP connection without importing any remote functions, or deleted all remote functions of an existing SAP connection. 
  
    To solve this error, import at least one remote function, or delete the connection.

Double-click on the error line to take you directly to the SAP Connection where the problem was detected.
