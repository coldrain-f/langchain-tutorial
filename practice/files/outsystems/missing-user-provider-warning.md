---
summary: OutSystems 11 (O11) troubleshooting guide for resolving missing User Provider module errors during application runtime.
tags: outsystems, troubleshooting, application runtime, platform server, user provider
locale: en-us
guid: 708e1290-d4e0-4877-96fa-19876fd8b685
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
audience:
  - mobile developers
  - frontend developers
  - full stack developers
  - platform administrators
outsystems-tools:
  - service studio
  - platform server
coverage-type:
  - unblock
---

# Missing User Provider Warning

## Could not find the &lt;provider> User Provider module in this server. Application runtime errors might occur

**Cause**

Your module has a User Provider module that does not exist in the Platform Server you are publishing to.

**Recommended action**

Do one of the following:

* Check with the Platform Server administrator or with the User Provider's owner to determine what the cause might be for this situation.
* Change the User Provider [module](../../../ref/lang/auto/class-module.md) property of your module.
