# Batch Processing News Headline Text

This project automates the extraction, processing, and visualization of BBC news headlines. It consists of two components:
1. Data pipeline: A batch job that scrapes, cleans, and stores news headlines daily for visualisation
2. CI/CD Deployment pipeline: Automates the deployment of Docker containers to an AWS EC2 instance using Github Actions

#### Data Pipeline
- Data Extraction and Cleaning
    - Scraping: Extract headline text from BBC website 
    - Data Cleaning: Processes text data to remove stopwords and perform tokenisation
    - Storage: Write the cleaned data to PostgreSQL database
- Scheduling with Cron
    -  A cron job is configured within the backend Docker container to perform data extraction and cleaning daily, and setup during the container's startup
- Data Visualisation
    - A Streamlit dashboard reads data from the PostgreSQL database
    - It shows a wordcloud of the most common keywords and the corresponding news headline text

<img src = "./images/data_pipeline.png" width="50%" height="50%">

#### CI/CD Deployment Pipeline

- The components are dockerised and built into images that are pushed to Docker Hub
- An AWS EC2 instance pulls that latest images and runs them using Docker Compose

<img src = "./images/cicd_pipeline.png" width="50%" height="50%">

#### Running the project
- Configure the following Github secrets to automate deployment to AWS EC2. 

| Name               | Description                                                 |
|--------------------|-------------------------------------------------------------|
| `DOCKER_USER`  | Docker Hub username                                             |
| `DOCKER_PASSWORD`  | Docker Hub password or access token                         |                 
| `EC2_INSTANCE_IP`  | Public IP of the EC2 instance                               |
| `PASSWORD`  | Base64-encoded **private SSH key** for EC2 access                  |
- Alternatively, run the full pipeline with the following command for local development
```
docker-compose up --build -d
```

- To view the dashboard, go to 
    - ```http://<your-ec2-public-ip>:8501``` for deployment to AWS EC2
    - ```http://localhost:8501``` for local development

<img src = "./images/streamlit.png" width="50%" height="50%">

#### Reference

- https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions
- https://medium.com/ryanjang-devnotes/ci-cd-hands-on-github-actions-docker-hub-aws-ec2-ba09f80297e1
- https://medium.com/@fredmanre/how-to-configure-docker-docker-compose-in-aws-ec2-amazon-linux-2023-ami-ab4d10b2bcdc
- https://github.com/adiii717/docker-python-cronjob


