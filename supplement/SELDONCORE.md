# Seldon Core 

## What is Seldon Core? 

Seldon Core is an open-source project that enables the deployment and serving of machine learning models on Kubernetes clusters. It provides a flexible and production-ready platform for serving real-time predictions and managing machine learning workflows in a scalable and efficient manner.

## Key Features

- **Scalability**: Seldon Core leverages Kubernetes to provide horizontal scalability, enabling the deployment of machine learning models on distributed clusters and handling high workloads efficiently.

- **Multi-Framework Support**: Seldon Core supports various machine learning frameworks, including TensorFlow, PyTorch, XGBoost, Scikit-learn, and more, allowing you to deploy models trained using your preferred framework.

- **RESTful API Endpoints**: Seldon Core automatically exposes machine learning models as RESTful API endpoints, making it easy to integrate predictions into your applications and services.

- **A/B Testing & Canary Deployments**: With Seldon Core, you can easily perform A/B testing and canary deployments of machine learning models, enabling you to experiment with different models and configurations seamlessly.

- **Monitoring and Metrics**: Seldon Core provides built-in monitoring and metrics, allowing you to gain insights into the performance and health of your deployed models.

- **Explainability**: Seldon Core includes support for model explainability techniques, helping you understand the reasons behind model predictions.

## How Does Seldon Core Work?

Seldon Core is designed to be deployed on Kubernetes clusters and consists of several components:

1. **Seldon Deployment Engine**: This component manages the lifecycle of machine learning models and handles model deployment, scaling, and monitoring.

2. **Model Servers**: Seldon Core utilizes model servers to serve predictions from deployed models through RESTful API endpoints.

3. **Model Adapters**: Model adapters allow Seldon Core to interface with various machine learning frameworks, enabling compatibility with a wide range of models.

4. **Explainers**: Seldon Core provides explainers that produce explanations for model predictions, making the AI/ML decision-making process more transparent and interpretable.

## Getting Started

To get started with Seldon Core, you can follow the installation and setup instructions in the [official documentation](https://github.com/SeldonIO/seldon-core).

## Documentation

Comprehensive documentation, including installation guides, tutorials, and API references, can be found in the [Seldon Core documentation](https://docs.seldon.io/projects/seldon-core/en/latest/).
