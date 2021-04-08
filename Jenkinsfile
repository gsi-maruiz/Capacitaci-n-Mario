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
        }
}
