pipeline {
  agent any

  environment {
    DOCKERHUB_USERNAME = 'ganeshjchoudhary'
    DOCKERHUB_REPOSITORY = 'django-app'
    IMAGE_TAG = "${BUILD_NUMBER}"
    DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
    GITHUB_CREDENTIALS_ID = 'github-token'
    KUBECONFIG_CREDENTIALS_ID = 'kubeconfig'
    K8S_NAMESPACE = 'django-app'
  }

  stages {
    stage('Checkout Code') {
      steps {
        git credentialsId: env.GITHUB_CREDENTIALS_ID, url: 'https://github.com/YourUsername/django-app-repo.git', branch: 'main'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          dockerImage = docker.build("${DOCKERHUB_USERNAME}/${DOCKERHUB_REPOSITORY}:${IMAGE_TAG}")
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', env.DOCKERHUB_CREDENTIALS_ID) {
            dockerImage.push()
            dockerImage.push('latest')
          }
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withKubeConfig(credentialsId: env.KUBECONFIG_CREDENTIALS_ID) {
          script {
            sh """
            kubectl get ns ${K8S_NAMESPACE} || kubectl create ns ${K8S_NAMESPACE}

            # Replace image tag dynamically in deployment YAML before apply
            sed 's|__IMAGE_TAG__|${IMAGE_TAG}|g' k8s/deployment.yaml | kubectl apply -n ${K8S_NAMESPACE} -f -

            # Patch deployment to ensure image update
            kubectl set image deployment/django-app django-app=docker.io/${DOCKERHUB_USERNAME}/${DOCKERHUB_REPOSITORY}:${IMAGE_TAG} -n ${K8S_NAMESPACE}
            """
          }
        }
      }
    }

    stage('Verify Deployment') {
      steps {
        withKubeConfig(credentialsId: env.KUBECONFIG_CREDENTIALS_ID) {
          sh "kubectl rollout status deployment/django-app -n ${K8S_NAMESPACE}"
        }
      }
    }
  }
}
