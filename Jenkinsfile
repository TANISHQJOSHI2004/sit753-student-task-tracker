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
                bat 'python -m pytest --cov=app --cov-report=xml:coverage.xml -v'
            }
        }

        stage('Code Quality') {
            steps {
                withCredentials([string(
                    credentialsId: 'sonarqube-token',
                    variable: 'SONAR_TOKEN'
                )]) {
                    bat 'python -m pip install pysonar'
                    bat 'pysonar --sonar-host-url=http://localhost:9000 --sonar-token=%SONAR_TOKEN% --sonar-project-key=sit753-student-task-tracker --sonar-python-version=3.12 --sonar-python-coverage-report-paths=coverage.xml'
                }
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