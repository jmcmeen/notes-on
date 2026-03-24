# Introduction to Grafana

## Table of Contents

- [What is Grafana](#what-is-grafana)
- [Installation and Setup](#installation-and-setup)
- [Data Sources](#data-sources)
- [Dashboards](#dashboards)
- [Panel Types](#panel-types)
- [Queries](#queries)
- [Variables and Templating](#variables-and-templating)
- [Alerting](#alerting)
- [Annotations](#annotations)
- [Dashboard Provisioning](#dashboard-provisioning)
- [Organizations and Users](#organizations-and-users)
- [Grafana Loki for Logs](#grafana-loki-for-logs)
- [API Basics](#api-basics)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Grafana

Grafana is an open-source observability and data visualization platform. It connects to backends like Prometheus, InfluxDB, PostgreSQL, Elasticsearch, and Loki to render interactive dashboards and set up alerts. Grafana does not store data itself; it queries and visualizes data from external sources.

```bash
# Grafana default port: 3000
# Default credentials: admin / admin (change on first login)
# Configuration file: /etc/grafana/grafana.ini
```

---

## Installation and Setup

### Docker

```bash
# Run Grafana with persistent storage
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  -e "GF_SECURITY_ADMIN_PASSWORD=mysecretpassword" \
  grafana/grafana-oss:latest
```

### Docker Compose

```yaml
# docker-compose.yml - Grafana with Prometheus
version: "3.8"

services:
  grafana:
    image: grafana/grafana-oss:latest
    ports:
      - "3000:3000"                        # Web UI
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
      - ./provisioning:/etc/grafana/provisioning
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"                        # Prometheus UI
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

volumes:
  grafana-data:
```

### Installing with apt

```bash
# Add Grafana repository and install
sudo apt install -y apt-transport-https software-properties-common wget
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt update && sudo apt install grafana

# Start and enable
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

---

## Data Sources

### Prometheus

```yaml
# provisioning/datasources/prometheus.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy                # Grafana proxies requests to the backend
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: "15s"       # Default scrape interval
```

### Other Data Sources

```yaml
# InfluxDB, PostgreSQL, Elasticsearch, and Loki follow similar patterns
apiVersion: 1
datasources:
  - name: PostgreSQL
    type: postgres
    url: postgres-server:5432
    jsonData:
      database: app_metrics
      sslmode: disable
    secureJsonData:
      user: grafana_reader
      password: "secretpassword"

  - name: Loki
    type: loki
    url: http://loki:3100
    jsonData:
      maxLines: 1000

  - name: Elasticsearch
    type: elasticsearch
    url: http://elasticsearch:9200
    jsonData:
      index: "logs-*"
      timeField: "@timestamp"
```

---

## Dashboards

Dashboards consist of panels arranged in rows, with configurable time ranges and variables.

```bash
# Dashboards can be created via:
# 1. Grafana UI (Home > Dashboards > New)
# 2. JSON model imports
# 3. Provisioning from YAML/JSON files
# 4. The Grafana API
```

```yaml
# Dashboard best practices:
# - Use rows to group related panels
# - Set meaningful titles and descriptions on panels
# - Use variables for reusability across environments
# - Set appropriate refresh intervals
# - Use links to connect related dashboards
```

---

## Panel Types

### Time Series

```promql
# Default panel type for metrics over time

# CPU usage percentage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# HTTP request rate
rate(http_requests_total[5m])

# Memory usage percentage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

### Stat and Gauge

```promql
# Stat: single large number with optional sparkline
sum(active_users_total)                          # Total active users
(time() - process_start_time_seconds) / 3600     # Uptime in hours

# Gauge: value within a defined range (set min=0, max=100)
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100
```

### Bar Chart, Table, Heatmap, Logs

```promql
# Bar chart: categorical comparisons
topk(10, sum by (handler) (increase(http_requests_total[24h])))

# Table: detailed breakdowns
up{job="node-exporter"}

# Heatmap: distribution over time (latency histograms)
sum(increase(http_request_duration_seconds_bucket[5m])) by (le)
```

```bash
# Logs panel uses Loki or Elasticsearch
# Example LogQL: {job="myapp"} |= "error"
# With JSON parsing: {job="myapp"} | json | status >= 400
```

---

## Queries

### PromQL Basics

```promql
# Instant vector: current value
up{job="api-server"}

# Rate: per-second counter increase
rate(http_requests_total[5m])

# Aggregation
sum(rate(http_requests_total[5m]))                     # Total rate
sum by (status_code) (rate(http_requests_total[5m]))   # Grouped
avg by (instance) (node_cpu_seconds_total)              # Average
count(up == 1)                                          # Count up targets

# Error rate as percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# 95th percentile latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Comparison filtering
node_filesystem_avail_bytes < 1e9   # Less than 1GB free
```

### SQL Queries

```bash
# SQL data sources require columns named "time" and the metric value
# Example: SELECT created_at AS "time", count(*) AS "signups"
#          FROM users WHERE $__timeFilter(created_at)
#          GROUP BY time_bucket('1 hour', created_at) ORDER BY "time"

# Grafana macros for SQL:
# $__timeFrom()         - Start of time range
# $__timeTo()           - End of time range
# $__timeFilter(col)    - WHERE clause for time column
# $__timeGroup(col,'1h') - Group by interval
```

---

## Variables and Templating

Variables appear as dropdowns at the top of dashboards, making them interactive and reusable.

### Custom and Query Variables

```promql
# Custom variable (static values):
# Name: environment    Values: dev, staging, production

# Query variable (dynamic from data source):
label_values(up, instance)                         # All instance values
label_values(job)                                   # All job values
label_values(kube_pod_info{namespace="$namespace"}, pod)  # Filtered by another var
```

### Interval Variable

```yaml
# Interval variable for time-based grouping
# Name: interval
# Values: 1m, 5m, 15m, 30m, 1h, 6h, 12h, 1d
# Enable Auto option for automatic calculation
```

### Using Variables in Queries

```promql
# In PromQL queries
rate(http_requests_total{instance="$instance", job="$job"}[$interval])

# Multi-value variable (use regex match)
up{instance=~"$instance"}

# Variables also work in panel titles: "CPU Usage - $instance"
# And in text panels: "Dashboard for **$environment** environment"
```

---

## Alerting

### Alert Rules

```yaml
# Alert rule components:
# - Query:     Data to evaluate
# - Condition: When to fire (threshold, no data, etc.)
# - Duration:  How long condition must be true
# - Labels:    Categorize (severity, team)
# - Annotations: Context (summary, runbook URL)

# Example:
# Name: High CPU Usage
# Query: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
# Condition: IS ABOVE 80
# For: 5m
# Labels: severity=warning, team=infrastructure
# Annotations:
#   summary: "CPU above 80% on {{ $labels.instance }}"
#   runbook_url: "https://wiki.example.com/runbooks/high-cpu"
```

### Contact Points

```yaml
# provisioning/alerting/contactpoints.yml
apiVersion: 1
contactPoints:
  - orgId: 1
    name: slack-infra
    receivers:
      - uid: slack-receiver
        type: slack
        settings:
          url: "https://hooks.slack.com/services/T00/B00/XXXX"
          channel: "#infra-alerts"
          title: "{{ .Status | toUpper }} - {{ .CommonLabels.alertname }}"
```

### Notification Policies and Silences

```yaml
# provisioning/alerting/policies.yml
apiVersion: 1
policies:
  - orgId: 1
    receiver: slack-infra              # Default receiver
    group_by: [alertname, cluster]
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
      - receiver: pagerduty-critical   # Critical alerts to PagerDuty
        matchers:
          - severity = critical
      - receiver: slack-infra          # Warnings to Slack
        matchers:
          - severity = warning
```

```bash
# Create a silence for maintenance windows via the API
# POST /api/alertmanager/grafana/api/v2/silences with matchers,
# startsAt, endsAt, createdBy, and comment fields
# Silences can also be created through the Grafana UI under Alerting > Silences
```

---

## Annotations

Annotations mark events on graphs to correlate with metric changes (deployments, incidents).

```bash
# Add an annotation via API
curl -X POST http://localhost:3000/api/annotations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dashboardUID":"abc123","time":1711270800000,"text":"Deployed v2.4.1","tags":["deployment"]}'
```

---

## Dashboard Provisioning

Provisioning enables infrastructure-as-code for monitoring configuration.

### Data Source and Dashboard Provisioning

```yaml
# provisioning/datasources/datasources.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    isDefault: true
    editable: false               # Prevent UI changes
```

```yaml
# provisioning/dashboards/dashboards.yml
apiVersion: 1
providers:
  - name: "default"
    orgId: 1
    folder: "Provisioned"
    type: file
    updateIntervalSeconds: 30     # Check for changes every 30s
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

```bash
# Export a dashboard as JSON via API
curl -s "http://localhost:3000/api/dashboards/uid/YOUR_UID" \
  -H "Authorization: Bearer YOUR_API_KEY" | jq '.dashboard' > dashboard.json

# Place JSON files in the provisioned directory for auto-import
```

---

## Organizations and Users

```bash
# Grafana supports multi-tenancy through organizations
# Roles: Viewer (view only), Editor (create/edit), Admin (full org admin)

# Create an organization
curl -X POST http://localhost:3000/api/orgs \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Engineering Team"}'

# Add user to organization with a role
curl -X POST http://localhost:3000/api/orgs/1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"loginOrEmail": "alice", "role": "Editor"}'
```

---

## Grafana Loki for Logs

Loki is a log aggregation system that indexes labels rather than full content, making it cost-effective.

### LogQL Queries

```bash
# Basic log stream selection
# {job="myapp"}

# Filter by content
# {job="myapp"} |= "error"          # Contains "error"
# {job="myapp"} != "debug"          # Does NOT contain "debug"
# {job="myapp"} |~ "status=(4|5)\\d{2}"  # Regex match

# Parse and filter structured logs
# {job="myapp"} | json | level="error" | status >= 500

# Metric queries from logs
# rate({job="myapp"} |= "error" [5m])              # Errors per second
# sum by (level) (count_over_time({job="myapp"} | json [1h]))  # Count by level
```

### Promtail Configuration

```yaml
# promtail-config.yml - ships logs to Loki
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml     # Track read positions

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets: [localhost]
        labels:
          job: syslog
          __path__: /var/log/syslog

  - job_name: myapp
    static_configs:
      - targets: [localhost]
        labels:
          job: myapp
          environment: production
          __path__: /var/log/myapp/*.log
```

---

## API Basics

```bash
# Authentication: use API keys or basic auth
# Create API key via UI: Configuration > API Keys

# List all dashboards
curl -s http://localhost:3000/api/search \
  -H "Authorization: Bearer YOUR_API_KEY" | jq '.'

# Get a dashboard by UID
curl -s http://localhost:3000/api/dashboards/uid/abc123 \
  -H "Authorization: Bearer YOUR_API_KEY" | jq '.'

# Create or update a dashboard
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dashboard":{"title":"API Dashboard","panels":[]},"overwrite":false}'

# Delete a dashboard
curl -X DELETE http://localhost:3000/api/dashboards/uid/abc123 \
  -H "Authorization: Bearer YOUR_API_KEY"

# Health check (no auth)
curl -s http://localhost:3000/api/health | jq '.'

# List data sources
curl -s http://localhost:3000/api/datasources \
  -H "Authorization: Bearer YOUR_API_KEY" | jq '.'
```

---

## Practice Exercises

```bash
# Exercise 1: Deploy Grafana + Prometheus + Node Exporter with Docker Compose.
# Create a dashboard with CPU, memory, disk, and network panels.
# Add threshold colors (green < 60%, yellow < 80%, red >= 80%).

# Exercise 2: Instrument an application with Prometheus metrics.
# Create panels for request rate, error percentage, P95 latency,
# and top endpoints. Add instance and interval variables.

# Exercise 3: Deploy Loki + Promtail. Combine metrics and logs in one
# dashboard. Write LogQL to count errors/minute. Alert on high error rate.

# Exercise 4: Create alert rules for high CPU, low disk, and service down.
# Configure Slack contact point, notification policies by severity,
# and a silence for a maintenance window.

# Exercise 5: Export a dashboard as JSON, set up provisioning for data
# sources and dashboards, store in Git, and use the API to manage them.
```

---

## Summary

Grafana is a powerful observability platform unifying metrics, logs, and traces. Key concepts covered:

- **Installation**: Deploying with Docker or system packages.
- **Data Sources**: Connecting Prometheus, InfluxDB, PostgreSQL, Elasticsearch, and Loki.
- **Dashboards**: Creating visual representations with panels and rows.
- **Panel Types**: Time series, stat, gauge, bar chart, table, heatmap, and logs.
- **Queries**: Writing PromQL and SQL to fetch and transform data.
- **Variables**: Making dashboards interactive with template variables.
- **Alerting**: Rules, contact points, notification policies, and silences.
- **Provisioning**: Managing configuration as code.
- **Loki**: Log aggregation and querying with LogQL.
- **API**: Automating Grafana management programmatically.

---

## Next Steps

- Explore Grafana Tempo for distributed tracing.
- Learn Grafana Mimir for scalable long-term metrics storage.
- Study Grafana OnCall for incident management.
- Build custom Grafana plugins for specialized visualizations.
- Deploy Grafana on Kubernetes with Helm charts.
- Explore Grafana Cloud for a managed solution.

---

## Additional Resources

- [Grafana Official Documentation](https://grafana.com/docs/grafana/latest/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [PromQL Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [LogQL Documentation](https://grafana.com/docs/loki/latest/logql/)
- [Grafana Dashboard Library](https://grafana.com/grafana/dashboards/)
- [Grafana API Reference](https://grafana.com/docs/grafana/latest/developers/http_api/)
- [Grafana Community Forums](https://community.grafana.com/)
