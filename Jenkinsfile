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
	stage('Verify SonarQube Token') {
	    steps {
		withSonarQubeEnv('SonarQube') {
		    sh '''
			python3 - <<'PY'
	import os
	import urllib.request
	import urllib.error
	import base64

	token = os.environ.get("SONAR_AUTH_TOKEN", "")
	host = os.environ.get("SONAR_HOST_URL", "")

	credentials = base64.b64encode((token + ":").encode()).decode()

	request = urllib.request.Request(
	    host + "/api/authentication/validate",
	    headers={"Authorization": "Basic " + credentials}
	)

	try:
	    with urllib.request.urlopen(request) as response:
		print("SonarQube authentication response:", response.read().decode())
	except urllib.error.HTTPError as error:
	    print("SonarQube authentication HTTP status:", error.code)
	PY
		    '''
		}
	    }
	}
	stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
				export SONAR_TOKEN="\$SONAR_AUTH_TOKEN"
				${scannerHome}/bin/sonar-scanner
			"""
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
