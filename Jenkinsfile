pipeline {
    agent { label 'master'}

        stages {
            stage ('settings') {
                steps {
                    sh "python3 manage.py migrate"                  
                }
            }            
            stage ('create deploy') {
                steps {
                    sh "python3 manage.py runserver"
                }
            }
            stage('Performance Testing') {
                steps {                    
                    echo 'Running K6 performance tests...'
                    sh 'k6 run loadTests/performance-test.js'
                }
            }
        }
}
