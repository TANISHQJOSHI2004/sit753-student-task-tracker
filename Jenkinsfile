pipeline {
    agent any

    stages {

        stage('Environment Check') {
            steps {
                bat 'python --version'
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" --version'
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
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" build -t student-task-tracker:%BUILD_NUMBER% .'
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" tag student-task-tracker:%BUILD_NUMBER% student-task-tracker:latest'
            }
        }
    }
}