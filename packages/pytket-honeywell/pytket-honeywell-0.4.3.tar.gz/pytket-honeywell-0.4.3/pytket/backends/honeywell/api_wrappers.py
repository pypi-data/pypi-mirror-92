# -*- coding: utf-8 -*-
""""
Functions used to submit jobs with Honeywell Quantum Solutions API.

Adapted from original file provided by Honeywell Quantum Solutions
"""
import asyncio
import json
import sys
import getpass
import jwt
import datetime
import time
from http import HTTPStatus
from typing import Union, Optional

import requests
import websockets
import nest_asyncio
import keyring


# This is necessary for use in Jupyter notebooks to allow for nested asyncio loops
nest_asyncio.apply()


class _OverrideManger:
    def __init__(
        self,
        api_handler: "HoneywellQAPI",
        ws_timeout: Optional[int] = None,
        retry_timeout: Optional[int] = None,
    ):
        self._ws = ws_timeout
        self._retry = retry_timeout
        self.api_handler = api_handler
        self._orig_ws = api_handler.ws_timeout
        self._orig_retry = api_handler.retry_timeout

    def __enter__(self) -> None:
        if self._ws is not None:
            self.api_handler.ws_timeout = self._ws
        if self._retry is not None:
            self.api_handler.retry_timeout = self._retry

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.api_handler.ws_timeout = self._orig_ws
        self.api_handler.retry_timeout = self._orig_retry


class HoneywellQAPI:

    JOB_DONE = ["failed", "completed", "canceled"]

    DEFAULT_API_URL = "https://qapi.honeywell.com/"
    DEFAULT_TIME_SAFETY = (
        30  # Default safety factor (in seconds) to token expiration before a refresh
    )

    def __init__(
        self,
        user_name: str = None,
        token: str = None,
        machine: str = None,
        api_url: str = None,
        api_version: int = 1,
        shots: int = 100,
        use_websocket: bool = True,
        time_safety: int = None,
    ):
        """Initialize and login to the Honeywell Quantum API interface

        All arguments are optional

        Arguments:
            user_name (str): User e-mail used to register
            token (str): Token used to refresh id token
            url (str): Url of the Quantum API including version: https://qapi.honeywell.com/v1/
            shots (int): Default number of shots for submitted experiments
            use_websockets: Whether to default to using websockets to reduce traffic
        """
        try:
            import config
        except:
            config = None

        api_url = getattr(config, "api_url", api_url)
        if not api_url or api_url == self.DEFAULT_API_URL:
            self.url = f"{self.DEFAULT_API_URL}v{api_version}/"
            self.keyring_service = "HQS-API"
        else:
            self.url = f"{api_url}v{api_version}/"
            self.keyring_service = f"HQS-API:{self.url}"

        self.user_name = getattr(config, "user_name", user_name)
        self.refresh_token = (
            token
            if token
            else getattr(config, "refresh_token", self._get_token("refresh_token"))
        )
        self.shots = getattr(config, "shots", shots)
        self.api_version = getattr(config, "api_version", api_version)
        self.machine = getattr(config, "machine", machine)
        self.use_websocket = getattr(config, "use_websocket", use_websocket)
        self.time_safety_factor = (
            time_safety
            if time_safety
            else getattr(config, "time_safety", self.DEFAULT_TIME_SAFETY)
        )
        self.ws_timeout = getattr(config, "ws_timeout", 180)
        self.retry_timeout = getattr(config, "retry_timeout", 4)
        self.recently_submitted = []

        self.login()

    def override_timeouts(
        self, ws_timeout: Optional[int] = None, retry_timeout: Optional[int] = None
    ):
        return _OverrideManger(self, ws_timeout=ws_timeout, retry_timeout=retry_timeout)

    def _request_tokens(self, body):
        """ Method to send login request to machine api and save tokens. """
        try:
            # send request to login
            response = requests.post(
                f"{self.url}/login",
                json.dumps(body),
            )

            # reset body to delete credentials
            body = {}

            if response.status_code != HTTPStatus.OK:
                return response.status_code, response.json()

            else:
                print("***Successfully logged in***")
                self._save_tokens(
                    response.json()["id-token"], response.json()["refresh-token"]
                )
                return response.status_code, None

        except requests.exceptions.RequestException as e:
            print(e)
            return None, None

    def _get_credentials(self):
        """ Method to ask for user's credentials """
        if not self.user_name:
            user_name = input("Enter your email: ")
        else:
            user_name = self.user_name
        pwd = getpass.getpass(prompt="Enter your password: ")
        return user_name, pwd

    def _authenticate(self, action=None):
        """This method makes requests to refresh or get new id-token.
        If a token refresh fails due to token being expired, credentials
        get requested from user.
        """
        # login body
        body = {}

        if action == "refresh":
            body["refresh-token"] = self.refresh_token
        else:
            # ask user for crendentials before making login request
            user_name, pwd = self._get_credentials()
            body["email"] = user_name
            body["password"] = pwd

            # clear credentials
            user_name = None
            pwd = None

        # send login request to API
        status_code, message = self._request_tokens(body)

        body = {}

        if status_code != HTTPStatus.OK:
            # check if we got an error because refresh token has expired
            if status_code == HTTPStatus.BAD_REQUEST:

                if "Invalid Refresh Token" in message["error"]["text"]:
                    # ask user for credentials to login again
                    user_name, pwd = self._get_credentials()
                    body["email"] = user_name
                    body["password"] = pwd

                    # send login request to API
                    status_code, message = self._request_tokens(body)

        if status_code != HTTPStatus.OK:
            raise RuntimeError(f"HTTP error while logging in:", status_code)

    def _get_token(self, token_name: str):
        """Method to retrieve id and refresh tokens from system's keyring service.
        Windows keyring backend has a length limitation on passwords.
        To avoid this, passwords get splitted up into two credentials.
        """

        token = None

        token_first = keyring.get_password(self.keyring_service, f"{token_name}_first")
        token_second = keyring.get_password(
            self.keyring_service, f"{token_name}_second"
        )

        if token_first is not None and token_second is not None:
            token = token_first + token_second

        return token

    def _save_tokens(self, id_token: str, refresh_token: str):
        """Method to save id and refresh tokens on system's keyring service.
        Windows keyring backend has a length limitation on passwords.
        To avoid this, passwords get splitted up into two credentials.
        """

        # save two id_token halves
        id_token_first = id_token[: len(id_token) // 2]
        id_token_second = id_token[len(id_token) // 2 :]
        keyring.set_password(self.keyring_service, "id_token_first", id_token_first)
        keyring.set_password(self.keyring_service, "id_token_second", id_token_second)

        # save refresh_token halves
        refresh_token_first = refresh_token[: len(refresh_token) // 2]
        refresh_token_second = refresh_token[len(refresh_token) // 2 :]
        keyring.set_password(
            self.keyring_service, "refresh_token_first", refresh_token_first
        )
        keyring.set_password(
            self.keyring_service, "refresh_token_second", refresh_token_second
        )

    def login(self) -> str:
        """This methods checks if we have a valid (non-expired) id-token
        and returns it, otherwise it gets a new one with refresh-token.
        If refresh-token doesn't exist, it asks user for credentials.
        """
        # check if id_token exists
        id_token = self._get_token("id_token")
        if id_token is None:
            # authenticate against '/login' endpoint
            self._authenticate()

            # get id_token
            id_token = self._get_token("id_token")

        # check id_token is not expired yet
        expiration_date = jwt.decode(id_token, verify=False)["exp"]
        if expiration_date < (
            datetime.datetime.now().timestamp() - self.time_safety_factor
        ):
            print("Your id token is expired. Refreshing...")

            # get refresh_token
            refresh_token = self._get_token("refresh_token")
            if refresh_token is not None:
                self._authenticate("refresh")
            else:
                self._authenticate()

            # get id_token
            id_token = self._get_token("id_token")

        return id_token

    def recent_jobs(
        self, start: str = None, end: str = None, days: int = None, jobs: int = None
    ):
        id_token = self.login()
        if start is not None and end is not None:
            res = requests.get(
                f"{self.url}metering?start={start}&end={end}",
                headers={"Authorization": id_token},
            )
            self._response_check(res, f"metering between {start} and {end}")
            return res.json()
        elif days is not None:
            res = requests.get(
                f"{self.url}metering?days={days}", headers={"Authorization": id_token}
            )
            self._response_check(res, f"metering of last {days} days")
            return res.json()
        elif jobs is not None:
            res = requests.get(
                f"{self.url}metering?jobs={jobs}", headers={"Authorization": id_token}
            )
            self._response_check(res, f"metering of last {jobs} jobs")
            return res.json()
        else:
            raise ValueError("Need more information to make a metering request")

    def submit_job(
        self, qasm_str: str, shots: int = None, machine: str = None, name: str = "job"
    ) -> str:
        """
        Submits job to device and returns job ID.

        Args:
            qasm_str:   OpenQASM file to run
            shots:      number of repetitions of qasm_str
            machine:    machine to run on
            name:       name of job (for error handling)

        Returns:
            (str):     id of job submitted

        """
        try:
            if not machine and not self.machine:
                raise RuntimeError("Must provide valid machine name")
            # send job request
            body = {
                "machine": machine if machine else self.machine,
                "name": name,
                "language": "OPENQASM 2.0",
                "program": qasm_str,
                "priority": "normal",
                "count": shots if shots else self.shots,
                "options": None,
            }
            id_token = self.login()
            res = requests.post(
                f"{self.url}job", json.dumps(body), headers={"Authorization": id_token}
            )
            self._response_check(res, "job submission")

            # extract job ID from response
            jr = res.json()
            job_id = jr["job"]
            print(
                f"submitted {name} id={{job}}, submit date={{submit-date}}".format(**jr)
            )

        except ConnectionError:
            if len(sys.argv) > 2:
                print("{} Connection Error: Error during submit...".format(name))
            else:
                print("Connection Error: Error during submit...")

        self.recently_submitted.append(
            {"job": job_id, "name": name, "machine": machine, "program": qasm_str}
        )
        return job_id

    def _response_check(self, res, description):
        """Consolidate as much error-checking of response"""
        # check if token has expired or is generally unauthorized
        if res.status_code == HTTPStatus.UNAUTHORIZED:
            jr = res.json()
            raise RuntimeError(
                f"Authorization failure attempting: {description}.\n\nServer Response: {jr}"
            )
        elif res.status_code != HTTPStatus.OK:
            jr = res.json()
            raise RuntimeError(
                f"HTTP error attempting: {description}.\n\nServer Response: {jr}"
            )

    def retrieve_job_status(self, job_id: str, use_websocket: bool = None) -> dict:
        """
        Retrieves job status from device.

        Args:
            job_id:        unique id of job
            use_websocket: use websocket to minimize interaction

        Returns:
            (dict):        output from API

        """
        job_url = f"{self.url}job/{job_id}"
        # Using the login wrapper we will automatically try to refresh token
        id_token = self.login()
        if use_websocket or (use_websocket is None and self.use_websocket):
            job_url += "?websocket=true"
        res = requests.get(job_url, headers={"Authorization": id_token})

        jr = None
        # Check for invalid responses, and raise an exception if so
        self._response_check(res, "job status")
        # if we successfully got status return the decoded details
        if res.status_code == HTTPStatus.OK:
            jr = res.json()
        return jr

    def retrieve_job(self, job_id: str, use_websocket: bool = None) -> dict:
        """
        Retrieves job from device.

        Args:
            job_id:        unique id of job
            use_websocket: use websocket to minimize interaction

        Returns:
            (dict):        output from API

        """
        jr = self.retrieve_job_status(job_id, use_websocket)
        if "status" in jr and jr["status"] in self.JOB_DONE:
            return jr

        if "websocket" in jr:
            # wait for job completion using websocket
            jr = asyncio.get_event_loop().run_until_complete(self._wait_results(job_id))
        else:
            # poll for job completion
            jr = self._poll_results(job_id)
        return jr

    def _poll_results(self, job_id):
        id_token = self.login()
        jr = None
        while True:
            try:
                jr = self.retrieve_job_status(job_id)

                # If we are failing to retrieve status of any kind, then fail out.
                if jr is None:
                    break

                time.sleep(self.retry_timeout)
            except KeyboardInterrupt:
                raise RuntimeError("Keyboard Interrupted")
        return jr

    async def _wait_results(self, job_id):
        id_token = self.login()
        while True:
            jr = self.retrieve_job_status(job_id, True)
            if not jr:
                return jr
            elif "status" in jr and jr["status"] in self.JOB_DONE:
                return jr
            else:
                task_token = jr["websocket"]["task_token"]
                execution_arn = jr["websocket"]["executionArn"]
                websocket_uri = self.url.replace("https://", "wss://ws.")
                async with websockets.connect(websocket_uri) as websocket:
                    body = {
                        "action": "OpenConnection",
                        "task_token": task_token,
                        "executionArn": execution_arn,
                    }
                    await websocket.send(json.dumps(body))
                    while True:
                        try:
                            res = await asyncio.wait_for(
                                websocket.recv(), timeout=self.ws_timeout
                            )
                            jr = json.loads(res)
                            if "status" in jr and jr["status"] in self.JOB_DONE:
                                return jr
                        except (
                            asyncio.TimeoutError,
                            websockets.exceptions.ConnectionClosed,
                        ):
                            try:
                                # Try to keep the connection alive...
                                pong = await websocket.ping()
                                await asyncio.wait_for(pong, timeout=10)
                                continue
                            except:
                                # If we are failing, wait a little while, then start from the top
                                await asyncio.sleep(self.retry_timeout)
                                break
                        except KeyboardInterrupt:
                            raise RuntimeError("Keyboard Interrupted")

    def run_job(
        self, qasm_str: str, shots: int, machine: str, name: str = "job"
    ) -> dict:
        """
        Submits a job and waits to receives job result dictionary.

        Args:
            qasm_file:  OpenQASM file to run
            name:       name of job (for error handling)
            shots:      number of repetitions of qasm_str
            machine:    machine to run on

        Returns:
            jr:         (dict) output from API

        """
        job_id = self.submit_job(
            qasm_str=qasm_str, shots=shots, machine=machine, name=name
        )

        jr = self.retrieve_job(job_id)

        return jr

    def status(self, machine: str = None) -> str:
        """
        Check status of machine.

        Args:
            (str):    machine name

        """
        id_token = self.login()
        res = requests.get(
            f"{self.url}machine/{machine if machine else self.machine}",
            headers={"Authorization": id_token},
        )
        self._response_check(res, "get machine status")
        jr = res.json()

        return jr["state"]

    def cancel(self, job_id: str) -> dict:
        """
        Cancels job.

        Args:
            job_id:     job ID to cancel

        Returns:
            jr:         (dict) output from API

        """

        id_token = self.login()
        res = requests.post(
            f"{self.url}job/{job_id}/cancel", headers={"Authorization": id_token}
        )
        self._response_check(res, "job cancel")
        jr = res.json()

        return jr
