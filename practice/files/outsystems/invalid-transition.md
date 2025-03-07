---
summary: OutSystems 11 (O11) generates an "Invalid Transition" error when a reverse transition is incorrectly set for a screen destination.
locale: en-us
guid: d844068c-7299-46e1-80e4-6f7a6a0d8942
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
tags: error handling, debugging, user interface, ide usage, reactive web apps
audience:
  - mobile developers
  - frontend developers
  - full stack developers
outsystems-tools:
  - service studio
coverage-type:
  - unblock
---

# Invalid Transition

The `Invalid Transition` error is issued in the following situations:

* `(Reverse Transition) is not a valid transition for <Screen>. This transition is only applicable to (Previous Screen) destinations.`

    You have a Destination node with the property Transition set to `(Reverse Transition)`, but this transition can only be used if the property Destination is `(Previous Screen)`.

    Change the property Destination to `(Previous Screen)` or choose another transition.

Double-click on the error line to take you directly to the source of the error.
