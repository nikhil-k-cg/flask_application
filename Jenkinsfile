pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                credentialsId: githubCredential,
                url: 'https://github.com/nikhil-k-cg/jenkins_test.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
                }
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
    }
}
