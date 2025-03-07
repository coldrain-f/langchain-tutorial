---
summary: OutSystems 11 (O11) issues an 'Invalid Public Block' error when a public block navigates to screens or uses similar blocks.
locale: en-us
guid: 63bbdcba-14e9-4a53-82af-ba32f92139bb
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
tags: error handling, public blocks, navigation logic, debugging, outsystems platform
audience:
  - frontend developers
  - full stack developers
outsystems-tools:
  - service studio
coverage-type:
  - unblock
---

# Invalid Public Block Error

The `Invalid Public Block` error is issued in the following situations:

* `Block '<Block>' cannot be public. It cannot navigate to Screens using Destination elements or use other blocks that do so.`

    You have a public Block that uses the node Destination to navigate to a Screen or uses another Block that does this. Public Blocks cannot navigate to screens. 

    Remove the navigation to the Screen or set the property Public of the Block to `No`.

Double-click on the error line to take you directly to the source of the error.
