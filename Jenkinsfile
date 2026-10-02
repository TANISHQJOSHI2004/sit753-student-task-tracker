pipeline {
    agent any

    environment {
        DOCKER_EXE = 'C:\\Users\\TANISHQ JOSHI\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

    stages {

        stage('Environment Check') {
            steps {
                bat 'python --version'
                bat '"%DOCKER_EXE%" --version'
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
                bat '"%DOCKER_EXE%" build -t student-task-tracker:%BUILD_NUMBER% .'
                bat '"%DOCKER_EXE%" tag student-task-tracker:%BUILD_NUMBER% student-task-tracker:latest'
            }
        }
    }
}