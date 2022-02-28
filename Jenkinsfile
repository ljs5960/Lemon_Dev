pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh './gradlew clean build'
      }
    }

    stage('upload') {
      steps {
        sh 'aws s3 cp build/libs/application.war s3://elasticbeanstalk-ap-northeast-2-282460372239/Lemon/application.war --region ap-northeast-2'
      }
    }

    stage('deploy') {
      steps {
        sh 'aws elasticbeanstalk create-application-version --region ap-northeast-2 --application-name Lemon --version-label ${BUILD_TAG} --source-bundle S3Bucket="elasticbeanstalk-ap-northeast-2-282460372239/Lemon",S3Key="application.war"'
        sh 'aws elasticbeanstalk update-environment --region ap-northeast-2 --environment-name Lemon-dev --version-label ${BUILD_TAG}'
      }
    }

  }
}
