URL-Shortener service  

Objective 

The objective of this project was to design and implement a scalable, reliable URL shortening service similar to TinyURL or Bitly. The service aims to: 

    Convert long URLs into short, unique aliases. 

    Redirect users to the original URL when the short alias is accessed. 

    Handle high traffic efficiently using a cloud-native infrastructure. 

    Automate deployment and management using CI/CD pipelines and Kubernetes on AWS EKS. 

The system was built to ensure high availability, low latency, and scalability to support millions of URL shortening requests and redirections daily. 

 

Tools & Technologies Used 

    Infrastructure:  

    AWS EKS (Elastic Kubernetes Service): For container orchestration and cluster management. 

    Terraform: To provision and manage the EKS cluster and related AWS resources. 

    AWS ECR (Elastic Container Registry): To store Docker images for the application components. 

    CI/CD:  

    GitHub Actions: For automating the build, test, and deployment pipeline. 

    kubectl: To interact with the Kubernetes cluster and deploy manifests. 

    Application:  

    Backend: Python (or any preferred backend framework) for URL shortening logic and API endpoints. 

    Frontend: Python (or similar) for a simple user interface to input URLs and receive shortened links. 

    Database: PostgreSQL for persistent storage of URL mappings. 

    Docker: To containerize the backend, frontend, and database services. 

    Other Tools:  

    Git: For version control. 

    Nginx: As a reverse proxy/load balancer within the cluster. 

 

Architecture Overview 

The URL shortening service follows a microservices architecture deployed on an AWS EKS cluster: 



 +-------------------+       +-------------------+
|    Client (UI/API)| ----> | Load Balancer (ALB/Ingress) |
+-------------------+       +-------------------+
                              |
                              v
+-------------------+       +-------------------+
|  Shortener Service| <-->  |   PostgreSQL DB   |
| (Backend Pods)    |       | (Persistent Store)|
+-------------------+       +-------------------+
         |
         v
+-------------------+
|  Kubernetes (EKS) |
+-------------------+
         |
         v
+-------------------+
| Monitoring (Prometheus/Grafana) |
+-------------------+

    Client Layer: Users interact with the system via a web interface or API calls. 

    Load Balancer: An Nginx ingress controller distributes traffic across backend pods. 

    Backend Service: Handles URL shortening logic, generates unique aliases (e.g., using base62 encoding of an incremental ID), and stores mappings in the database. 

    Frontend Service: Provides a simple UI for users to input long URLs and retrieve shortened ones. 

    Database: PostgreSQL stores the mapping between short aliases and original URLs in a key-value structure. 

    EKS Cluster: Managed by Terraform, it hosts all services in Kubernetes pods, with auto-scaling enabled based on traffic load. 

The system is designed for horizontal scalability, with each component running in isolated pods that can scale independently. Data consistency is maintained through PostgreSQL, while Kubernetes ensures fault tolerance and high availability. 

 

Implementation Steps 

    Infrastructure Setup:  

    Created a Terraform configuration to define an EKS cluster with a managed node group (e.g., t3.medium instances). 

    Configured VPC, subnets, and security groups for network isolation and access control. 

    Applied Terraform scripts to provision the cluster (terraform apply). 

    Application Development:  

    Developed a backend service with two main endpoints:  

    POST /shorten: Takes a long URL and returns a short alias. 

    GET /{shortAlias}: Redirects to the original URL. 

    Built a minimal frontend with a form to submit URLs and display results. 

    Set up PostgreSQL with a table (urls) containing columns: id (auto-increment), short_alias, and original_url. 

    Containerization:  

    Created Dockerfiles for backend and frontend services. 

    Built and pushed images to AWS ECR. 

    Kubernetes Deployment:  

    Wrote Kubernetes manifests (deployments, services, ingress) for each component. 

    CI/CD Pipeline:  

    Set up a GitHub Actions workflow to:  

    Build and test the application on each push/PR. 

    Deploy services to EKS using kubectl. 

    Added verification steps to check pod status and service availability. 

    Testing and Validation:  

    Tested the service locally using Docker Compose. 

    Validated end-to-end functionality on EKS after deployment. 


 

 

Conclusion & Learnings 

The URL shortening service was successfully implemented and deployed on an AWS EKS cluster and CI/CD pipeline via GitHub Actions is in-progress. The system meets its objectives of scalability, reliability, and ease of use, capable of handling moderate traffic with room for further optimization. 

Key Learnings: 

    Infrastructure as Code (IaC): Terraform simplified cluster management and made infrastructure reproducible. 

    Kubernetes Power: EKS provided robust orchestration, auto-scaling, and fault tolerance out of the box. 

    CI/CD Automation: GitHub Actions streamlined the deployment process, reducing manual errors and deployment time. 

    Scalability Considerations: Early planning for database scalability (e.g., replication) is critical for high-traffic services. 

    Monitoring Needs(Not inplemented): Future iterations should include observability tools (e.g., Prometheus, Grafana) to monitor performance and detect issues proactively. 

This project demonstrated the power of combining modern DevOps practices with cloud-native technologies to build a production-ready service. Future enhancements could include custom alias support, analytics tracking, and rate limiting to prevent abuse. 

 
