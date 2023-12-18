**IMPORTANT**: No additional bug fixes or documentation updates will be released for this version. For the latest information, see the [current release documentation](../current/index.html). 

[Elastic Docs](/guide/) ›

Workplace Search Guide

  * Enterprise Search guides
    * [Enterprise Search](/guide/en/enterprise-search/current/index.html)
    * [App Search](/guide/en/app-search/current/index.html)
    * [Workplace Search](/guide/en/workplace-search/current/index.html)
  * Programming language clients
    * [Node.js client](https://www.elastic.co/guide/en/enterprise-search-clients/enterprise-search-node/current/index.html)
    * [PHP client](https://www.elastic.co/guide/en/enterprise-search-clients/php/current/index.html)
    * [Python client](https://www.elastic.co/guide/en/enterprise-search-clients/python/current/index.html)
    * [Ruby client](https://www.elastic.co/guide/en/enterprise-search-clients/ruby/current/index.html)

›[Permissions & Access Control](workplace-search-permissions.html)

[« Permissions & Access Control](workplace-search-permissions.html) [Defining
Document Permissions for custom sources »](workplace-search-document-
permissions.html)

## Managing document access & permissions for content
sources[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

The following guide applies to **first-party content sources**. For more
information on custom sources, visit the [Document permissions for custom
sources](workplace-search-document-permissions.html) guide.

Workplace Search can associate its notion of a user to a third-party’s, and in
doing so limit access to documents. If a person has certain permissions on
Google Drive, for example, you can associate their Google Drive user via the
[External Identities API reference](workplace-search-external-identities-
api.html) to their Workplace Search user. When their Workplace Search user
tries to search, their permissions are honoured. As a result, they will see
documents they can see and **not** see documents which they cannot.

This guide will walk you through how to do so with each supporting third-
party.

### First-party content sources[edit](https://github.com/elastic/enterprise-
search-pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-
document-permissions.asciidoc)

Document permission synchronization can be enabled for sources when connecting
an instance to Workplace Search.

We support document permission synchronization within:

  * [Document-level permissions for Atlassian Cloud](workplace-search-sources-document-permissions.html#sources-permissions-atlassian-cloud): Jira Cloud & Confluence Cloud 
  * [Document-level permissions for Box](workplace-search-sources-document-permissions.html#sources-permissions-box): Box 
  * [Document-level permissions for Dropbox](workplace-search-sources-document-permissions.html#sources-permissions-dropbox): Dropbox 
  * [Document-level permissions for Google](workplace-search-sources-document-permissions.html#sources-permissions-google): Google Drive 
  * [Document-level permissions for Microsoft](workplace-search-sources-document-permissions.html#sources-permissions-microsoft): SharePoint Online & OneDrive 

Once activated during connector setup, document access for a user must be
mapped to Workplace Search’s notion of that user. Use the [External Identities
API reference](workplace-search-external-identities-api.html), to provide the
external ```source_user_id``` and link it to its associated Workplace Search
```user```:

    {
    	"source_user_id": "john.doe@example.com",
    	"user": "john.doe"
    }

The above example would link Google’s notion of ```john.doe@example.com``` and
Workplace Search’s notion of ```john.doe``` as the same entity. Permissions
are then synchronized between these entities, restricting or enabling access
to documents. Different content sources will expose their notion of a user in
different ways.

#### Document-level permissions for Atlassian
Cloud[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

Applies to: Confluence Cloud, Jira Cloud

Use the [external identities API](workplace-search-external-identities-
api.html) to map Atlassian Cloud user IDs to Workplace Search usernames for
each of your Confluence and Jira content sources.

First, gather the following information:

Atlassian Cloud user IDs

The string IDs of the Atlassian Cloud users that you’d like to map to
Workplace Search usernames. Example: ```5b10ac8d82e05b22cc7d4ef5```.

Atlassian assigns a string ID to each of its Atlassian Cloud users. The string
identifies the user across all Atlassian Cloud products. However, each product
has its own procedure to get the IDs:

Product Procedure to get user IDs

Confluence

Within the Confluence UI, choose **Settings** > **User Management**. From the
**Users** screen, choose **Export Users**. Within the data file, locate the
```id``` for each user.

If you are using multiple Atlassian Cloud products, filter your list of IDs to
only those users who can access Confluence under your Atlassian license
agreement. These users have the _Use Confluence_ permission. See [Manage
global permissions](https://support.atlassian.com/confluence-
cloud/docs/manage-global-permissions/) in the Atlassian documentation.

Jira

Use the [Users resource of the Jira Cloud
API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-
users/) to request one or more users. Within each response, locate the
```accountId``` for each user.

Workplace Search usernames

The string usernames of the Workplace Search users to which you will map
Atlassian Cloud user IDs. Example: ```sam_foo```.

Use the appropriate UI or API to locate this information within your Elastic
deployment. The specific interface depends on how you [manage
users](workplace-search-security.html).

User mappings

A collection of mappings, where each maps an Atlassian Cloud user ID to a
Workplace Search username.

Store this data in a format that makes sense to you. You will need to
construct one or more API requests for each user mapping.

Content source IDs and access token

The string IDs of the Confluence or Jira content sources within your Workplace
Search deployment, and your personal access token, which grants you access to
write external identities through the API.

See [Content source ID and access token](workplace-search-sources-document-
permissions.html#sources-permissions-content-source-id-token).

Then, send one API request per user mapping, per content source ID:

**Request template:**
    curl \
    --request 'POST' \
    --url '<WORKPLACE_SEARCH_BASE_URL>/api/ws/v1/sources/<CONTENT_SOURCE_ID>/external_identities' \
    --header 'Authorization: Bearer <ACCESS_TOKEN>' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "<WORKPLACE_SEARCH_USERNAME>",
        "source_user_id": "<ATLASSIAN_CLOUD_USER_ID>"
    }'

**Example requests:**
    curl \
    --request 'POST' \
    --url 'http://localhost:3002/api/ws/v1/sources/40bd9d00713a5d9874444410/external_identities' \
    --header 'Authorization: Bearer 64c51eee12c1f7a3be8ab0ecf9a2184106c1641e49736119414da0c0e85f3611' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "john_doe",
        "source_user_id": "91e7f8ba23a0637de213ae6d"
    }'
    curl \
    --request 'POST' \
    --url 'https://f3fae9ab3e4f423d9d345979331ef3a1.ent-search.us-east-1.aws.cloud.es.io:443/api/ws/v1/sources/8fda765d3e474d44e40369d6/external_identities' \
    --header 'Authorization: Bearer 7ea05c8bd50ab5c75d2b71adbcb9ae71c4034d7a4f8d6c16a8940510a951cec7' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "sam.foo",
        "source_user_id": "5b10ac8d82e05b22cc7d4ef5"
    }'

**Jira Cloud notes:**

  * To ensure permissions map from Jira to Workplace Search, define _project permissions_ directly on Jira Cloud groups (or users).

    * Workplace Search does **not** sync other types of permission data, such as _issue-level security permissions_. 

  * Workplace Search syncs permission data from _classic Jira projects_ only.

    * Workplace Search does **not** support syncing permissions from _Jira next-gen projects_. 

  * To make a Jira project visible to all Workplace Search users, use the _Any logged in user_ permission under _Application Access_.

    * Workplace Search does **not** sync the _Public_ group permission. 

**Confluence Cloud notes:**

If anonymous access is enabled for a Confluence Space that you are syncing to
Workplace Search, ensure anonymous access is enabled in your Confluence global
permissions as well. See [Manage global
permissions](https://support.atlassian.com/confluence-cloud/docs/manage-
global-permissions/) in the Atlassian documentation.

The space with anonymous access will be searchable by all of your Workplace
Search users, even those without an external identity mapping.

#### Document-level permissions for
Box[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

Applies to: Box

Use the [external identities API](workplace-search-external-identities-
api.html) to map Box user IDs to Workplace Search usernames for your Box
organization content source.

First, gather the following information:

Box user IDs

The string IDs of the Box users that you’d like to map to Workplace Search
usernames. Example: ```14436967113```.

Use the [List enterprise users](https://developer.box.com/reference/get-
users/) endpoint of the Box API to request a list of all Box users. Within
each of the ```entries```, locate the ```id```.

Workplace Search usernames

The string usernames of the Workplace Search users to which you will map Box
user IDs. Example: ```sam_foo```.

Use the appropriate UI or API to locate this information within your Elastic
deployment. The specific interface depends on how you [manage
users](workplace-search-security.html).

User mappings

A collection of mappings, where each maps a Box user ID to a Workplace Search
username.

Store this data in a format that makes sense to you. You will need to
construct one or more API requests for each user mapping.

Content source IDs and access token

The string IDs of the Box organization content sources within your Workplace
Search deployment, and your personal access token, which grants you access to
write external identities through the API.

See [Content source ID and access token](workplace-search-sources-document-
permissions.html#sources-permissions-content-source-id-token).

Then, send one API request per user mapping, per content source ID:

**Request template:**
    curl \
    --request 'POST' \
    --url '<WORKPLACE_SEARCH_BASE_URL>/api/ws/v1/sources/<CONTENT_SOURCE_ID>/external_identities' \
    --header 'Authorization: Bearer <ACCESS_TOKEN>' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "<WORKPLACE_SEARCH_USERNAME>",
        "source_user_id": "<BOX_USER_ID>"
    }'

**Example requests:**
    curl \
    --request 'POST' \
    --url 'http://localhost:3002/api/ws/v1/sources/40bd9d00713a5d9874444410/external_identities' \
    --header 'Authorization: Bearer 64c51eee12c1f7a3be8ab0ecf9a2184106c1641e49736119414da0c0e85f3611' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "john_doe",
        "source_user_id": "14436967113"
    }'
    curl \
    --request 'POST' \
    --url 'https://f3fae9ab3e4f423d9d345979331ef3a1.ent-search.us-east-1.aws.cloud.es.io:443/api/ws/v1/sources/8fda765d3e474d44e40369d6/external_identities' \
    --header 'Authorization: Bearer 7ea05c8bd50ab5c75d2b71adbcb9ae71c4034d7a4f8d6c16a8940510a951cec7' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "sam.foo",
        "source_user_id": "36658789235"
    }'

#### Document-level permissions for
Dropbox[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

Applies to: Dropbox

Use the [external identities API](workplace-search-external-identities-
api.html) to map Dropbox user IDs to Workplace Search usernames for your
Dropbox organization content source.

A Dropbox Business plan is required in order to enable document-level
permissions.

First, gather the following information:

Google user IDs

The string IDs of the Dropbox users that you’d like to map to Workplace Search
usernames. Dropbox user IDs are email addresses. Example:
```sam.foo@example.com```.

You can export a list of users from the [Dropbox Business Admin
Console](https://www.dropbox.com/team/admin/members).

Workplace Search usernames

The string usernames of the Workplace Search users to which you will map
Dropbox user IDs. Example: ```sam_foo```.

Use the appropriate UI or API to locate this information within your Elastic
deployment. The specific interface depends on how you [manage
users](workplace-search-security.html).

User mappings

A collection of mappings, where each maps a Dropbox user ID to a Workplace
Search username.

Store this data in a format that makes sense to you. You will need to
construct one or more API requests for each user mapping.

Content source IDs and access token

The string IDs of the Dropbox organization content sources within your
Workplace Search deployment, and your personal access token, which grants you
access to write external identities through the API.

See [Content source ID and access token](workplace-search-sources-document-
permissions.html#sources-permissions-content-source-id-token).

Then, send one API request per user mapping, per content source ID:

**Request template:**
    curl \
    --request 'POST' \
    --url '<WORKPLACE_SEARCH_BASE_URL>/api/ws/v1/sources/<CONTENT_SOURCE_ID>/external_identities' \
    --header 'Authorization: Bearer <ACCESS_TOKEN>' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "<WORKPLACE_SEARCH_USERNAME>",
        "source_user_id": "<DROPBOX_USER_EMAIL>"
    }'

**Example requests:**
    curl \
    --request 'POST' \
    --url 'http://localhost:3002/api/ws/v1/sources/40bd9d00713a5d9874444410/external_identities' \
    --header 'Authorization: Bearer 64c51eee12c1f7a3be8ab0ecf9a2184106c1641e49736119414da0c0e85f3611' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "john_doe",
        "source_user_id": "john.doe@example.com"
    }'
    curl \
    --request 'POST' \
    --url 'https://f3fae9ab3e4f423d9d345979331ef3a1.ent-search.us-east-1.aws.cloud.es.io:443/api/ws/v1/sources/8fda765d3e474d44e40369d6/external_identities' \
    --header 'Authorization: Bearer 7ea05c8bd50ab5c75d2b71adbcb9ae71c4034d7a4f8d6c16a8940510a951cec7' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "sam.foo",
        "source_user_id": "sam.foo@example.com"
    }'

#### Document-level permissions for
Google[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

Applies to: Google Drive

Use the [external identities API](workplace-search-external-identities-
api.html) to map Google user IDs to Workplace Search usernames for your Google
Drive organization content source.

First, gather the following information:

Google user IDs

The string IDs of the Google users that you’d like to map to Workplace Search
usernames. Google user IDs are email addresses. Example:
```sam.foo@example.com```.

See [View or export a group’s
members](https://support.google.com/a/answer/9772903?hl=en) in the Google
documentation for instructions to export all users.

Workplace Search usernames

The string usernames of the Workplace Search users to which you will map
Google user IDs. Example: ```sam_foo```.

Use the appropriate UI or API to locate this information within your Elastic
deployment. The specific interface depends on how you [manage
users](workplace-search-security.html).

User mappings

A collection of mappings, where each maps a Google user ID to a Workplace
Search username.

Store this data in a format that makes sense to you. You will need to
construct one or more API requests for each user mapping.

Content source IDs and access token

The string IDs of the Google Drive organization content sources within your
Workplace Search deployment, and your personal access token, which grants you
access to write external identities through the API.

See [Content source ID and access token](workplace-search-sources-document-
permissions.html#sources-permissions-content-source-id-token).

Then, send one API request per user mapping, per content source ID:

**Request template:**
    curl \
    --request 'POST' \
    --url '<WORKPLACE_SEARCH_BASE_URL>/api/ws/v1/sources/<CONTENT_SOURCE_ID>/external_identities' \
    --header 'Authorization: Bearer <ACCESS_TOKEN>' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "<WORKPLACE_SEARCH_USERNAME>",
        "source_user_id": "<GOOGLE_USER_ID>"
    }'

**Example requests:**
    curl \
    --request 'POST' \
    --url 'http://localhost:3002/api/ws/v1/sources/40bd9d00713a5d9874444410/external_identities' \
    --header 'Authorization: Bearer 64c51eee12c1f7a3be8ab0ecf9a2184106c1641e49736119414da0c0e85f3611' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "john_doe",
        "source_user_id": "john.doe@example.com"
    }'
    curl \
    --request 'POST' \
    --url 'https://f3fae9ab3e4f423d9d345979331ef3a1.ent-search.us-east-1.aws.cloud.es.io:443/api/ws/v1/sources/8fda765d3e474d44e40369d6/external_identities' \
    --header 'Authorization: Bearer 7ea05c8bd50ab5c75d2b71adbcb9ae71c4034d7a4f8d6c16a8940510a951cec7' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "sam.foo",
        "source_user_id": "sam.foo@example.com"
    }'

#### Document-level permissions for
Microsoft[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

Applies to: OneDrive, SharePoint Online

Use the [external identities API](workplace-search-external-identities-
api.html) to map user IDs from Microsoft Office 365 Groups to usernames from
Workplace Search for your OneDrive and SharePoint Online organization content
source.

First, gather the following information:

Microsoft Office 365 Groups user IDs

The string IDs of the Microsoft Office 365 Groups users that you’d like to map
to Workplace Search usernames. Each ID is an opaque string. Example:
```32ad7bda-3de1-4a77-ee97-f3476c2cf58d```.

To export user IDs, log in to your [Microsoft
Admin](https://admin.microsoft.com), then navigate to [Users](https://admin.mi
crosoft.com/Adminportal/Home?source=applauncher#/users). Select the users you
would like to export, and click **Export Users**.

Workplace Search usernames

The string usernames of the Workplace Search users to which you will map
Microsoft user IDs. Example: ```sam_foo```.

Use the appropriate UI or API to locate this information within your Elastic
deployment. The specific interface depends on how you [manage
users](workplace-search-security.html).

User mappings

A collection of mappings, where each maps a Microsoft user ID to a Workplace
Search username.

Store this data in a format that makes sense to you. You will need to
construct one or more API requests for each user mapping.

Content source IDs and access token

The string IDs of the OneDrive or SharePoint Online organization content
sources within your Workplace Search deployment, and your personal access
token, which grants you access to write external identities through the API.

See [Content source ID and access token](workplace-search-sources-document-
permissions.html#sources-permissions-content-source-id-token).

Then, send one API request per user mapping, per content source ID:

**Request template:**
    curl \
    --request 'POST' \
    --url '<WORKPLACE_SEARCH_BASE_URL>/api/ws/v1/sources/<CONTENT_SOURCE_ID>/external_identities' \
    --header 'Authorization: Bearer <ACCESS_TOKEN>' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "<WORKPLACE_SEARCH_USERNAME>",
        "source_user_id": "<MICROSOFT_USER_ID>"
    }'

**Example requests:**
    curl \
    --request 'POST' \
    --url 'http://localhost:3002/api/ws/v1/sources/40bd9d00713a5d9874444410/external_identities' \
    --header 'Authorization: Bearer 64c51eee12c1f7a3be8ab0ecf9a2184106c1641e49736119414da0c0e85f3611' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "john_doe",
        "source_user_id": "32ad7bda-3de1-4a77-ee97-f3476c2cf58d"
    }'
    curl \
    --request 'POST' \
    --url 'https://f3fae9ab3e4f423d9d345979331ef3a1.ent-search.us-east-1.aws.cloud.es.io:443/api/ws/v1/sources/8fda765d3e474d44e40369d6/external_identities' \
    --header 'Authorization: Bearer 7ea05c8bd50ab5c75d2b71adbcb9ae71c4034d7a4f8d6c16a8940510a951cec7' \
    --header 'Content-Type: application/json' \
    --data '{
        "user": "sam.foo",
        "source_user_id": "64bc9acd-5df2-5a88-ff98-a4496c2c568e"
    }'

**SharePoint Online notes:**

SharePoint Online has the concept of a "Members" group that SharePoint Online
manages itself. The API endpoints for the "Visitors" and "Owners" groups
within their grouping system cannot be accessed via API. Therefore, if you are
trying to grant access using those groups, it will not work — Workplace Search
cannot understand them. We recommend creating the equivalent groups in Office
365 Groups and use that to map instead.

### Custom sources[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

Custom sources allow you to ingest document access information using the
```_allow_permissions``` and ```_deny_permissions``` fields. For more
information, refer to [Custom API sources](workplace-search-custom-api-
sources.html) guide.

### Content source ID and access
token[edit](https://github.com/elastic/enterprise-search-
pubs/edit/7.15/workplace-search-docs/guides/permissions/sources-document-
permissions.asciidoc)

Each call to the external identities API must include the ID of the Workplace
Search content source and an access token that identifies the Workplace Search
user making the call.

Each of these is an opaque string, as in the following examples:

  * Source Identifier: ```8fda765d3e474d44e40369d6```. 
  * Access token: ```7ea05c8bd50ab5c75d2b71adbcb9ae71c4034d7a4f8d6c16a8940510a951cec7```. 

You can find this information in the Workplace Search administrative
dashboard, within the _Source overview_ of each content source.

  1. Within the Workplace Search dashboard menu, choose **Sources**. 
  2. Locate the row for the desired content source, and choose **Details**. 
  3. Within _Source overview_, locate _Document-level permissions_. 
  4. Toggle **Source Identifier** to expose the content source ID, and toggle **Access Token** to expose your personal access token.

![content source id access token](images/content-source-id-access-token.png)

* * *

Further reading:

  * [Enabling private content sources](workplace-search-enabling-private-sources.html)
  * [Document permissions for custom sources](workplace-search-document-permissions.html)
  * [External Identities API reference](workplace-search-external-identities-api.html)
  * _[Content sources_](workplace-search-content-sources.html)
  * [Custom API sources](workplace-search-custom-api-sources.html)

* * *

The following sections have moved:

_Organizational Sources and Private Sources_ → [Organizational Sources and
Private Sources](workplace-search-permissions.html#organizational-sources-
private-sources)

_Which strategy should I choose?_ → [Which strategy should I
choose?](workplace-search-permissions.html#permissions-strategy)

_Enabling private sources_ → [Enabling private content sources](workplace-
search-enabling-private-sources.html)

_Enabling Private Sources for Remote Content Sources_ → [Enabling private
sources for remote content sources](workplace-search-enabling-private-
sources.html#enabling-private-sources-remote)

_Enabling Private Sources for Standard Content Sources_ → [Enabling private
sources for standard content sources](workplace-search-enabling-private-
sources.html#enabling-private-sources-standard)

[« Permissions & Access Control](workplace-search-permissions.html) [Defining
Document Permissions for custom sources »](workplace-search-document-
permissions.html)

Most Popular

Video

[

Get Started with Elasticsearch

](https://www.elastic.co/webinars/getting-started-
elasticsearch?baymax=default&elektra=docs&storm=top-video)

Video

[

Intro to Kibana

](https://www.elastic.co/webinars/getting-started-
kibana?baymax=default&elektra=docs&storm=top-video)

Video

[

ELK for Logs & Metrics

](https://www.elastic.co/webinars/introduction-elk-
stack?baymax=default&elektra=docs&storm=top-video)