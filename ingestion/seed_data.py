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
    },
    {
        "doc_id": "doc_011",
        "title": "Task Dependencies and Milestones",
        "content": """Nexora lets you model complex work with task dependencies and milestones, giving your team a clear path to delivery. Dependencies define the order in which tasks must be completed, while milestones mark significant checkpoints or deliverables within a project.

To create a task dependency, open a task and click 'Add Dependency' in the right-hand panel. You can set either a 'Blocks' or 'Depends On' relationship. When task A blocks task B, task B cannot be started until task A is marked as done. Nexora automatically surfaces cascading delays: if a blocking task slips, downstream dependent tasks show an updated expected completion date with a warning badge.

Milestones are created from Project Settings under the 'Milestones' tab. Give the milestone a name, a target date, and optionally describe its acceptance criteria. You can link one or more tasks as 'Milestone Tasks'. Once all linked tasks are complete, the milestone automatically marks itself as reached and triggers a notification to project watchers.

Use the Timeline (Gantt) view to visualize dependencies and milestones together. Critical path tasks — those where a delay would push the entire project back — are highlighted in a distinct color. To adjust a dependency, simply drag the connector line between task bars in the Gantt view.

Best practices for dependencies: keep dependency chains shallow (ideally no deeper than three levels), always assign a concrete due date to dependency-driving tasks, and review the critical path each week. If you notice tasks stuck in 'Blocked' status, use the 'Blocked By' filter to identify which upstream task is the culprit.""",
        "source_url": "https://docs.nexora.com/dependencies-milestones",
        "metadata": {"category": "workflows", "priority": "medium"}
    },
    {
        "doc_id": "doc_012",
        "title": "Time Tracking and Reporting",
        "content": """Accurately tracking time is essential for understanding team capacity and project profitability. Nexora includes a built-in time tracking module and a flexible reporting engine so you can measure effort without leaving the platform.

To log time, open any task and navigate to the 'Time' tab. Click 'Add Time Entry', select the team member, enter the duration in hours and minutes, and optionally attach a note describing what was done. Time entries can also be started as timers from the task card or the global 'Start Timer' button in the top bar — the timer records elapsed time until you stop it.

Bulk time entry is available from the Gantt and List views. You can select multiple tasks and assign estimated hours, or drag the edge of a task bar on the Gantt to extend its planned duration. Nexora distinguishes between 'Estimated' time (planned) and 'Logged' time (actual), and shows variance in the reports.

The Reporting module, found under the Reports tab, offers several pre-built reports: Time by Project, Time by Member, Effort vs Estimate, and Utilization Rate. Every report can be filtered by date range, project, assignee, or task tag, and exported to CSV or PDF. You can also schedule a report to be emailed to you weekly or monthly.

Utilization is computed as logged hours divided by available hours for a selected period. High utilization (above 85%) may indicate over-allocation, while low utilization (below 50%) suggests capacity is available. Use these insights during sprint planning to balance workloads before assignments are locked in.""",
        "source_url": "https://docs.nexora.com/time-tracking",
        "metadata": {"category": "reporting", "priority": "medium"}
    },
    {
        "doc_id": "doc_013",
        "title": "Custom Fields and Task Metadata",
        "content": """Every team tracks slightly different data. Nexora's Custom Fields let you define your own metadata attached to tasks, projects, and milestones so your project management tool matches the way your team actually works.

To create a custom field, go to Project Settings and select the 'Custom Fields' tab. Click 'Add Field', choose a field type, and name it. Supported field types include Single Select, Multi Select, Number, Currency, Date, Date Range, Text, Long Text, Checkbox, Person, and URL. You can mark a field as required, which forces all new tasks to have a value, and set a default value shown on new tasks.

Fields defined at the project level apply to all tasks within that project. For organization-wide consistency, workspace admins can create 'Global Fields' under Organization Settings that apply across every project. A field can be added to task views by editing the List view columns or by selecting 'Customize Board' in the Board view and dragging the new field onto cards.

Custom fields are searchable and filterable just like standard fields. Use them to power automation, such as 'When Priority equals Critical, Then assign to the Engineering Lead'. They are also included in CSV/JSON exports, so your downstream reporting stays complete.

Example uses: a 'Severity' single-select field on bugs, a 'Client Account' person field for agency work, a 'Budget Remaining' currency field for project finance, and a 'Launch Date' date-range field for campaign planning.""",
        "source_url": "https://docs.nexora.com/custom-fields",
        "metadata": {"category": "workflows", "priority": "medium"}
    },
    {
        "doc_id": "doc_014",
        "title": "Mobile App for iOS and Android",
        "content": """Stay productive on the go with Nexora's mobile applications for iOS and Android. The mobile apps are designed for task management, quick updates, and staying notified — with full parity for reading and editing tasks, viewing boards, and logging time.

Download the official app from the Apple App Store or Google Play Store and sign in with your Nexora account. The first time you sign in, the app asks which workspaces to sync. You can switch between workspaces using the workspace switcher in the profile menu at the top right.

The mobile home screen shows your 'My Tasks', broken into sections: 'Overdue', 'Due Today', 'Due This Week', and 'Upcoming'. Tap any task to open its detail view, where you can edit the description, change status, add comments, attach photos from your device, or log time. Swipe actions let you quickly complete a task or mark it as in progress without opening the detail screen.

Push notifications mirror your desktop notification settings and arrive in real time. You can triage right from the lock screen — mark a task done, reply to a comment, or mute a thread. Offline mode is supported: changes you make while offline are queued and synchronized automatically once connectivity returns, with conflicts resolved by keeping the most recent edit.

To keep mobile and desktop in sync, ensure you are running the latest app version by enabling auto-update. If you encounter sync issues, toggle Airplane Mode on and off, or sign out and sign back in, which forces a full re-sync of your workspace data.""",
        "source_url": "https://docs.nexora.com/mobile",
        "metadata": {"category": "account", "priority": "medium"}
    },
    {
        "doc_id": "doc_015",
        "title": "User Roles and Permissions Reference",
        "content": """Nexora's permission system is built on four standard roles — Workspace Admin, Project Editor, Project Viewer, and Guest — plus flexible per-project overrides. Understanding each role's capabilities helps you configure secure and efficient workspaces.

Workspace Admin: Full control. Can manage billing, create and delete projects, configure integrations, edit organization settings, invite or remove members, assign roles, and access the admin audit log. This is the only role that can manage billing and workspace-level SSO.

Project Editor: Line-level power on projects they have access to. Can create, edit, delete tasks and subtasks, change statuses, manage milestones and dependencies, add comments, attach files, and log time. Cannot modify billing, organization settings, or other projects' access.

Project Viewer: Read-only. Can view tasks, boards, and reports; read descriptions and comments; and download attachments. Cannot edit fields, add comments, or log time. Suitable for stakeholders, executives, and cross-team collaborators who need visibility without write access.

Guest: Externally scoped. Can only access projects they are explicitly added to. Ideal for clients, contractors, and auditors. Guests cannot access project reports containing unshared data and cannot invite other members.

Per-Project Overrides: A member's global role can be elevated or reduced for a specific project via Project Settings → Access. For example, a global Project Viewer can be granted Editor rights on just one project. Overrides always take precedence over the global role within that project.

Ownership transfers, SCIM provisioning, and domain allow-listing are managed by Workspace Admins. For enterprise accounts, all permission changes are written to the admin audit trail for full compliance.""",
        "source_url": "https://docs.nexora.com/roles-reference",
        "metadata": {"category": "administration", "priority": "high"}
    },
    {
        "doc_id": "doc_016",
        "title": "Document and File Attachments",
        "content": """Nexora makes file collaboration simple with built-in attachments and document preview. You can attach files to tasks, comments, and milestones, and preview most common file types directly in the browser.

To attach a file to a task, open the task and click the paperclip icon in the top-right of the detail panel. You can drag-and-drop files from your desktop, paste images from the clipboard, or select from your device. Supported attachment types include images (PNG, JPG, GIF, SVG, WebP), documents (PDF, DOCX, XLSX, PPTX), and code files (with syntax highlighting in the previewer). Each task has a 5 GB per-file upload limit and a 50 GB total per-project storage allowance on paid plans.

Attachments support versioning. When you drop a new file with the same name onto an existing attachment, Nexora asks whether to add a new version or replace the current one. The version history is preserved, and you can compare or roll back to any prior version from the attachment menu.

Document previews support text search within PDFs and Office files, so you can quickly locate keywords without opening the original application. Comments made on a specific attachment using the 'Pin to file' action remain associated even if the file is later replaced with a new version.

Access control applies to attachments: Project Viewers can download files, and only Editors and above can upload or delete. Files deleted by mistake can be recovered from the Project Trash within 30 days. For data export, note that file attachments are packaged separately in a ZIP archive during full workspace exports.""",
        "source_url": "https://docs.nexora.com/attachments",
        "metadata": {"category": "workflows", "priority": "medium"}
    },
    {
        "doc_id": "doc_017",
        "title": "Single Sign-On and Enterprise Security",
        "content": """Nexora Enterprise plans support Single Sign-On (SSO) with SAML 2.0 and OIDC, granting your organization centralized, secure access control. This guide walks through enabling SSO, configuring suppliers like Okta or Azure AD, and enforcing security policies.

To enable SSO, go to Organization Settings → Security → Single Sign-On. Select your provider (Okta, Microsoft Entra ID, Google Workspace, or Any SAML 2.0). Click 'Configure' to begin the setup wizard. Nexora will provide a Metadata URL and SP entity ID that you paste into your identity provider, and you'll paste your provider's Metadata URL back into Nexora. Save once both sides are connected, and optionally enable 'Automatic Redirect' so members are sent to your identity provider when they visit the Nexora login page.

After enabling SSO, you can enforce 'SSO Only' mode, which disables password-based login for all members. Provisioning can be automated with SCIM 2.0, allowing user accounts and role assignments to be created and deactivated automatically as people join or leave your identity provider (IdP).

Additional enterprise security controls include: domain allow-listing (only accounts from approved domains can join), enforced Two-Factor Authentication (2FA) for all members, IP allow-listing for admin console access, and a comprehensive Admin Audit Log capturing sign-ins, permission changes, and configuration updates.

Troubleshooting SSO: if users see an authentication error, verify the user is provisioned in your IdP and that their email matches an allowed domain. If the login redirect loops, confirm the Metadata URLs were pasted correctly and that clocks on your SAML server and Nexora are in sync. Workspace Admins can temporarily grant password-based bypass for a specific user during an IdP outage.""",
        "source_url": "https://docs.nexora.com/sso-security",
        "metadata": {"category": "security", "priority": "high"}
    },
    {
        "doc_id": "doc_018",
        "title": "Guest Access for Clients and Contractors",
        "content": """Sharing projects with clients and external contractors is a common need, and Nexora's Guest access lets you collaborate with outside parties while keeping the rest of your workspace private.

Guests are externally-scoped users who can only see and interact with projects to which they are explicitly invited. Unlike regular members, guests consume no paid seat and cannot see your member directory, billing information, other projects, or organization settings.

To invite a guest, open the project you want to share and click 'Invite', then select 'Guest'. Enter the guest's email address; because guests do not have seats, they do not need to be pre-provisioned — sending the invitation creates their guest profile. The guest receives an email link and must accept the invitation. You can add a custom access note describing what they should be able to do.

By default, guests have viewer-like permissions on invited projects, but you can grant them Editor rights on a specific project through the project's Access settings. This is common for agencies where a client is expected to add comments and review work, or for contractors who need to update their own task statuses. Guest permissions can be revoked at any time, which immediately removes their access.

Security features for guests: guests see only their invited projects, guest activity is logged in the project activity feed, and workspace admins can audit all guest access. To share a link to a specific task or board, guests must be invited first — anonymous link sharing is not supported for security reasons. If a guest no longer works with you, remove them from the project to revoke their access instantly.""",
        "source_url": "https://docs.nexora.com/guest-access",
        "metadata": {"category": "account", "priority": "medium"}
    },
    {
        "doc_id": "doc_019",
        "title": "Automation Rules and Workflow Engine",
        "content": """Nexora's automation engine removes repetitive manual work by letting you define 'When-Then' rules that respond to project events. Automations help you enforce workflow consistency, accelerate handoffs, and reduce human error.

Creating an automation starts from Project Settings → Automations, or by clicking the Automation button on a board. Each rule has a Trigger ('When'), one or more Conditions, and one or more Actions ('Then'). Triggers include task status changes, task creation, due date changes, @mentions, comment additions, and custom field value changes.

Conditions let you scope a rule. For example: only trigger when a task's priority is 'High' and the assignee is in the 'Engineering' team. Actions include: changing a task status, assigning or unassigning a member, adding a label/tag, setting a due date, sending a notification, posting a Slack message, or creating a follow-up task.

Example rules: 'When a High priority bug moves to Done, Then notify the QA lead and tag it Verified.' Or 'When a task's due date passes and status is not Done, Then set status to At Risk and assign to the project manager.'

Automations run in near real time. Execution history is recorded in the Project Automation Log, where you can see which rules fired, when, and whether any action failed — along with the ability to re-run a failed action. You can enable or disable rules without deleting them, and rules support preview mode that shows what would have happened without executing.

To avoid infinite loops, Nexora prevents a rule from re-triggering itself indefinitely. There is a maximum of 100 active automation rules per project and 500 execution events per hour on Pro plans. If you exceed the limit, notifications are throttled until the next window.""",
        "source_url": "https://docs.nexora.com/automations",
        "metadata": {"category": "workflows", "priority": "medium"}
    },
    {
        "doc_id": "doc_020",
        "title": "Data Privacy and Compliance (GDPR)",
        "content": """Data privacy is a core commitment at Nexora, and our platform is designed to help your organization meet GDPR and other data-protection obligations. This document summarizes our data handling practices and the tools available to admins.

Nexora stores workspace data in encrypted-at-rest storage using AES-256, and data in transit is protected with TLS 1.2+ on all connections. Our data centers are hosted on major cloud providers in regions you select during workspace setup, allowing you to keep data within specific jurisdictions when required.

Under GDPR, you have rights to access, rectify, export, and delete personal data. Nexora provides tools to support these rights: personal data can be exported via the standard workspace export, and account deletion removes personal data within 30 days. Admins can also use Data Retention Policies (Enterprise) to define how long raw activity logs and deleted items are retained before automatic purging.

Processing purpose and data categories: Nexora processes user account data (name, email, role), task and activity data, and authentication logs solely to provide and secure the platform. We do not sell personal data. Subprocessors, including cloud infrastructure and email delivery providers, are listed in the public Subprocessors page.

For admins, the Data Management section lets you: run a full data audit, generate a Data Processing Agreement (DPA) attachment for your records, configure data residency, and set automated retention windows. Enterprise customers can request a signed DPA through the support portal.

To exercise a data-subject request, or to report a privacy concern, contact our Data Protection Officer at privacy@nexora.com. All requests are acknowledged within 48 hours and handled per our published SLA. We also publish a transparency report covering government data requests each year.""",
        "source_url": "https://docs.nexora.com/privacy-compliance",
        "metadata": {"category": "compliance", "priority": "high"}
    },
    {
        "doc_id": "doc_021",
        "title": "Keyboard Shortcuts and Productivity Tips",
        "content": """Master Nexora's keyboard shortcuts and hidden workflows to move through tasks dramatically faster. This reference lists the most useful shortcuts and lesser-known productivity tips.

Global shortcuts (click anywhere then press): 'N' creates a new task, 'C' opens quick capture, 'G then B' goes to the Board view, 'G then L' opens List view, 'G then T' jumps to the Timeline, and 'G then D' to the Dashboard. 'Cmd/Ctrl + K' opens the Command Palette, where you can search anything by typing. '?' shows the full shortcut reference at any time.

Within a task: 'E' edits the description, 'Tab' moves between fields, 'S' changes status, 'A' assigns a member, 'D' sets a due date, and 'X' opens the label picker. Pressing 'Esc' returns to the board.

Power tips: use drag-and-drop to change task status on the board, or select multiple tasks (Shift+Click) and perform bulk actions like assigning or changing status. Type 'tomorrow', 'eod', or 'next Friday' in the due date field for smart natural-language date parsing. Use '#' to reference a task by ID in any comment for a linked mention.

The Command Palette is extensible — type '/' anywhere to search commands, or '.' to search across all projects. You can also launch the palette and type the name of any team member to quickly assign them, or any tag to filter.

For maximum speed, combine shortcuts with automations and templates: nail down a repeatable process as a project template, and let automations handle status transitions and notifications so you can focus on the work itself.""",
        "source_url": "https://docs.nexora.com/shortcuts",
        "metadata": {"category": "productivity", "priority": "low"}
    },
    {
        "doc_id": "doc_022",
        "title": "Board, List, Timeline, and Calendar Views",
        "content": """Nexora presents your work through four primary views — Board, List, Timeline (Gantt), and Calendar — each suited to different workflows. Switching between them never loses or duplicates data; they are simply different lenses on the same tasks.

Board View: A Kanban-style layout with columns representing task statuses. Drag cards left or right to change status. Cards show assignee avatars, due dates, priority, and tags, and can be expanded inline. Great for managing flow and WIP limits.

List View: A spreadsheet-like grid with sortable, filterable columns. Choose which columns to show, including any custom fields. Ideal for bulk editing, sorting by due date or priority, and exporting filtered data. Group rows by status, assignee, project, or any custom field.

Timeline (Gantt) View: Visualizes tasks as horizontal bars along a time axis, including dependencies and milestones. Drag bar edges to adjust dates, and drag connector lines to create dependencies. The critical path is highlighted. Best for scheduling, capacity planning, and understanding start-to-finish sequencing.

Calendar View: Shows tasks as event blocks on a monthly, weekly, or daily calendar based on their due dates. Drag tasks to reschedule across days. Supports overtime display to spot when a day is over-allocated. Ideal for deadline-focused work and recurring deliverables.

All views support the same filtering, sorting, and saved views. A Saved View lets you persist a combination of filters and grouping under a name so teammates can open the same focused view in one click. Changes made in one view (e.g., status update on the Board) are immediately reflected in every other view.""",
        "source_url": "https://docs.nexora.com/views",
        "metadata": {"category": "workflows", "priority": "medium"}
    },
    {
        "doc_id": "doc_023",
        "title": "Webhooks and API Rate Limits",
        "content": """This technical reference detail the Nexora REST API and webhook behavior, focusing on authentication, rate limits, and error handling so you can build reliable integrations.

Authentication: Every API request must include an `Authorization: Bearer <personal_access_token>` header. Tokens are created in Developer Settings → API Tokens and scoped to read, write, or admin permissions. Never share tokens; rotate them periodically and revoke immediately if exposed.

Rate Limits: The Nexora API is rate-limited to 1,000 requests per hour per token (Pro) and 5,000 requests per hour per token (Enterprise), measured on a rolling window. When you exceed the limit, the API returns HTTP 429 with a `Retry-After` header specifying the seconds to wait. Respect this header and back off; ignoring it triggers progressively longer cooldowns.

Webhooks: Deliver real-time event notifications to your endpoint. Each webhook is signed with an HMAC-SHA256 signature using a per-webhook secret. Verify by computing the HMAC over the raw request body and comparing with the `X-Nexora-Signature` header to prevent tampering. Webhooks that fail (non-2xx response) are retried with exponential backoff up to 5 times over 24 hours, then disabled and flagged in the dashboard.

Events: Key event types include `task.created`, `task.updated`, `task.completed`, `comment.added`, `project.created`, and `milestone.reached`. Each payload contains a `type`, an `id`, `workspace_id`, `project_id`, and a nested `data` object with the affected entity.

Pagination & Errors: List endpoints return a cursor-based pagination object (`{ items, next_cursor }`). Use the cursor to fetch the next page. Standard error responses include a `code`, `message`, and `request_id` for support debugging. Idempotency keys can be supplied via the `Idempotency-Key` header on write endpoints to safely retry.""",
        "source_url": "https://docs.nexora.com/api-reference",
        "metadata": {"category": "developer", "priority": "high"}
    },
    {
        "doc_id": "doc_024",
        "title": "Security Best Practices and Account Protection",
        "content": """Protecting your Nexora account and workspace is a shared responsibility. This guide outlines the security best practices we recommend for every user and admin.

For individual users: enable Two-Factor Authentication (2FA) in My Settings → Security. Use a password manager to generate strong, unique passwords. Regularly review the list of active sessions under Security and revoke any you don't recognize. Never share your login credentials or personal access tokens.

For workspace admins: enforce 2FA for all members via Organization Settings → Security. Enable SSO Only mode if your organization uses an identity provider. Restrict membership to approved email domains using domain allow-listing. Review the Admin Audit Log weekly for unusual sign-ins or permission changes. Set short-lived sessions or token expiry policies where available.

Password policy: Nexora enforces a minimum of 12 characters and requires a mix of letters, numbers, and symbols for new passwords. Accounts that have been inactive for extended periods are flagged, and Workspace Admins can force a password rotation for any member.

Data protection: Encrypt any sensitive exports you download from the platform. Avoid storing API tokens or passwords in code, notes, or shared documents. When using webhooks, always verify the signature before processing the payload. Restrict API token scopes to the minimum needed and rotate them regularly.

Incident response: If you suspect your account has been compromised, immediately change your password, revoke active sessions, enable 2FA, and contact support. For a workspace-wide incident, admins can temporarily lock a member's account and review the audit log to determine scope. Our security team publishes advisories for any confirmed vulnerabilities.""" ,
        "source_url": "https://docs.nexora.com/security-best-practices",
        "metadata": {"category": "security", "priority": "high"}
    },
    {
        "doc_id": "doc_025",
        "title": "Pricing Plans Comparison and Upgrading",
        "content": """Nexora offers four plans — Free, Starter, Pro, and Enterprise — so you can choose the right tooling for your team's size and needs. This comparison helps you understand what each tier includes and how to upgrade.

Free: Up to 5 members, up to 3 active projects, List and Board views, basic task management, and 1 GB of attachment storage. Monthly and Annual billing available (annual saves 20%). Free plans include community support.

Starter: Unpriced per-seat, unlimited boards, Timeline and Calendar views, custom fields, 10 GB attachment storage, and email support. Suitable for small teams getting serious about project tracking.

Pro: Everything in Starter, plus Gantt-critical-path, task dependencies, unlimited guests, automation rules (up to 100), reporting and time tracking, API access, webhooks, and priority support. The most popular plan for growing teams. Adds advanced integrations with Slack, GitHub, and Jira.

Enterprise: Everything in Pro, plus SSO (SAML/OIDC), SCIM provisioning, enforced 2FA, IP allow-listing, data residency, automated retention policies, audit log, dedicated account manager, and contracted SLA with phone support. Custom pricing based on seat count.

Billing is per-seat based on active members. Guests are always free and do not count toward seats. Adding seats mid-cycle charges a prorated amount; removing seats takes effect at the next billing cycle. You can cancel or downgrade at any time from Billing Settings; paid access continues until the end of the current pre-paid period.

To upgrade, go to Billing Settings → Plans, select the desired tier, and confirm. Upgrades take effect immediately and advanced features unlock right away. We offer a 14-day money-back guarantee on annual renewals and a 30-day free trial of Pro for new accounts upgrading from Free.""",
        "source_url": "https://docs.nexora.com/pricing",
        "metadata": {"category": "billing", "priority": "high"}
    }
]
