# Flask API with Docker and Kubernetes Deployment

This is a sample Flask API that is containerized using Docker and can be automatically deployed to a Kubernetes cluster using GitHub Actions.

## Prerequisites

- Docker installed locally (for building and testing the image)
- Access to a Kubernetes cluster
- `kubectl` command-line tool configured to interact with your cluster
- A Docker Hub account (or another container registry)

## Application Details

-   **API Endpoint**: `GET /` returns `{"message": "Hello, World!"}`
-   **Application Port**: The application inside the container runs on port 5000 (configurable via the `PORT` environment variable in the Dockerfile).

## Local Docker Build & Run

1.  **Build the Docker image:**
    ```bash
    docker build -t your-docker-username/my-flask-app:latest .
    ```
    (Replace `your-docker-username` with your Docker Hub username or your preferred image name).

2.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 your-docker-username/my-flask-app:latest
    ```
    The API should then be accessible at `http://localhost:5000/`.

## Kubernetes Deployment via GitHub Actions

The GitHub Actions workflow in `.github/workflows/main.yml` will automate the build and deployment process.

### Required GitHub Secrets

To enable the workflow, you need to configure the following secrets in your GitHub repository settings (`Settings > Secrets and variables > Actions`):

1.  `DOCKER_USERNAME`: Your Docker Hub username.
2.  `DOCKER_PASSWORD`: Your Docker Hub password or access token.
3.  `KUBE_CONFIG_DATA`: Base64 encoded string of your Kubernetes configuration file (`kubeconfig`). You can typically get this by running:
    ```bash
    cat ~/.kube/config | base64 -w 0
    ```
    **Security Note**: Ensure your `kubeconfig` has appropriate permissions for the deployment. It's recommended to use a service account with limited permissions rather than a personal admin `kubeconfig`.

### Workflow Steps

1.  **Trigger**: Pushes to the `main` branch.
2.  **Build & Push Image**: The workflow builds the Docker image and pushes it to Docker Hub, tagged with your `DOCKER_USERNAME` and the GitHub SHA (e.g., `your-docker-username/my-flask-app:commit-sha`).
    *   **Note**: The image name in the workflow is `my-flask-app`. If you change this in the `.github/workflows/main.yml` file, ensure your Kubernetes deployment manifest (`k8s/deployment.yaml`) and local build commands reflect this change if necessary. The workflow automatically updates the image tag in `k8s/deployment.yaml` before applying it.
3.  **Deploy to Kubernetes**: The workflow uses `kubectl` to apply the manifest files located in the `k8s/` directory (`deployment.yaml` and `service.yaml`).

### Accessing the Deployed Application

Once deployed, the method to access the application depends on your Kubernetes environment and the type of service used (`LoadBalancer` in the provided `service.yaml`).

-   If you are using a cloud provider with LoadBalancer support, it will provision an external IP address for the `flask-api-service`. You can find this IP by running:
    ```bash
    kubectl get svc flask-api-service
    ```
    Look for the `EXTERNAL-IP`. The application will be accessible at `http://<EXTERNAL-IP>:80/`.
-   If `LoadBalancer` is not supported or you are in a local environment (like Minikube), you might need to use `kubectl port-forward` or change the service type to `NodePort`. For `NodePort`, you would access it via `<NodeIP>:<NodePort>`.

## Kubernetes Manifests

The Kubernetes configuration files are located in the `k8s/` directory:
-   `deployment.yaml`: Defines the desired state for your application, including the number of replicas and the container image to use.
-   `service.yaml`: Exposes your application as a network service.
