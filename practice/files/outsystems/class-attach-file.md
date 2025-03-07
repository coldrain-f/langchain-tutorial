---
summary: Learn how to attach a file to an email using OutSystems 11 (O11), including mandatory properties like 'Name' and 'File Content'.
locale: en-us
guid: 05294b82-4021-4992-abe8-41d7d285b55b
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
tags: email attachment, file management, web development, outsystems platform, user interface components
audience:
  - mobile developers
  - frontend developers
  - full stack developers
outsystems-tools:
  - service studio
coverage-type:
  - remember
---

# Attach File

Attaches a file to an e-mail.  

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
<td title="File Name">File Name</td>
<td>Text literal or expression with the name of the file, including the extension.</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td title="File Content">File Content</td>
<td>Holds the file selected by the user.</td>
<td>Yes</td>
<td></td>
<td></td>
</tr>
<tr>
<td title="Mime-Type">Mime-Type</td>
<td>Text literal or expression specifying the media type of the file.</td>
<td></td>
<td></td>
<td>Example values:<br/>
– "application/x-msexcel";<br/>
– "application/msword";<br/>
– "application/pdf";<br/>
– "image/gif";<br/>
– "text/html";<br/>
– "video/avi";<br/>
– "audio/wav".</td>
</tr>
</tbody>
</table>

