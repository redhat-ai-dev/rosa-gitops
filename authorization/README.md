# authorization

> [!IMPORTANT]  
> Before adding a new group or rolebinding to the cluster, you **must** reach out to one of the cluster admins on Slack first.

> [!NOTE]  
> Adding your username to one of the `Group`s managed by this ArgoCD application does **not** create your username or grant access to the cluster. You must already have an internal SSO login in order for these role bindings to take effect.

Membership in the `redhat-ai-dev-users` `Group` on the cluster grants cluster-wide `edit` permissions. Additional permissions can be configured via additional `Group` and `RoleBinding` resources.