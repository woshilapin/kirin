node {
    stage ('Checkout') {
        checkout scm
        sh 'git fetch  # to fetch tags too...'
        sh 'git submodule update --init --recursive'
    }
    try {
        stage ('Tests') {
            sh 'make test_in_context'
        }
    } catch (err) {
        echo "Caught: ${err}"
            currentBuild.result = 'FAILURE'
    } finally {
        stage ('Cleanup') {
            cleanWs()
        }
    }
}
