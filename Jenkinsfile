pipeline {
    agent any
        environment {
            K6_API_TOKEN=credentials("K6_API_TOKEN")
            K6_CLOUD_PROJECT_ID=credentials("K6_CLOUD_PROJECT_ID")
        }
        stages {
            stage('Performance Testing') {
                steps {                    
                    echo 'Running K6 performance tests...'
                    sh 'k6 login cloud --token ${K6_API_TOKEN}'
                    sh 'k6 cloud loadTests/test-api-gcom.js'
                    echo 'Completed Running K6 performance tests!'
                }
            }                                    
        }
}
