pipeline {
    agent any
        stages {
            stage('Performance Testing') {
                steps {                    
                    echo 'Running K6 performance tests...'
                    sh 'k6 run loadTests/performance-test.js'
                }
            }                                    
        }
}
