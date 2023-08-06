import os
import traceback
import logging
from typing import Union, Any, Dict

import boto3


class ClusterIDNotFound(Exception):
    pass


class Logger(logging.Logger):
    def __init__(self, name: str, level: int = logging.WARNING):
        super().__init__(name, level)

    def exception(self, payload: Any, kwargs={}):
        self.error(traceback.format_exc().replace("\n", " \\n "))
        self.error(payload, **kwargs)


class RSConnectionProvider:
    def __init__(
        self,
        cluster_id: str = None,
        username: str = None,
        db_name: str = None,
        auto_create: bool = False,
        duration_seconds: int = 900,
        logger: Any = None,
        session: boto3.Session = None,
    ):
        self.session = session if session is not None else boto3.Session()
        self.rs_client = self.session.client("redshift")
        self.sm_client = self.session.client("secretsmanager")
        self.logger = self.__set_logger(logger)

        self.__set_cluster_id(cluster_id)
        self.cluster = None
        self.get_cluster_info()
        self.username = username
        self.db_name = db_name
        self.auto_create = auto_create
        self.duration_seconds = duration_seconds

    @staticmethod
    def __set_logger(logger: Any = None) -> Union[Logger, Any]:
        if logger is not None:
            return logger
        elif isinstance(logger, logging.Logger):
            return Logger(logger.name, logger.level)
        else:
            return Logger(__name__)

    def __set_cluster_id(self, cluster_id: str = None) -> None:
        if cluster_id is not None and cluster_id.strip() != "":
            self.cluster_id = cluster_id
            self.logger.debug("Cluster id explicitly set.")
        else:
            try:
                assert "CLUSTER_ID" in os.environ
                self.cluster_id = os.environ["CLUSTER_ID"]
                self.logger.debug("Cluster id found in ENV.")
            except AssertionError as exc:
                self.logger.exception("Unable to find Cluster id, Aborting.")
                raise ClusterIDNotFound from exc

    def get_cluster_info(self) -> Dict[str, str]:
        if self.cluster is not None:
            return self.cluster
        else:
            try:
                res = self.rs_client.describe_clusters(
                    ClusterIdentifier=self.cluster_id,
                )
                assert (
                    "Clusters" in res
                    and isinstance(res.get("Clusters"), list)
                    and len(res.get("Clusters")) > 0
                )
            except Exception as exc:
                self.logger.error("Unable to retrieve Cluster info, Aborting.")
                raise exc

            self.cluster = res.get("Clusters")[0]
            self.port = self.cluster.get("Endpoint").get("Port")
            self.addr = self.cluster.get("Endpoint").get("Address")

            return self.cluster

    def get_username(self) -> str:
        """Retrieves Redshift Username.
        Retrieval order is ENV Variable (`DB_USER`), Secrets Manager (name `DB_USER_SECRET_NAME`), Cluster's MasterUsername.
        """
        username = self.cluster.get("MasterUsername")
        try:
            assert "DB_USER" in os.environ
            self.logger.warn("RS User was found in ENV, please consider safer options.")
            username = os.environ["DB_USER"]
        except AssertionError as exc:
            self.logger.info(
                "RS Username not found in ENV, attempting to retrieve from Secrets Manager."
            )

            try:
                assert "DB_USER_SECRET_NAME" in os.environ

                try:
                    res = self.sm_client.get_secret_value(
                        SecretId=os.environ["DB_USER_SECRET_NAME"],
                    )
                    assert "SecretString" in res and isinstance(
                        res.get("SecretString"), str
                    )

                    username = res.get("SecretString")
                except Exception as exc:
                    self.logger.exception(
                        "Unable to retrieve parameter from Secrets Manager, aborting."
                    )
                    raise exc
            except AssertionError as exc:
                self.logger.warn("Secret name is missing from ENV, using master one.")

        return username

    def get_db_name(self) -> Union[str, None]:
        """Retrieves Redshift DB Name.
        Retrieval order is explicit argument (set during init), ENV Variable (`DB_NAME`).

        In case one is retrieved, and IAM Temporary Credentials are obtained, such credentials will be scoped to the DB specified."""
        if self.db_name is None:
            try:
                assert "DB_NAME" in os.environ
                self.logger.info(
                    "DB Name was found in ENV, credentials will be scoped to this DB."
                )
                return os.environ["DB_NAME"]
            except AssertionError as exc:
                self.logger.info(
                    "DB Name not found in ENV, credentials will allow access to any DB."
                )
                return None
        else:
            return self.db_name

    def get_pass(self) -> str:
        """Retrieves Redshift Password.
        Retrieval order is ENV Variable (`DB_PASS`), Secrets Manager (name `DB_PASS_SECRET_NAME`), IAM Temporary Credentials.

        In case of IAM Temporary Credentials it uses `boto3.client('redshift').get_cluster_credentials(**kwargs)`."""
        password = None
        try:
            assert "DB_PASS" in os.environ
            self.logger.warn(
                "RS Password was found in ENV, please consider safer options."
            )
            password = os.environ["DB_PASS"]
        except AssertionError as exc:
            self.logger.info(
                "RS Password not found in ENV, attempting to retrieve from Secrets Manager."
            )

            try:
                assert "DB_PASS_SECRET_NAME" in os.environ
                try:
                    res = self.sm_client.get_secret_value(
                        SecretId=os.environ["DB_PASS_SECRET_NAME"],
                    )
                    assert "SecretString" in res and isinstance(
                        res.get("SecretString"), str
                    )

                    password = res.get("SecretString")
                except Exception as exc:
                    self.logger.exception(
                        "Unable to retrieve parameter from Secrets Manager, aborting."
                    )
                    raise exc
            except AssertionError as exc:
                self.logger.info(
                    "Secret name not found in ENV, attempting to retrieve temporary password."
                )

                try:
                    kwargs = {
                        "AutoCreate": self.auto_create,
                        "ClusterIdentifier": self.cluster_id,
                        "DurationSeconds": self.duration_seconds,
                    }

                    if self.db_name is not None:
                        kwargs["DbName"] = self.db_name

                    if self.username is None:
                        raise Exception("Username cannot be None.")
                    else:
                        kwargs["DbUser"] = self.username

                    res = self.rs_client.get_cluster_credentials(**kwargs)

                    assert "DbUser" in res and "DbPassword" in res

                    self.username = res["DbUser"]
                    password = res["DbPassword"]
                except Exception as exc:
                    self.logger.exception(
                        "Unable to obtain temporary credentials, aborting."
                    )
                    raise exc

        return password

    def get_conn(self) -> Dict[str, Union[str, int, None]]:
        if self.username is None:
            self.username = self.get_username()

        if self.db_name is None:
            self.db_name = self.get_db_name()

        return {
            "host": self.addr,
            "port": self.port,
            "dbname": self.db_name,
            "password": self.get_pass(),
            "user": self.username,
        }