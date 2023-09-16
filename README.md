1. **Telemetry Code Integration**: 
    - A dictionary named `telemetry_data` was added to store metrics related to the number of requests and their response times for each endpoint.
    - The `telemetry_decorator` function was introduced. This decorator collects metrics for each Flask route it's applied to. It increments the request count and aggregates the response time for the endpoint.
    
2. **Metrics Endpoint**:
    - A new Flask route, `/metrics`, was added. This endpoint exposes the collected metrics in the Prometheus exposition format. When accessed, it provides metrics data for each decorated Flask route.

3. **Decorator Application**:
    - The `telemetry_decorator` was applied to the original Flask routes (`/`, `/add`, and `/update`). This enables the collection of metrics for these endpoints.

### Usage:

1. **Set Up the Flask Environment**:
    ```bash
    # Set up the Flask environment variables
    export FLASK_APP=app.py
    export FLASK_ENV=development

    # Run the Flask application
    flask run
    ```

   ```
   flask shell
   ```

   ```python
   from app import db
   db.create_all()
   ```

2. **Test the Endpoints**:
    - **Main Page (GET request to `/`)**:
        ```bash
        curl http://127.0.0.1:5000/
        ```
    - **Add a To-Do Item (POST request to `/add`)**:
        ```bash
        curl -X POST -d "todo_item=Sample Task" http://127.0.0.1:5000/add
        ```
    - **Trigger the Update Endpoint (POST request to `/update`)**:
        ```bash
        curl -X POST http://127.0.0.1:5000/update
        ```

3. **View Telemetry Data in Prometheus Format**:
    ```bash
    curl http://127.0.0.1:5000/metrics
    ```

### Summary:

The Flask application has been enhanced with telemetry capabilities. The integrated telemetry code collects data about the number of requests and their response times for each of the Flask routes. This data is then exposed via the `/metrics` endpoint in a format that can be scraped and understood by Prometheus, a popular open-source monitoring system. With this setup, you can monitor the performance and usage of your Flask application using Prometheus and related tools.


 **PS Telemetry Code Integration**: 

### 1. Setting Up Prometheus:

**a.** Download and install Prometheus for your platform from the [official Prometheus downloads page](https://prometheus.io/download/).

**b.** Create a configuration file for Prometheus, say `prometheus.yml`, with the following content:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask_app'
    static_configs:
      - targets: ['localhost:5000']
```

The above configuration tells Prometheus to scrape the metrics from your Flask app every 15 seconds.

**c.** Start Prometheus using the configuration file:

```bash
prometheus --config.file=prometheus.yml
```

Prometheus will start and by default will be accessible at `http://localhost:9090`.

### 2. Visualizing Metrics:

**a.** Open a web browser and navigate to `http://localhost:9090`.

**b.** You can enter your metric names (like `_get_requests_total` or `add_post_requests_total`) in the "Expression" input box and click "Execute" to see the raw metrics.

### 3. Setting Up Grafana for Advanced Visualization:

For more advanced visualizations, Grafana is a popular choice that integrates well with Prometheus.

**a.** Download and install Grafana from the [official Grafana downloads page](https://grafana.com/grafana/download).

**b.** Start Grafana. Depending on your platform, this can be as simple as running the `grafana-server` command or using a service manager like `systemd`.

**c.** Open Grafana in a web browser (by default, it's at `http://localhost:3000`). The default login is `admin`/`admin`.

**d.** Add Prometheus as a data source:
   - Click on the gear icon (⚙️) on the left sidebar.
   - Click on "Data Sources."
   - Click "Add data source" and choose Prometheus.
   - Set the URL to `http://localhost:9090` (Prometheus's default address) and click "Save & Test."

**e.** Create a dashboard and add panels to visualize your metrics. When adding queries to your panels, you can use the metric names from your Flask application.
