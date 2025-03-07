---
summary: Learn to configure PingFederate as an external identity provider for OutSystems 11 (O11), covering LDAP setups and token management.
tags: identity provider configuration, pingfederate, active directory, ldap, token management
locale: en-us
guid: 8c57419b-f92a-4e5d-bcbc-f2b89abb2a28
app_type: traditional web apps, mobile apps, reactive web apps
platform-version: o11
figma:
audience:
  - platform administrators
  - full stack developers
  - backend developers
  - architects
  - tech leads
outsystems-tools:
  - none
coverage-type:
  - apply
---

# Configuring PingFederate as an external identity provider

## Prerequisites

* A running instance of PingFederate server
* Existing users in the server's active directory's user store.
To configure PingFederate as an external IdP, follow these steps:

## 1. Configure an active directory as a user datastore

Establish an Active Directory datastore connection for retrieving user attributes for outbound connections.

**LDAP configuration details:**

* **Authentication method**: Simple
* **User DN**: Distinguished name of the active directory user used to authenticate the user store.
* **Password**: Active directory user password

For more information, refer to  [Configuring an Active Directory datastore](https://docs.pingidentity.com/r/en-us/solution-guides/htg_config_ad_datastore_pingfed).

## 2. Create a password credential validator instance

**Instance configuration details:**

* **Search Filter**: ``(|(sAMAccountName=${username})(userPrincipalName=${username}))``
* **Scope of Search**: Subtree

For more information, refer to [Creating an LDAP Username Password Credential Validator instance](https://docs.pingidentity.com/r/en-us/pingfederate-112/pf_creat_ldap_username_pass_credent_validat_instanc).

## 3. Configure the authorization server settings

The **Authorization Server Settings** window provides controls over the usage and behavior of PingFederate as an authorization server (AS), including the policies and settings for various grant types, refresh tokens, persistent grants, and ID tokens.

Make sure to add the **email** and **preferred_username** as **Persistent Grant Extended Attributes**.

For more information, refer to [Configuring authorization server settings](https://docs.pingidentity.com/r/en-us/pingfederate-112/help_authorizationserversettingstasklet_oauthauthorizationserversettingsstate).

## 4. Configure scopes

In addition to OAuth, PingFederate supports the use of scopes to constrain and define access privileges.

**openid**, **email**, **profile**, and **offline_access** scopes are mandatory settings.

For more information, refer to [Scopes](https://docs.pingidentity.com/r/en-us/pingfederate-111/pf_scopes).

## 5. Configure access token management

Define your access token management instance. This capability allows you to configure different access token policies and attribute contracts for different OAuth clients. It also allows you to control the validation of access tokens to one or more resource servers.

For more information, refer to [Defining an access token management instance](https://docs.pingidentity.com/r/en-us/pingfederate-101/help_beareraccesstokenmgmtplugintasklet_selectadaptertypestate).

## 6. Configure access token mappings

To define how access tokens are created, use the **Access Token Manager Mapping** tab to associate one or more access token manager instances with the connection.

For more information, refer to [Configuring access token manager mappings](https://docs.pingidentity.com/r/en-us/pingfederate-112/help_oauthsamlgrantattributemappingtasklet_oauthsaml2targetmappingliststate). 

## 7. Configure OpenID Connect policy management

This configuration allows you to define OpenID Connect policies for client access to attributes mapped according to OpenID specifications. Ensure "INCLUDE USER INFO IN ID TOKEN" and "RETURN ID TOKEN ON REFRESH GRANT" are selected.

For more information, refer to [Configuring OpenID Connect policies](https://docs.pingidentity.com/r/en-us/pingfederate-101/help_policiesmanagementtasklet_policiesmanagementstate). 

## 8. Configure IdP adapters

For more information, refer to [Configuring the IdP adapter](https://docs.pingidentity.com/r/en-us/solution-guides/gdn1597773067220).

## 9. Configure IdP adapter grant mapping

For more information, refer to [Managing IdP adapter grant mapping](https://docs.pingidentity.com/r/en-us/pingfederate-100/help_oauthsource2targetmappingtasklet_oauthidpadapter2targetmappingsstate).

## 10. Create clients (Web and Desktop) 

#### Web client

**Redirect URIs**: 
For each of the environments on your infrastructure (including Lifetime), add a new URI for the Service Center login page: ``https://<YOUR_ENV>/ServiceCenter/CentralizedLogin_AuthCodeFlow_TokenPart.aspx``
  
**Allowed Grant Types**: Select Authorization Code, Refresh Token, Client Credentials.

#### Native client

**Redirect URIs**: Add the following redirect URIs for mobile and desktop applications:
* ``integrationstudio://auth``
* ``servicestudiox11://auth``
* ``https://experiencebuilder.outsystems.com/Authentication/OIDC_Callback``
* ``https://workflowbuilder.outsystems.com/Authentication/OIDC_Callback``
* ``https://integrationbuilder.outsystems.com/Authentication/OIDC_Callback``
* ``https://aimentorstudio.outsystems.com/Authentication/OIDC_Callback``
* For each OutSystems environment in your infrastructure (excluding Lifetime), add an **Integration Managers URI**: ``https://<YOUR_ENV>/OSIntegrationManager/OIDC_Callback``

**Allowed Grant Types**: Select Authorization Code and Refresh Token.

For more information, refer to [Configuring an OAuth client](https://docs.pingidentity.com/r/en-us/solution-guides/mzt1663945300370).

## 11. Configure PingFederate as OpenID connect provider in Lifetime

Follow the steps mentioned [here](external-idp-lifetime.md).