pipeline {

    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    triggers {
    //    pollSCM('H/2 * * * *')
	githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                sh 'python3 --version'
                sh 'git --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p reports
                    python -m pytest -v --junitxml=reports/junit.xml
                '''
            }
        }

	stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
			sh '''
                    	if [ -n "$SONAR_AUTH_TOKEN" ]; then
                        	echo "SONAR_AUTH_TOKEN is available"
                    	else
                        	echo "SONAR_AUTH_TOKEN is missing"
                    	fi

                    	if [ -n "$SONAR_TOKEN" ]; then
                        	echo "SONAR_TOKEN is available"
                    	else
                        	echo "SONAR_TOKEN is missing"
                    	fi
                	'''		
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
    }

    post {

        always {
            junit(
                testResults: 'reports/junit.xml',
                allowEmptyResults: true
            )
        }

        success {
            echo 'BUILD SUCCESSFUL'
        }

        failure {
            echo 'BUILD FAILED'
        }
    }
}
