---
summary: Explore the properties of input parameters for SAP remote functions in OutSystems 11 (O11), detailing mandatory fields and data types.
helpids: 30066
locale: en-us
guid: 0c2f28f8-e4c4-4b13-9139-fba94b1a2774
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
tags: sap integration, data types, parameter management, api development, traditional web apps
audience:
  - mobile developers
  - frontend developers
  - full stack developers
outsystems-tools:
  - service studio
coverage-type:
  - remember
---

# Input Parameter - SAP Remote Function

Input parameter of an imported SAP remote function.  

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
<td title="Type">Data Type</td>
<td>The data type of the input parameter.</td>
<td>Yes</td>
<td></td>
<td></td>
</tr>
<tr>
<td title="IsMandatory">Is Mandatory</td>
<td>Set to Yes to require for a value to be set.</td>
<td>Yes</td>
<td>Yes</td>
<td></td>
</tr>
<tr>
<td title="DefaultValue">Default Value</td>
<td>Initial value of this element. If undefined, the default value of the data type is used.</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr >
<th colspan="5">Advanced</th>
</tr>
<tr>
<td title="OriginalDescription">OriginalDescription</td>
<td>Original description of the parameter.</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td title="OriginalType">Original Type</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td title="OriginalABAPType">Original ABAP DataType</td>
<td></td>
<td>Yes</td>
<td>Integer</td>
<td></td>
</tr>
</tbody>
</table>

