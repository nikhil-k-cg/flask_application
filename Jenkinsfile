pipeline {
    agent any

    environment {
        githubCredential = 'GITHUB'
        SONAR_NODEJS_EXECUTABLE = '/usr/bin/nodejs'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                credentialsId: githubCredential,
                url: 'https://github.com/nikhil-k-cg/flask_application.git'
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
