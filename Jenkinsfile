pipeline {
    environment {
        registry = "boressan/cicd"
        registryCredential = 'dockerhub_id'
    }
    agent any
    stages {
        stage('Image build') {
            steps {
                echo '====================building image===================================='
                script { customImage = docker.build(registry) }
            }
        }
        stage('Unit testing') {
            steps {
                echo '====================executing unittest================================'
                script { customImage.inside("--entrypoint=''") {} }
            }
        }
        stage('Docker-hub upload') {
            steps {
                echo '====================uploading docker-hub=============================='
                script { docker.withRegistry('', registryCredential) { customImage.push('master') } }
            }
        }
    }
}