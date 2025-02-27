---
summary: Resolve the "Resource in Use Error" in OutSystems 11 (O11) by closing interfering external applications.
locale: en-us
guid: b12ff345-5101-4765-997c-97c7150f70a5
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
tags: error resolution, integration studio, application lifecycle management, debugging, application deployment
audience:
  - frontend developers
  - full stack developers
  - platform administrators
outsystems-tools:
  - integration studio
coverage-type:
  - unblock
---

# Resource in Use Error

Message
:   `The resources of the extension are being used by an external application. Close the external application and repeat the operation.`

Cause
:   A resource that needs to be updated by Integration Studio is open in another application.

Recommendation
:   Check which resource is being used by an external application and close it, in order to proceed with the operation in Integration Studio.
