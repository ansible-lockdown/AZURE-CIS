Azure Foundations CIS
================
Configure Azure Tenant to be [CIS](https://www.cisecurity.org/cis-benchmarks/) compliant

Based on [CIS Microsoft Azure Foundations Benchmark 1.2.0 ](https://workbench.cisecurity.org/benchmarks/1408)

Caution(s)
-------
This role **will make changes to the subscription** which may have unintended concequences. This is not an auditing tool but rather a remediation tool to be used after an audit has been conducted.

This role was developed against a new Azure Tenant and subscription. If you are implimenting to an existing tenant and subscription(s) please review this role for any site specific changes that are needed.

To use release version please point to main branch

Additional costs may be incured for specific features
- 1.2.1 | To create custom roles, your organization needs Azure AD Premium P1 or P2
- 2.9   | Azure Defender
- 4.2.1 | Azure Defender for SQL costs 15 USD/server/month. It includes Vulnerability Assessment and Advanced Threat Protection.
- 5.1.4 | KeyVault transactions
- 6.4   | Storage Accounts used for storing logss
- 7.6   | Endpoint Protection


Documentation
------------
[Activity Log Alerts](https://docs.microsoft.com/en-us/rest/api/monitor/activitylogalerts/createorupdate#actionlist)


Requirements
------------
- RHEL 8 or CentOS 8 to execute the playbook/role
- Azure Tenant and subscription
  - A Service Principle with the following access:
    - Read role at the subscription level
    - SECTION 1 App Registration needs GraphAPI permission "User.Read.All"
    - SECTION 3 Service Principal requires Contributor role
    - SECTION 8 Access Policy required to allow Service Principal to list keys and secrets
      - [Assign Access Policy](https://docs.microsoft.com/en-us/azure/key-vault/general/assign-access-policy-portal)

Dependencies
------------
- Python3
- Ansible 2.9+
- Azure CLI 2.23+
- PowerShell Core 7.1.3+
  - Az.Accounts Module 2.3.0
  - Az.SQL Module 3.1.0

Known Issues
------------
- 2.9
  - ⚠ The evidence query returns an empty array because no value exists where name = WDATP, but it appears that the PATCH tasks does work
- 2.10
  - ⚠ The evidence query returns an empty array because no value exists where name = MCAS, but it appears that the PATCH tasks does work
- 3.3, 3.5, 3.10, 3.11
  - PATCH
    - 🔩HIGH COMPLEXITY. Need to add the storage account name and account_key to the storage container JSON
- 3.5
  - PATCH
    - 3.6 will break this
- 4.2.5
  - PATCH
    - ⚠ Update-AzSqlServerVulnerabilityAssessmentSetting: The provided storage account shared access signature or account storage key is not valid.
- 4.5
  - PATCH
    - ⚠ Despite being the correct syntax, this command does not seem to work: "The requested server key was not found."
- 5.1.2
  - PATCH
    - 🔩HIGH COMPLEXITY. Requires creating resources. CIS example uses PowerShell using ARM templates.
      - Resource Group (if it doesn't exist already)
      - [Microsoft.OperationalInsights/workspaces](https://docs.microsoft.com/en-us/azure/templates/microsoft.operationalinsights/workspaces?tabs=json) (if it doesn't already exist)
      - [microsoft.insights/diagnosticSettings](https://docs.microsoft.com/en-us/azure/templates/microsoft.insights/diagnosticsettings) (if it doesn't already exist)
- 5.1.3
  - PATCH
    - 3.6 will break this
    - 🔩HIGH COMPLEXITY. Need to understand how to determine the storage account
      - The object insights_operational_logs_storage_container_list contains the storage container, but not the storage account. Need to find a way to get the storage account, or use id
- 5.1.4
  - PATCH
    - 🔩HIGH COMPLEXITY. Need to understand how to determine the storage account
- 6.1
  - 🔩HIGH COMPLEXITY. Did not implement search for port 3389 in a destinationPortRange (i.e. "3388-3390")
- 6.2
  - 🔩HIGH COMPLEXITY. Did not implement search for port 22 in a destinationPortRange (i.e. "21-23")
- 6.4 Ensure Network Watcher is provisioned for region or will receive "ERROR: network watcher is not enabled for region 'westus'." See 6.5
- 7.4
  - 🔩HIGH COMPLEXITY. Need to add an array variable with a list of approved extensions, then loop through the array to compare with the extensions found.
- 7.6
  - 🔩HIGH COMPLEXITY. Need to add an array variable with a list of possible endpoint protection values, then loop through the array to compare with the extensions found.
- 9.4
  - PATCH
    - ⚠ ERROR: Operation returned an invalid status 