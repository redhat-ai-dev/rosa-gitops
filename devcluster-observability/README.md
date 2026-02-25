# DevCluster Observability GitOps

This gitops project manages the observability for:

- Openshift AI Deployed models.
- Red Hat Developer Hub deployments.

## Grafana

- Managed by the [Grafana Operator](https://github.com/grafana/grafana-operator)
- Runs in `devcluster-monitoring` namespace
- Dashboards are declared as `GrafanaDashboard` CRDs
- Prometheus datasources are configured via `GrafanaDatasource` CRDs

Available Dashboards are:

- RHOAI Models Registry (Observability on RHOAI deployed models for RHDH AI DevCluster)
- RHDH AI Rolling Demo

## Alerts

Alerts are set via `PrometheusRule` and routed through `AlertmanagerConfig` directly to a Slack App Incoming Webhook.

Alert notifications include the alert title, summary, description, and severity. Resolved alerts are also sent.

Available alerts are:

- **VllmPodNotReady** (critical, `vllm` namespace) — fires when any pod in the `vllm` namespace is stuck in Pending or Failed phase for more than 1 hour
- **RollingDemoPodNotReady** (critical, `rolling-demo-ns` namespace) — fires when any pod in the `rolling-demo-ns` namespace is stuck in Pending or Failed phase for more than 1 hour

## Required Pre-existing Secrets

These Secrets are NOT managed by this repo and must exist before Argo CD sync:

### Grafana

```
devcluster-monitoring/grafana-admin
```

Keys:

- `username`
- `password`

### Keycloak OAuth

```
devcluster-monitoring/keycloak-secrets
```

Keys:

- `grafana_url` — the public Grafana route URL (e.g. `https://grafana-devcluster-monitoring.apps.<cluster>`)
- `client_id`
- `client_secret`
- `auth_url` — the Keycloak authorization endpoint (`https://<KEYCLOAK_HOST>/realms/<REALM>/protocol/openid-connect/auth`)
- `token_url` — the Keycloak token endpoint (`https://<KEYCLOAK_HOST>/realms/<REALM>/protocol/openid-connect/token`)
- `api_url` — the Keycloak userinfo endpoint (`https://<KEYCLOAK_HOST>/realms/<REALM>/protocol/openid-connect/userinfo`)

### Slack App Webhook

The Slack webhook secret must exist in every namespace that has an `AlertmanagerConfig`:

```
vllm/webhook-secret
rolling-demo-ns/webhook-secret
```

Keys:

- `webhook-url` — the Slack App Incoming Webhook URL (e.g. `https://hooks.slack.com/services/...`)

## Installation

1. Ensure the **Grafana Operator** and **Prometheus Operator** are installed on the cluster.
2. Ensure the `devcluster-monitoring`, `vllm`, `rolling-demo-ns` namespaces already exist in your cluster.
3. Enable **user-workload monitoring** on the cluster (required for ServiceMonitor scraping in user namespaces):
   ```bash
   oc apply -f - <<EOF
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: cluster-monitoring-config
     namespace: openshift-monitoring
   data:
     config.yaml: |
       enableUserWorkload: true
   EOF
   ```
4. Enable **user-workload Alertmanager** (required for `AlertmanagerConfig` routing to Slack):
   ```bash
   oc apply -f - <<EOF
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: user-workload-monitoring-config
     namespace: openshift-user-workload-monitoring
   data:
     config.yaml: |
       alertmanager:
         enabled: true
         enableAlertmanagerConfig: true
       prometheus:
         logLevel: debug
         retention: 15d
   EOF
   ```
5. Create the **webhook-secret** for Slack alerting in each alerting namespace:
   ```bash
   WEBHOOK_URL='https://hooks.slack.com/services/YOUR/APP/WEBHOOK'
   oc create secret generic webhook-secret -n vllm --from-literal=webhook-url="$WEBHOOK_URL"
   oc create secret generic webhook-secret -n rolling-demo-ns --from-literal=webhook-url="$WEBHOOK_URL"
   ```
6. Create the **grafana-admin** to store your admin's credentials:
   ```bash
   USERNAME='your-admins-username'
   PASSWORD='your-admins-password'
   oc create secret generic grafana-admin -n devcluster-monitoring --from-literal=username="$USERNAME" --from-literal=password="$PASSWORD"
   ```
7. Create the **keycloak-secrets** for Grafana OAuth integration with Keycloak:
   ```bash
   GRAFANA_URL='https://grafana-devcluster-monitoring.apps.<cluster>'
   KEYCLOAK_HOST='your-keycloak-host'
   REALM='your-realm'
   oc create secret generic keycloak-secrets -n devcluster-monitoring \
     --from-literal=grafana_url="${GRAFANA_URL}" \
     --from-literal=client_id="your-client-id" \
     --from-literal=client_secret="your-client-secret" \
     --from-literal=auth_url="https://${KEYCLOAK_HOST}/realms/${REALM}/protocol/openid-connect/auth" \
     --from-literal=token_url="https://${KEYCLOAK_HOST}/realms/${REALM}/protocol/openid-connect/token" \
     --from-literal=api_url="https://${KEYCLOAK_HOST}/realms/${REALM}/protocol/openid-connect/userinfo"
   ```
   > **Note:** Users are auto-provisioned as `Viewer` on their first Red Hat SSO login. Role promotion (Editor, Admin) must be done manually by a Grafana admin.
8. Apply Argo CD Project + Application from `argocd/`

## Contributions

Contributions are welcomed in the repo. Feel free to open a PR.
