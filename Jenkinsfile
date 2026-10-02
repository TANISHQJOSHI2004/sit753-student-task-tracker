pipeline {
    agent any

    stages {

        stage('Environment Check') {
            steps {
                bat 'python --version'
                bat 'docker --version'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pytest -v'
            }
        }

        stage('Build') {
            steps {
                bat 'docker build -t student-task-tracker:%BUILD_NUMBER% .'
                bat 'docker tag student-task-tracker:%BUILD_NUMBER% student-task-tracker:latest'
            }
        }
    }
}