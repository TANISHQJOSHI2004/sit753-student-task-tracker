pipeline {
    agent any

    environment {
        DOCKER_EXE = 'C:\\Users\\TANISHQ JOSHI\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        TRIVY_EXE  = 'C:\\Tools\\Trivy\\trivy.exe'
    }

    stages {

        stage('Build') {
            steps {
                echo 'Checking build environment...'

                bat 'python --version'
                bat '"%DOCKER_EXE%" --version'

                echo 'Building versioned Docker image...'

                bat '"%DOCKER_EXE%" build -t student-task-tracker:%BUILD_NUMBER% .'

                bat '"%DOCKER_EXE%" tag student-task-tracker:%BUILD_NUMBER% student-task-tracker:latest'
            }
        }

        stage('Test') {
            steps {
                echo 'Installing test dependencies...'

                bat 'python -m pip install -r requirements.txt'

                echo 'Running automated tests with coverage...'

                bat 'python -m pytest --cov=app --cov-report=xml:coverage.xml -v'
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running SonarQube analysis...'

                withCredentials([string(
                    credentialsId: 'sonarqube-token',
                    variable: 'SONAR_TOKEN'
                )]) {

                    bat 'python -m pip install pysonar'

                    bat 'pysonar --sonar-host-url=http://localhost:9000 --sonar-token=%SONAR_TOKEN% --sonar-project-key=sit753-student-task-tracker --sonar-python-version=3.12 --sonar-python-coverage-report-paths=coverage.xml'
                }
            }
        }

        stage('Security') {
            steps {

                echo 'Installing Bandit security scanner...'

                bat 'python -m pip install bandit'

                echo 'Running Python source-code security scan...'

                script {
                    def banditStatus = bat(
                        returnStatus: true,
                        script: 'python -m bandit -r app.py -lll -iii -f json -o bandit-report.json'
                    )

                    bat 'python -m bandit -r app.py -lll -iii || exit /b 0'

                    if (banditStatus != 0) {
                        error('Bandit detected a HIGH severity and HIGH confidence security issue.')
                    }
                }

                echo 'Running Docker image vulnerability scan...'

                bat '"%TRIVY_EXE%" image --severity HIGH,CRITICAL --exit-code 0 student-task-tracker:%BUILD_NUMBER%'

                script {
                    def trivyStatus = bat(
                        returnStatus: true,
                        script: '"%TRIVY_EXE%" image --ignore-unfixed --severity HIGH,CRITICAL --format json --output trivy-report.json --exit-code 1 student-task-tracker:%BUILD_NUMBER%'
                    )

                    if (trivyStatus != 0) {
                        error('Trivy detected fixable HIGH or CRITICAL vulnerabilities.')
                    }
                }

                echo 'Security checks completed successfully.'
            }

            post {
                always {
                    archiveArtifacts(
                        artifacts: 'bandit-report.json,trivy-report.json',
                        allowEmptyArchive: true,
                        fingerprint: true
                    )
                }
            }
        }
    }
}