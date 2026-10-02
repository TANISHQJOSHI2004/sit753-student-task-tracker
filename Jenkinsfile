pipeline {
    agent any

    environment {
        DOCKER_EXE = 'C:\\Users\\TANISHQ JOSHI\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        TRIVY_EXE  = 'C:\\Tools\\Trivy\\trivy.exe'
        APP_NAME   = 'student-task-tracker'
        CONTAINER_NAME = 'student-task-tracker-app'
    }

    stages {

        stage('Build') {
            steps {
                echo 'Checking build environment...'

                bat 'python --version'
                bat '"%DOCKER_EXE%" --version'

                echo 'Building versioned Docker image...'

                bat '"%DOCKER_EXE%" build --pull -t %APP_NAME%:%BUILD_NUMBER% .'
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

                bat '"%TRIVY_EXE%" image --severity HIGH,CRITICAL --exit-code 0 %APP_NAME%:%BUILD_NUMBER%'

                script {
                    def trivyStatus = bat(
                        returnStatus: true,
                        script: '"%TRIVY_EXE%" image --ignore-unfixed --severity HIGH,CRITICAL --format json --output trivy-report.json --exit-code 1 %APP_NAME%:%BUILD_NUMBER%'
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

        stage('Deploy') {
            steps {
                echo 'Deploying Student Task Tracker...'

                bat '''
                "%DOCKER_EXE%" rm -f %CONTAINER_NAME% 2>nul || exit /b 0
                '''

                bat '"%DOCKER_EXE%" run -d --name %CONTAINER_NAME% --restart unless-stopped -p 5001:5000 %APP_NAME%:%BUILD_NUMBER%'

                echo 'Waiting for deployed container to become healthy...'

                bat '''
                powershell -NoProfile -Command "$status=''; for($i=0; $i -lt 20; $i++){ $status = & $env:DOCKER_EXE inspect --format '{{.State.Health.Status}}' $env:CONTAINER_NAME; Write-Host ('Container health: ' + $status); if($status -eq 'healthy'){ exit 0 }; Start-Sleep -Seconds 2 }; Write-Host 'Container failed health check'; exit 1"
                '''

                echo 'Deployment completed successfully.'

                bat '"%DOCKER_EXE%" ps --filter "name=%CONTAINER_NAME%"'
            }
        }

        stage('Release') {
            steps {
                echo 'Creating release tags...'

                bat '"%DOCKER_EXE%" tag %APP_NAME%:%BUILD_NUMBER% %APP_NAME%:release-%BUILD_NUMBER%'
                bat '"%DOCKER_EXE%" tag %APP_NAME%:%BUILD_NUMBER% %APP_NAME%:latest'

                echo 'Creating release metadata...'

                bat '''
                echo Application=Student Task Tracker> release-info.txt
                echo Build=%BUILD_NUMBER%>> release-info.txt
                echo Image=%APP_NAME%:release-%BUILD_NUMBER%>> release-info.txt
                echo GitCommit=%GIT_COMMIT%>> release-info.txt
                '''

                echo 'Release created successfully.'
            }

            post {
                success {
                    archiveArtifacts(
                        artifacts: 'release-info.txt',
                        fingerprint: true
                    )
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking Docker container status...'

                bat '"%DOCKER_EXE%" ps --filter "name=%CONTAINER_NAME%"'

                echo 'Checking Docker health status...'

                bat '''
                powershell -NoProfile -Command "$status = & $env:DOCKER_EXE inspect --format '{{.State.Health.Status}}' $env:CONTAINER_NAME; Write-Host ('Docker health status: ' + $status); if($status -ne 'healthy'){ exit 1 }"
                '''

                echo 'Checking application health endpoint...'

                bat '''
                powershell -NoProfile -Command "$response = Invoke-RestMethod -Uri 'http://127.0.0.1:5001/health' -TimeoutSec 10; Write-Host ('Service: ' + $response.service); Write-Host ('Status: ' + $response.status); if($response.status -ne 'healthy'){ exit 1 }"
                '''

                echo 'Monitoring checks passed. Application is healthy.'
            }
        }
    }

    post {
        success {
            echo '=============================================='
            echo 'CI/CD PIPELINE COMPLETED SUCCESSFULLY'
            echo 'Build -> Test -> Code Quality -> Security'
            echo 'Deploy -> Release -> Monitoring'
            echo 'Application: http://localhost:5001'
            echo 'Health: http://localhost:5001/health'
            echo '=============================================='
        }

        failure {
            echo 'Pipeline failed. Check the failed stage in Jenkins Console Output.'
        }
    }
}