SEED_DOCUMENTS = [
    {
        "doc_id": "doc_001",
        "title": "Getting Started with Nexora",
        "content": """Welcome to Nexora, the modern, collaborative project management platform designed to help high-performing teams plan, track, and execute work seamlessly. This guide will walk you through the essential onboarding steps to set up your account, organize your first workspace, and get your team running in minutes. 

First, let's understand the Nexora hierarchy. Everything starts with a Workspace, which acts as the umbrella container for your organization. Within a workspace, you can create multiple Projects to represent specific initiatives, departments, or client engagements. Inside each project, work is broken down into Tasks, Subtasks, and Milestones. Tasks hold all the contextual details, such as assignee, due date, description, attachments, and comments.

To begin, create your first project by clicking the '+' button next to the 'Projects' header in the left navigation sidebar. You can start from scratch or choose one of our curated templates. Once your project is created, you can customize the layout by switching between List, Board, Timeline (Gantt), and Calendar views. Each view provides a different perspective on your work to suit your workflow.

Next, add your team members to the project. Click the 'Invite' button in the top right corner of the screen, type their email addresses, and select their initial permission level. Once they accept the email invitation, they will appear in your workspace. You can then assign tasks to them and begin collaborating.

Communication is key. You can discuss tasks directly in the comment section at the bottom of every task card. Use '@mentions' to notify specific team members, or use custom tags to group related tasks across different projects. 

For monitoring progress, navigate to the Dashboard tab. Here, you can configure widgets to show key metrics, such as task completion rates, workload distribution, and upcoming milestones. If you need any assistance, click the '?' help icon in the bottom-left corner to access our resource library or message our active support channel. We are excited to help your team achieve their goals with Nexora!""",
        "source_url": "https://docs.nexora.com/getting-started",
        "metadata": {"category": "onboarding", "priority": "high"}
    },
    {
        "doc_id": "doc_002",
        "title": "Managing Team Members and Permissions",
        "content": """Managing team membership and setting precise access permissions is critical for maintaining data security and operational efficiency in Nexora. This document describes how administrators can add new members, edit user roles, transfer project ownership, and manage organization-wide permissions.

To add a new member to your team, navigate to the Organization Settings page, select the 'Members' tab, and click 'Invite Member'. Enter the email address of the invitee and choose their role. Nexora offers four distinct standard user roles: Workspace Admin, Project Editor, Project Viewer, and Guest. 
- Workspace Admins have full access to all projects, billing details, third-party integrations, and organization settings.
- Project Editors can create, modify, and delete tasks and projects, but cannot alter billing or workspace configurations.
- Project Viewers have read-only access. They can view tasks, read descriptions, and download attachments, but cannot edit fields or add comments.
- Guests are restricted users who can only see specific projects to which they are explicitly invited, ideal for external contractors or clients.

If you need to change a member's role, locate their name in the Members list, click the ellipsis (three dots) icon, and select 'Edit Permissions'. Select the new role from the dropdown menu and save changes. 

In addition to workspace-level roles, you can set custom overrides for individual projects. For example, a user who is a Project Viewer globally can be upgraded to a Project Editor on a specific project. To configure project overrides, go to the Project settings, select the 'Access' tab, and invite the user with the elevated permission.

Transferring project ownership is straightforward. If a project leader leaves the team, the current owner or a Workspace Admin can assign a new owner. Go to Project Settings, click 'Transfer Ownership', select the new owner, and confirm. 

For enterprise accounts, Nexora supports Single Sign-On (SSO) and automated user provisioning via SCIM. Admins can restrict email domains allowed to join the workspace, preventing unauthorized users from accessing company data. If you encounter any access control issues, consult the administrator activity log for a detailed audit trail of permission changes.""",
        "source_url": "https://docs.nexora.com/team-permissions",
        "metadata": {"category": "administration", "priority": "high"}
    },
    {
        "doc_id": "doc_003",
        "title": "Billing and Subscription Plans",
        "content": """Nexora offers flexible billing options and subscription plans tailored to teams of all sizes, from small startups to global enterprises. This guide outlines our plan tiers, billing cycles, accepted payment methods, and policies regarding subscription cancellations and refunds.

Nexora is available in three distinct pricing plans:
1. Starter Plan: Designed for small teams, providing access to essential task management features, list views, and basic integration options.
2. Pro Plan: Suited for growing organizations. Includes advanced features like Timeline (Gantt) charts, custom task dependencies, automated workflows, and unlimited guests.
3. Enterprise Plan: Crafted for large-scale operations requiring advanced security, Single Sign-On (SSO), SAML integration, custom data retention policies, and dedicated account support.

We offer both monthly and annual billing cycles. The annual billing option offers a discount of 20% compared to paying monthly. Billing is calculated on a per-seat basis. A seat represents any internal user added to your workspace. Guests are free and do not consume paid seats. If you add new team members during a billing cycle, your account will be charged a prorated amount for the remainder of that period. If you remove seats, the change will take effect at the start of your next billing cycle.

We accept all major credit cards, including Visa, Mastercard, American Express, and Discover. Enterprise customers can request invoicing with net-30 payment terms by contacting our accounts department.

You can cancel your subscription plan at any time. To cancel, navigate to Billing Settings, click 'Cancel Subscription', and follow the prompts. Upon cancellation, your workspace will remain active on the paid tier until the end of your current pre-paid billing period. After this date, your workspace will automatically downgrade to our Free plan, and advanced features will be locked.

Our refund policy is simple. If you cancel your plan within 14 days of your initial purchase or annual renewal, you are eligible for a full refund. To request a refund, please contact support with your invoice number. Refund requests received after 14 days will not be processed, but you will retain full access through your current billing term.""",
        "source_url": "https://docs.nexora.com/billing",
        "metadata": {"category": "billing", "priority": "high"}
    },
    {
        "doc_id": "doc_004",
        "title": "Integrations: Slack, GitHub, and Jira",
        "content": """Connecting Nexora with your team's favorite tools improves collaboration and keeps everyone aligned. Nexora supports robust, native integrations with Slack, GitHub, and Jira. This guide explains how to connect and configure these integrations to automate your development workflows.

To connect Slack, go to Organization Settings, select 'Integrations', and click 'Connect Slack'. You will be redirected to Slack's authorization screen. Once authorized, you can link specific Nexora projects to corresponding Slack channels. This integration allows you to receive instant notifications in Slack whenever a task is created, assigned, or completed in Nexora. You can also create tasks directly from Slack using the `/nexora create` slash command, or use message actions to convert a Slack message into a task.

For software development teams, the GitHub integration links code changes with project management. Go to the Integrations dashboard and click 'Connect GitHub'. Authorize Nexora to access your repositories. Once connected, you can reference task IDs in your Git commit messages or pull request descriptions using the format `NX-123` (where 123 is the task ID). Nexora will automatically detect the reference and attach the commit links or PR status directly to the corresponding task card. You can also configure rules to automatically transition task statuses, such as moving a task to 'In Review' when a PR is opened, and 'Done' when the PR is merged.

The Jira integration helps bridge the gap between product management and engineering. You can import Jira issues into Nexora or configure two-way syncing. Connect by entering your Jira instance URL and credentials. You can set up mapping rules so that updates to fields in Jira are immediately reflected in Nexora, and vice versa. This is useful for cross-functional teams where product managers plan in Nexora and developers execute in Jira.

If you experience integration disconnects, navigate to the specific integration settings page, click 'Reauthorize', and verify the connection tokens. Make sure your organization has not revoked third-party app permissions in Slack, GitHub, or Jira settings.""",
        "source_url": "https://docs.nexora.com/integrations",
        "metadata": {"category": "integrations", "priority": "medium"}
    },
    {
        "doc_id": "doc_005",
        "title": "Project Templates and Workflows",
        "content": """Standardizing processes across your team saves time and ensures consistent project delivery. Nexora offers pre-built templates and custom workflow capabilities to support different departments and methodologies. This document details how to create and manage templates, customize task statuses, and set up automations.

Nexora provides a variety of built-in templates, including Agile Software Development, Product Launch, Employee Onboarding, and Creative Design requests. To use a template, click 'New Project' and select a template from the gallery. Each template comes pre-configured with relevant task views, custom fields, and dummy tasks to guide your process.

If your team has a unique workflow, you can save any active project as a custom template. This allows you to duplicate the project structure, milestones, task descriptions, and dependencies for future initiatives. To save a project as a template, open the project menu, click 'Save as Template', name the template, and define which elements (such as assignees or attachments) should be cleared upon instantiation.

Workflows in Nexora are centered around task statuses. By default, projects use a simple 'To Do', 'In Progress', 'Done' workflow. However, you can create custom status columns to fit your cycle, such as 'Backlog', 'Design', 'QA Testing', or 'Blocked'. To customize statuses, go to Board View, click the '+' sign next to the last column, or click 'Edit Statuses' in Project Settings.

You can supercharge your workflows using Nexora's automation engine. Automations are built using simple 'When-Then' triggers. For example, you can create a rule: 'When task status transitions to QA Testing, Then assign the task to Sarah Jenkins and set due date to 3 days from today'. This removes manual coordination and accelerates handoffs.

Admins can manage organization-wide templates and lock critical workflows to prevent team members from altering approved status stages. If you need to troubleshoot an automation, check the Project Automation Log to see a history of triggered rules and any execution failures.""",
        "source_url": "https://docs.nexora.com/templates-workflows",
        "metadata": {"category": "workflows", "priority": "medium"}
    },
    {
        "doc_id": "doc_006",
        "title": "Notifications and Alert Settings",
        "content": """Nexora is designed to keep you updated on project progress without overwhelming your inbox. Our notification and alert management system gives you granular control over what updates you receive, when you receive them, and through which channels.

Nexora notifications are divided into three main channels:
1. In-App Notifications: Access these via the bell icon in the top right corner of the dashboard. In-app alerts track direct actions: task assignments, mentions in comments, and attachments added to tasks you watch.
2. Email Notifications: You can choose to receive individual email updates for key actions, or subscribe to a daily digest summarizing workspace activity.
3. Desktop & Mobile Push Notifications: Stay connected on the go with real-time push alerts from the desktop app or mobile applications.

To customize your notification settings, click your profile avatar in the bottom left, select 'My Settings', and go to the 'Notifications' tab. Here, you can toggles settings on and off for different triggers. For example, you can choose to receive email notifications only when you are directly '@mentioned', while turning off emails for general task modifications.

You can choose to 'watch' or 'unwatch' specific tasks. If you create a task or are assigned to it, you automatically become a watcher. Watchers receive notifications for all updates: comment additions, status changes, and due-date edits. If you want to stop receiving updates for a task, open the task details and click the 'Unwatch' button.

For teams that use Slack, notifications can be routed to channels or direct messages. Admins can configure Slack integrations to notify channels of general project milestones while keeping personal notifications on their local desktop.

If you are not receiving expected notifications, verify that your browser has granted permission for desktop notifications, check your spam folder for emails from `no-reply@nexora.com`, and ensure your status is not set to 'Do Not Disturb' (DND). DND mode silences all push and email alerts instantly.""",
        "source_url": "https://docs.nexora.com/notifications",
        "metadata": {"category": "account", "priority": "medium"}
    },
    {
        "doc_id": "doc_007",
        "title": "Data Export and Backup",
        "content": """Data ownership and security are core principles of Nexora. We ensure you have constant access to your workspace data and provide tools to perform manual backups, schedule automated exports, and recover deleted items.

Nexora workspace data can be exported in two formats: CSV (Comma-Separated Values) and JSON (JavaScript Object Notation). CSV exports are ideal for spreadsheets and custom reporting in Excel or Google Sheets. JSON exports contain the complete metadata structure of your workspace, including task hierarchies, comments, history logs, and user IDs, suitable for importing into other platforms.

To export your project data as CSV, open the project menu, click 'Export Project', and select 'CSV'. The export will download directly to your browser. To export an entire workspace, go to Organization Settings, select the 'Data Management' tab, and click 'Request Workspace Export'. Choose between CSV and JSON. Depending on the size of your workspace, compiling the archive may take some time. Once complete, you will receive an email containing a secure download link. The link expires after 7 days.

For Enterprise customers, Nexora supports automated daily backups. These backups can be automatically uploaded to an external storage location, such as an AWS S3 bucket or Google Cloud Storage, which is configured in the Admin console.

In addition to exports, Nexora maintains a Trash Bin for deleted projects and tasks. Items placed in the Trash Bin are kept for 30 days before being permanently deleted. During this 30-day window, any Project Editor or Workspace Admin can restore the item by opening the Trash tab, selecting the item, and clicking 'Restore'.

Please note that file attachments are excluded from the standard JSON/CSV text backups. Attachments are packaged separately in a ZIP archive during full workspace exports. If you need to recover data from a deleted user account, please contact security support for help with account context restoration.""",
        "source_url": "https://docs.nexora.com/data-export",
        "metadata": {"category": "administration", "priority": "medium"}
    },
    {
        "doc_id": "doc_008",
        "title": "Two-Factor Authentication Setup",
        "content": """Securing your company's project data is of paramount importance. Nexora supports Two-Factor Authentication (2FA) to add an extra layer of security to user logins. When enabled, 2FA requires both your password and a verification code from a mobile device to access your account.

To enable two-factor authentication for your account, follow these steps:
1. Click on your profile avatar in the bottom left corner of the screen and select 'My Settings'.
2. Navigate to the 'Security' tab and locate the 'Two-Factor Authentication' section.
3. Click the 'Enable 2FA' button. You will be prompted to re-enter your current password for security verification.
4. Nexora will display a QR code on the screen, along with a text-based secret key. Open your preferred authenticator app (such as Google Authenticator, Authy, or Microsoft Authenticator) on your mobile device and scan the QR code.
5. Once scanned, the app will generate a 6-digit verification code. Type this code into the input field in Nexora to confirm the setup and click 'Verify and Enable'.

Upon successful verification, Nexora will display a list of 10 emergency recovery codes. Store these recovery codes in a secure, offline location (such as a password manager or printed document). If you lose access to your mobile device, these codes are the only way to log back into your account. Each code can only be used once.

Administrators can enforce 2FA workspace-wide. When enabled, all workspace members will be forced to set up 2FA upon their next login attempt. If a user is locked out of their account due to a lost device and has lost their recovery codes, a Workspace Admin can temporarily disable 2FA for that specific account from the Members management page. Find the user, click 'Security Settings', and click 'Reset 2FA'. This action is logged in the admin audit history for compliance verification.""",
        "source_url": "https://docs.nexora.com/2fa-setup",
        "metadata": {"category": "security", "priority": "high"}
    },
    {
        "doc_id": "doc_009",
        "title": "API Access and Webhooks",
        "content": """Nexora provides a developer-friendly API and webhook system to allow teams to build custom tools, automate integrations, and sync data in real time. This technical guide describes how to generate personal access tokens, make API calls, and configure webhooks.

To authenticate your API requests, you must use a Personal Access Token (PAT). To generate a token, click your profile avatar, go to 'Developer Settings', and select the 'API Tokens' tab. Click 'Generate Token', name the token, and select its scope (read, write, or admin). Copy the generated token immediately; for security reasons, Nexora will never show it again. All API calls must include this token in the HTTP request header as: `Authorization: Bearer <your_token>`.

Our REST API exposes endpoints for all core entities. For example, to list tasks in a project, make a GET request to `https://api.nexora.com/v1/projects/{project_id}/tasks`. The API returns responses in JSON format. The API is rate-limited to 1,000 requests per hour per token. If you exceed this limit, the API will respond with HTTP Status Code 429 (Too Many Requests).

Webhooks allow Nexora to send real-time notifications to your system when specific events occur. To set up a webhook, navigate to Developer Settings, select the 'Webhooks' tab, and click 'Create Webhook'. Enter your destination URL and select which events should trigger the webhook (such as `task.created`, `task.updated`, or `comment.added`).

To ensure the security of webhook payloads, Nexora signs every request. When you create a webhook, you receive a secret signing key. Every webhook POST request includes a `X-Nexora-Signature` header, which is a HMAC-SHA256 signature of the request body using your secret key. Your receiving server should compute this signature and compare it with the header to verify the request originated from Nexora. Webhooks that fail to deliver (e.g. server returns HTTP 500) are retried 5 times before being disabled.""",
        "source_url": "https://docs.nexora.com/api-webhooks",
        "metadata": {"category": "developer", "priority": "medium"}
    },
    {
        "doc_id": "doc_010",
        "title": "Troubleshooting Common Errors",
        "content": """When developing integrations or using Nexora, you may occasionally encounter errors. This guide describes the most common errors, their causes, and how to resolve them.

1. HTTP 429 Rate Limit Exceeded:
This error occurs when your API requests exceed our limit of 1,000 requests per hour. The API will respond with HTTP 429 and include a `Retry-After` header indicating the number of seconds you must wait before making another request. To avoid this, implement caching in your client, optimize requests, or use webhooks instead of polling.

2. Webhook Validation Failure:
If you are setting up webhooks and they are failing validation, the most common cause is that your server is not responding with HTTP 200 during the initial handshake, or the HMAC-SHA256 signature calculations do not match. Verify that your server processes the signature matching using the raw byte payload before parsing it into JSON. 

3. SSO and Login Issues:
If a user cannot log in and sees an SSO authentication error, confirm that the user has been properly provisioned in your identity provider (IDP) and that their email matches the domain configured in Nexora settings. Workspace Admins can temporarily bypass SSO restrictions for specific users to allow password-based login during service disruptions.

4. Network Offline or Connection Loss:
Nexora relies on a persistent WebSocket connection to sync updates. If you see a red 'Connecting...' banner, check your network status. If you are behind a corporate proxy or firewall, ensure that WebSocket traffic (ws:// and wss:// protocols) is allowed on ports 80 and 443 for domain `*.nexora.com`.

If you experience unexpected UI behavior or cache inconsistency, we recommend clearing your browser data or using our Desktop app's 'Force Reload' option under the View menu. For persistent bugs, collect console logs and submit a support ticket.""",
        "source_url": "https://docs.nexora.com/troubleshooting",
        "metadata": {"category": "troubleshooting", "priority": "high"}
    }
]
