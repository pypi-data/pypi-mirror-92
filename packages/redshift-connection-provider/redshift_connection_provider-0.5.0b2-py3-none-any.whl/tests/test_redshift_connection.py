import os
import logging
import unittest

import boto3
from moto import mock_secretsmanager, mock_redshift

from redshift_connection.provider import RSConnectionProvider, ClusterIDNotFound

CLUSTER_ID = "test-stack-rscluster1bedd956-1wz8352wp3vso"
DB_NAME = "default_db"
DB_USER = "some_user"
DB_PASS = "some_pass_1234"
DB_PORT = 5439
DB_USER_SECRET_NAME = "RSUser"
DB_PASS_SECRET_NAME = "RSPass"


class TestRSConnectionProvider(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        cls.mock_rs = mock_redshift()
        cls.mock_rs.start()
        cls.mock_sm = mock_secretsmanager()
        cls.mock_sm.start()

        cls.session = boto3.Session(
            aws_access_key_id="testing",
            aws_secret_access_key="testing",
            aws_session_token="testing",
        )

        cls.rs_client = cls.session.client("redshift")
        cls.__create_cluster(cls.rs_client)

        cls.sm_client = cls.session.client("secretsmanager")
        cls.__create_secret(cls.sm_client, DB_USER_SECRET_NAME, DB_USER)
        cls.__create_secret(cls.sm_client, DB_PASS_SECRET_NAME, DB_PASS)

    @staticmethod
    def __create_cluster(client):
        waiter = client.get_waiter("cluster_available")
        client.create_cluster(
            DBName=DB_NAME,
            ClusterIdentifier=CLUSTER_ID,
            ClusterType="single-node",
            NodeType="dc2.large",
            MasterUsername=DB_USER,
            MasterUserPassword=DB_PASS,
            Port=DB_PORT,
            NumberOfNodes=1,
        )
        waiter.wait(
            ClusterIdentifier=CLUSTER_ID, WaiterConfig={"Delay": 1, "MaxAttempts": 2}
        )

    @staticmethod
    def __create_secret(client, name: str, value: str):
        client.create_secret(
            Name=name,
            SecretString=value,
        )

    @staticmethod
    def __destroy_cluster(client):
        waiter = client.get_waiter("cluster_deleted")
        client.delete_cluster(
            ClusterIdentifier=CLUSTER_ID,
            SkipFinalClusterSnapshot=True,
        )
        waiter.wait(
            ClusterIdentifier=CLUSTER_ID, WaiterConfig={"Delay": 1, "MaxAttempts": 2}
        )

    @staticmethod
    def __destroy_secret(client, name: str):
        client.delete_secret(SecretId=name)

    @staticmethod
    def __cleanup_env():
        env_vars = [
            "CLUSTER_ID",
            "DB_NAME",
            "DB_USER",
            "DB_PASS",
            "DB_PORT",
            "DB_USER_SECRET_NAME",
            "DB_PASS_SECRET_NAME",
        ]
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]

    @classmethod
    def tearDownClass(cls):
        cls.__destroy_cluster(cls.rs_client)
        cls.mock_rs.stop()
        cls.__destroy_secret(cls.sm_client, DB_USER_SECRET_NAME)
        cls.__destroy_secret(cls.sm_client, DB_PASS_SECRET_NAME)
        cls.mock_sm.stop()
        cls.__cleanup_env()
        logging.disable(logging.NOTSET)

    def test_init(self):
        # Raises exceptions
        with self.assertRaises(ClusterIDNotFound):
            RSConnectionProvider()

        with self.assertRaises(Exception) as exc:
            RSConnectionProvider("some-id", session=self.session)
        self.assertEqual(
            exc.exception.response["Error"]["Code"], "ClusterNotFound"  # type: ignore
        )

        # From ENV
        os.environ["CLUSTER_ID"] = CLUSTER_ID
        rs_conn = RSConnectionProvider()
        self.assertEqual(os.environ["CLUSTER_ID"], rs_conn.cluster_id)
        self.assertEqual(DB_PORT, rs_conn.port)
        del os.environ["CLUSTER_ID"]

        # From args
        rs_conn = RSConnectionProvider(
            cluster_id=CLUSTER_ID,
            logger=logging.getLogger("some_name"),
            session=self.session,
        )
        self.assertEqual(CLUSTER_ID, rs_conn.cluster_id)
        self.assertEqual("testing", rs_conn.session.get_credentials().access_key)
        self.assertEqual("some_name", rs_conn.logger.name)

        # Defaults
        rs_conn = RSConnectionProvider(cluster_id=CLUSTER_ID)
        self.assertNotEqual("testing", rs_conn.session.get_credentials().access_key)
        self.assertEqual("redshift_connection.provider", rs_conn.logger.name)
        self.assertFalse(rs_conn.auto_create)
        self.assertEqual(900, rs_conn.duration_seconds)

    def test_username(self):
        # From Cluster info (master user)
        rs_conn = RSConnectionProvider(cluster_id=CLUSTER_ID, session=self.session)
        self.assertEqual(DB_USER, rs_conn.get_username())

        # From ENV
        os.environ["DB_USER"] = "user_from_env"
        self.assertEqual("user_from_env", rs_conn.get_username())
        del os.environ["DB_USER"]

        # From Secret Manager
        self.__create_secret(self.sm_client, "MY_DB_USER", "user_from_sm")
        os.environ["DB_USER_SECRET_NAME"] = "MY_DB_USER"
        self.assertEqual("user_from_sm", rs_conn.get_username())
        del os.environ["DB_USER_SECRET_NAME"]
        self.__destroy_secret(self.sm_client, "MY_DB_USER")

    def test_db_name(self):
        # No DB
        rs_conn = RSConnectionProvider(cluster_id=CLUSTER_ID, session=self.session)
        self.assertIsNone(rs_conn.get_db_name())

        # From ENV
        os.environ["DB_NAME"] = "some_db"
        self.assertEqual("some_db", rs_conn.get_db_name())
        del os.environ["DB_NAME"]

    def test_password(self):
        # Raises exceptions
        with self.assertRaises(Exception):
            rs_conn = RSConnectionProvider(cluster_id=CLUSTER_ID, session=self.session)
            rs_conn.get_pass()

        # From IAM
        rs_conn = RSConnectionProvider(
            cluster_id=CLUSTER_ID, username="my_user", session=self.session
        )
        self.assertEqual(32, len(rs_conn.get_pass()))
        self.assertTrue(rs_conn.username.startswith("IAM:"))

        # From ENV
        os.environ["DB_PASS"] = DB_PASS
        self.assertEqual(DB_PASS, rs_conn.get_pass())
        del os.environ["DB_PASS"]

        # From Secret Manager
        self.__create_secret(self.sm_client, "MY_DB_PASS", "pass_from_sm")
        os.environ["DB_PASS_SECRET_NAME"] = "MY_DB_PASS"
        self.assertEqual("pass_from_sm", rs_conn.get_pass())
        del os.environ["DB_PASS_SECRET_NAME"]
        self.__destroy_secret(self.sm_client, "MY_DB_PASS")

    def test_get_connection(self):
        # From IAM
        rs_conn = RSConnectionProvider(cluster_id=CLUSTER_ID, session=self.session)
        conn = rs_conn.get_conn()
        host = conn.get("host")
        self.assertTrue(host.startswith(CLUSTER_ID))  # type: ignore
        self.assertEqual(32, len(conn.get("password")))  # type: ignore
        del conn["host"]
        del conn["password"]
        self.assertDictEqual(
            {
                "port": DB_PORT,
                "dbname": None,
                "user": f"IAM:{DB_USER}",
            },
            conn,
        )

        # From IAM auto_create user
        rs_conn = RSConnectionProvider(
            cluster_id=CLUSTER_ID, session=self.session, auto_create=True
        )
        conn = rs_conn.get_conn()
        self.assertEqual(32, len(conn.get("password")))  # type: ignore
        self.assertTrue(rs_conn.username.startswith("IAMA:"))

        # From IAM explicit user
        rs_conn = RSConnectionProvider(
            cluster_id=CLUSTER_ID, session=self.session, username="my_user"
        )
        conn = rs_conn.get_conn()
        self.assertEqual(32, len(conn.get("password")))  # type: ignore
        self.assertEqual(rs_conn.username, "IAM:my_user")

        # With explicit DB name
        rs_conn = RSConnectionProvider(
            cluster_id=CLUSTER_ID, session=self.session, db_name="my_db"
        )
        conn = rs_conn.get_conn()
        self.assertEqual("my_db", conn.get("dbname"))


if __name__ == "__main__":
    unittest.main()