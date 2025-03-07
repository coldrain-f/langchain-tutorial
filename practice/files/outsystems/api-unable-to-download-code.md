---
summary: Explore troubleshooting steps for downloading application source code in OutSystems 11 (O11).
tags: troubleshooting guide, environment configuration, api usage, permissions management, service accounts
locale: en-us
guid: E542C662-6053-4758-A514-1A4117364DD0
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
audience:
  - platform administrators
  - full stack developers
  - backend developers
outsystems-tools:
  - lifetime
  - service center
coverage-type:
  - remember
---

# Unable to download the source code of an application

This article explains how you can troubleshoot if you are getting an error [downloading the source code package of an application](api-request-code.md).

## Step 1: Check if the user has Open and Debug over the application

To validate this requirement, follow these steps:

1. In the LifeTime management console, open the **User Management** tab and select the Service Accounts sub-menu.
1. Select the service account used on the source code access API by clicking the service account name.
1. Check if the level of permission of the user is Open and Debug on the environment you are requesting the source code.

The wrong permissions level returns a message: `You need permission to access the environment {EnvironmentKey} or the app {ApplicationKey}.`

## Step 2: Check if the environment key exists

Call the API method that returns all the environments registered on your infrastructure.
Request: `GET /lifetimeapi/rest/v2/environments/`

Response body:

```
[
  {...},
  {
    "Key": "849515f2-b4ff-4aca-a9d6-9407bea655f4",
    "Name": "Testing",
    "OSVersion": "11.0.110.0",
    "Order": 1,
    "HostName": "prd-env-1.company.com",
    "UseHTTPS": true,
    "EnvironmentType": "Production",
    "NumberOfFrontEnds": 1,
    "ApplicationServerType": ".NET",
    "ApplicationServer": "IIS",
    "DatabaseProvider": "SQLServer",
    "IsCloudEnvironment": false
  },
  {...}
]
```

Check that the environment key (**Key**) is correctly passed to the API call.

If the environment key does not exist, the API returns a message: `The environment {EnvironmentKey} or the app {ApplicationKey} doesn't exist.`

## Step 3: Check if the resource exists

### Step 3.1: Check if the application key exists

<div class = "info" markdown="1">

If calling the application's endpoints.

</div>

Call the API that returns all the applications available on your infrastructure.

Request: `GET /lifetimeapi/rest/v2/applications/`

Response body:

```
[
  {...},
  {
    "Key": "c9a7a82e-0eee-4a3d-8e22-2a19c69c766f",
    "Name": "EmployeeBackoffice",
    "Kind": "WebResponsive",
    "Team": "",
    "Description": "",
    "URLPath": "/EmployeeBackoffice",
    "IconHash": "IconHash6a79e71e-c8e5-9e18-115c-cab789517672",
    "IconURL": "/LifeTimeSDK/ApplicationIcon.aspx?ApplicationKey=c9a7a82e-0eee-4a3d-8e22-2a19c69c766f",
    "IsSystem": false,
    "AppStatusInEnvs": []
  },
  {...}
]
```

Check that the application key (**Key**) is passed correctly to the API call.

If the application key does not exist, the API returns a message: `The environment {EnvironmentKey} or the app {ApplicationKey} doesn't exist.`

### Step 3.2: Check if the module key exists

<div class = "info" markdown="1">

If calling the module's endpoints.

</div>

Call the API that returns all the modules available on your infrastructure.

Request: `GET /lifetimeapi/rest/v2/modules/`

Response body:

```
[
    {...},
    {
        "Key": "c9a7a82e-0eee-4a3d-8e22-2a19c69c766f",
        "Name": "EmployeeBackoffice",
        "Description": "",
        "Kind": "eSpace",
        "ModuleStatusInEnv": []
    },
    {...}
]
```

Check that the module key (**Key**) is passed correctly to the API call.

If the module key does not exist, the API returns a message: `The environment {EnvironmentKey} or the module {ModuleKey} doesn't exist.`

## Step 4: Error in the get download link

If you encounter errors getting the download link:
Request: `GET /environments/{EnvironmentKey}/modules/{ModuleKey}/sourcecodeaccess/{PackageKey}/download`

Check that the operation's status is **Done**. To do this, call the endpoint status and check the **Status** property.
Request: `GET /environments/{EnvironmentKey}/modules/{ModuleKey}/sourcecodeaccess/{PackageKey}/status`

```
{
  "PackageKey": "bc354abb-6691-41ee-9ed3-9454747e2d4d",
  "Status": "Done",
  "Messages": [
    {...}
  ]
}
```

## Step 5: Check if the package is bigger than the size limit

If you see an Error message such as **The resulting source code package has X Mb. The maximum size allowed is 150 Mb. Please refer to documentation on how to overcome this error.**, this means that the resulting source code archive is bigger than 150Mb. In such scenarios, because of scalability and performance reasons the API cannot store and send such big files.

As a workaround, you can call the [Module version of the API](api-request-code.md#get-the-source-code-of-a-module) to get the source code at the module level.

If the above validations didn't help you solve the issue and you need further assistance, [open a support case](https://www.outsystems.com/SupportPortal/CaseOpen/) to get help from OutSystems Support.
