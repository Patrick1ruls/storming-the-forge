# StormForge - Technical Challenge

## Requirements
* Make sure the web application is running locally on your machine
* Port forward to all components under test:
    ```
    kubectl port-forward <pod> <external_ip>:<internal_ip>
    ```
    * Use the following external_ip's:
        * voting-service: 5555
        * result-service: 9876
        * redis: 6379
* Python 3 installed
* Pip installed
* Install all requirements from requirements.txt ideally in a virtual environment
    ```
    pip install requirements.txt
    ```
* An up to date web driver like chrome or firefox installed
* Run the following command to startup all tests in parallel
    ```
    pytest tests --log-cli-level=INFO -n 24
    ```


## Example Report
```
[gw3] [  4%] PASSED tests/component/test_redis.py::test_redis_queue_push_pull
[gw8] [  8%] PASSED tests/component/test_result_api.py::test_bad_sid_400_response[0]
[gw2] [ 12%] PASSED tests/component/test_redis.py::test_redis_is_available
[gw9] [ 16%] PASSED tests/component/test_result_api.py::test_no_transport_400_response
[gw6] [ 20%] PASSED tests/component/test_result_api.py::test_bad_sid_400_response[gg]
[gw1] [ 25%] PASSED tests/component/test_postgres.py::test_db_column_types
[gw7] [ 29%] PASSED tests/component/test_result_api.py::test_bad_sid_400_response[-1]
[gw4] [ 33%] PASSED tests/component/test_result_api.py::test_no_sid_200_response
[gw11] [ 37%] PASSED tests/component/test_voter_api.py::test_200_vote[b]
[gw17] [ 41%] PASSED tests/component/test_voter_api.py::test_400_response[0]
[gw14] [ 45%] PASSED tests/component/test_voter_api.py::test_200_vote[=b]
[gw15] [ 50%] PASSED tests/component/test_voter_api.py::test_400_response[votes=a]
[gw5] [ 54%] PASSED tests/component/test_result_api.py::test_sid_200_response
[gw0] [ 58%] PASSED tests/component/test_postgres.py::test_db_connection
[gw12] [ 62%] PASSED tests/component/test_voter_api.py::test_200_vote[vote=-1]
[gw16] [ 66%] PASSED tests/component/test_voter_api.py::test_400_response[]
[gw10] [ 70%] PASSED tests/component/test_voter_api.py::test_200_vote[a]
[gw13] [ 75%] PASSED tests/component/test_voter_api.py::test_200_vote[asdfljhbb]
[gw20] [ 79%] PASSED tests/integration/test_user_can_vote.py::test_user_can_go_to_results_page
[gw18] [ 83%] PASSED tests/integration/test_user_can_vote.py::test_user_can_go_to_voting_page
[gw21] [ 87%] PASSED tests/integration/test_user_can_vote.py::test_results_page_elements_exist
[gw19] [ 91%] PASSED tests/integration/test_user_can_vote.py::test_voting_page_elements_exist
[gw23] [ 95%] PASSED tests/integration/test_user_can_vote.py::test_user_can_vote[a]
[gw22] [100%] PASSED tests/integration/test_user_can_vote.py::test_user_can_vote[b]
```
