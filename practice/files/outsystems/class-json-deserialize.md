---
summary: OutSystems 11 (O11) JSON Deserialize feature converts JSON strings into various data types with configurable properties.
helpids: 30004
locale: en-us
guid: ed1575d2-e5b5-41a1-be11-e638b406fbb4
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
tags: json parsing, data serialization, application development, api integration, data transformation
audience:
  - mobile developers
  - frontend developers
  - full stack developers
outsystems-tools:
  - service studio
coverage-type:
  - remember
---

# JSON Deserialize

JSON Deserialize converts JSON string to one of the following data types:

* Entity or Static Entity
* Structure
* List

## Properties

<table markdown="1">
<thead>
<tr>
<th>Name</th>
<th>Description</th>
<th>Mandatory</th>
<th>Default value</th>
<th>Observations</th>
</tr>
</thead>
<tbody>
<tr>
<td title="Name">Name</td>
<td>Identifies an element in the scope where it is defined, like a screen, action, or module.</td>
<td>Yes</td>
<td></td>
<td></td>
</tr>
<tr>
<td title="Description">Description</td>
<td>Text that documents the element.</td>
<td></td>
<td></td>
<td>Useful for documentation purpose.<br/>The maximum size of this property is 2000 characters.</td>
</tr>
<tr>
<td title="JSON String">JSON String</td>
<td>JSON string with the data to be deserialized to a Record or List.</td>
<td>Yes</td>
<td></td>
<td></td>
</tr>
<tr>
<td title="Data Type">Data Type</td>
<td>List or Structure of the data in the JSON string. If you want to add a Record composed of Attributes of several Entities, create a Structure first.</td>
<td>Yes</td>
<td></td>
<td></td>
</tr>
<tr>
<td title="Date Format">Date Format</td>
<td>Date format used in the JSON string.</td>
<td>Yes</td>
<td>2014-01-01T00:00:00Z (ISO)</td>
<td></td>
</tr>
</tbody>
</table>

## Runtime Properties

<table markdown="1">
<thead>
<tr>
<th>Name</th>
<th>Description</th>
<th>Read Only</th>
<th>Type</th>
<th>Observations</th>
</tr>
</thead>
<tbody>
<tr>
<td>Data</td>
<td>The Record or List with the JSON data.</td>
<td></td>
<td>Record, Record List</td>
<td></td>
</tr>
</tbody>
</table>

## Additional notes

Check [JSON Serialize](<class-json-serialize.md#notes>) for additional remarks on the JSON Deserialize/Serialize operations.

