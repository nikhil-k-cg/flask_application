pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nikhil1289/jenkins_test'
        DOCKER_REGISTRY = 'docker.io' 
        DOCKER_CREDENTIALS_ID = 'DOCKERHUB' 
        githubCredential = 'GITHUB'
        CONTAINER_NAME = 'my-flask-application'  
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                credentialsId: githubCredential,
                url: 'https://github.com/nikhil-k-cg/jenkins_test.git'
            }
        }

        stage('SonarQube analysis') {
            steps {
                script {
                    scannerHome = tool 'flask_application'// must match the name of an actual scanner installation directory on your Jenkins build agent
                }
                withSonarQubeEnv('flask_application') {// If you have configured more than one global server connection, you can specify its name as configured in Jenkins
                sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }

        stage('Check if container is running') {
            steps {
                script {
                    // Check if the container is running
                    def runningContainer = sh(script: "docker ps -q -f name=${CONTAINER_NAME}", returnStdout: true).trim()
                    if (runningContainer) {
                        echo "Container ${CONTAINER_NAME} is running. Stopping it now..."
                        // Stop the container
                        sh "docker stop ${CONTAINER_NAME}"
                    } else {
                        echo "Container ${CONTAINER_NAME} is not running."
                    }
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    // Build the Docker image
                    echo "Building Docker image ..."
                    sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
                }
            }
        }

        stage('Login to Docker Registry') {
            steps {
                script {
                    //docker.withRegistry("$DOCKER_REGISTRY", "$DOCKER_CREDENTIALS_ID") {
                        // Login to Docker registry
                         withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo $DOCKER_PASSWORD | docker login $DOCKER_REGISTRY -u $DOCKER_USERNAME --password-stdin
                        '''
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Push the Docker image to the registry
                    // docker.withRegistry("$DOCKER_REGISTRY", "$DOCKER_CREDENTIALS_ID") {
                    //     sh "docker push $DOCKER_IMAGE:$BUILD_NUMBER"
                    // }
                    sh "docker push $DOCKER_IMAGE:$BUILD_NUMBER"
                }
            }
        }

        stage('Docker run') {
            steps {
                script {
                    // Run the container from the newly built image
                    echo "Running Docker container ${CONTAINER_NAME}..."
                    sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME} $DOCKER_IMAGE:$BUILD_NUMBER"
                }
            }
        }
    }

    post {
        always {
            echo "Docker image built and pushed successfully!"
            echo "Application running successfully"
            sh "docker system prune -f"
        }
    }
}
