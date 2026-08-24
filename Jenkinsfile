pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '955501536964.dkr.ecr.us-east-1.amazonaws.com'

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
                sh '''
                    python3 -m py_compile backend/app.py
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    echo "Building Frontend Docker Image..."

                    docker build \
                    -t ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG} \
                    ./frontend

                    echo "Frontend image built successfully."

                    echo "Building Backend Docker Image..."

                    docker build \
                    -t ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG} \
                    ./backend

                    echo "Backend image built successfully."
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    echo "Logging in to Amazon ECR..."

                    aws ecr get-login-password \
                    --region ${AWS_REGION} | \
                    docker login \
                    --username AWS \
                    --password-stdin ${ECR_REGISTRY}

                    echo "ECR login successful."
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                    echo "Pushing Frontend image..."

                    docker push \
                    ${ECR_REGISTRY}/${FRONTEND_REPO}:${IMAGE_TAG}

                    echo "Frontend image pushed successfully."

                    echo "Pushing Backend image..."

                    docker push \
                    ${ECR_REGISTRY}/${BACKEND_REPO}:${IMAGE_TAG}

                    echo "Backend image pushed successfully."
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Docker images successfully pushed to Amazon ECR.'
                echo 'Deployment will be configured next.'
            }
        }
    }

    post {
        success {
            echo '========================================='
            echo '     PIPELINE COMPLETED SUCCESSFULLY'
            echo '========================================='
        }

        failure {
            echo '========================================='
            echo '          PIPELINE FAILED'
            echo 'Check the Console Output for the error.'
            echo '========================================='
        }
    }
}
