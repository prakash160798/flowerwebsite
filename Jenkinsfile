pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '776782461638.dkr.ecr.us-east-1.amazonaws.com'
        FRONTEND_REPO = 'flower-frontend'
        BACKEND_REPO = 'flower-backend'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Backend') {
            steps {
                sh 'python3 -m py_compile backend/app.py'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build -t ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG} -f frontend/Dockerfile .
                    docker build -t ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG} ./backend
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ${AWS_REGION} |
                    docker login --username AWS --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                    docker push ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy using the same docker-compose.yml on the application EC2.'
                echo 'Configure your secure Jenkins-to-EC2 connection here.'
            }
        }
    }
}
