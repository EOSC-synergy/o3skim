pipeline {
    agent { dockerfile true }
    
    stages {
        stage('Unit testing') {
            steps {
                echo '====================executing unittest================================'
                sh 'tox'
            }
        }
    }
}