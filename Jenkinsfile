node {
    stage ('Checkout') {
        checkout scm
        sh 'git fetch  # to fetch tags too...'
        sh 'git submodule update --init --recursive'
    }
    try {
        stage ('Tests') {
            sh 'docker run --rm --volume /var/run/docker.sock:/var/run/docker.sock --volume "${PWD}":/tmp/workspace --workdir /tmp/workspace python:2.7.18 sh -c \
            "make setup_for_test && make test"'
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
