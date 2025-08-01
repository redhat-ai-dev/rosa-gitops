# authorization

> [!IMPORTANT]  
> Before adding a new group or rolebinding to the cluster, you **must** reach out to the cluster admins on Slack first (handle: `rhdh-cluster-admins`).

> [!NOTE]  
> Adding your username to one of the `Group`s managed by this ArgoCD application does **not** create your username or grant access to the cluster. You must already have an internal SSO login in order for these role bindings to take effect.

Membership in under the listed `Group` entities provides the corresponding permissions: 

- `redhat-ai-dev-view-users` - grants cluster-wide `view` permissions
- `redhat-ai-dev-edit-users` - grants cluster-wide `edit` permissions
- `rhoai-workspace-edit-users` - grants `edit` permissions to the `rhoai-workspace` namespace 

Additional permissions can be configured via additional `Group` and `RoleBinding` resources.