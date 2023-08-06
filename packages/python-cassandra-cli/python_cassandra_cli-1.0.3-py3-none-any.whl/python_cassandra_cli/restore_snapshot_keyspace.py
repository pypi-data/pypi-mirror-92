import os
import boto3
import shutil
from python_cassandra_cli.aws_utils import AWSUtils

class RestoreSnapshotKeyspace(object):

    def __init__(self, s3, id, key, tag, keyspace, region, schema, snapshot_folder, host, user, password,
        cassandra_config_file, cassandra_keystore, cassandra_truststore, cassandra_port, ssl_connection, ssm_secret, secret_name, environment):

        self.s3 = s3
        self.id = id
        self.key = key
        self.tag = tag
        self.keyspace = keyspace
        self.region = region
        self.schema = schema
        self.snapshot_folder = snapshot_folder
        self.host = host
        self.user = user
        self.password = password
        self.cassandra_config_file = cassandra_config_file
        self.cassandra_keystore = cassandra_keystore
        self.cassandra_truststore = cassandra_truststore
        self.cassandra_port = cassandra_port
        self.ssl_connection = ssl_connection
        self.ssm_secret = ssm_secret
        self.secret_name = secret_name
        self.environment = environment

    def restore_snapshot_keyspace(self) :

        aws_utils = AWSUtils(self.id, self.key)

        client_s3 = aws_utils.s3_client()

        client_ssm = aws_utils.ssm_client(self.id, self.key, self.region)

        # copy snanpshot folder from s3 bucket into local system
        list=client_s3.list_objects(Bucket=self.s3, Prefix=self.snapshot_folder)['Contents']
        for s3_key in list:
            s3_object = s3_key['Key']
            # print object
            # print(s3_object)
            # creating folder for object
            os.makedirs(os.path.dirname(s3_object), exist_ok=True)
            # copy object from s3 to local folder
            client_s3.download_file(self.s3, s3_object, s3_object)

        if self.schema:
            if self.ssm_secret:
                print('Getting secrets from SSM')
                parameter = client_ssm.get_parameter(Name=self.secret_name, WithDecryption=True)
                value_array = parameter['Parameter']['Value'].split('\n')
                result_dict={}
                for item in value_array:
                    result_dict[item.partition('=')[0]]=item.partition('=')[2]
                user=result_dict['USER']
                password=result_dict['PASSWORD']
            else:
                user=self.user
                password=self.password

            print('Creating keyspace schema');

            cmd_cql = "cqlsh --cqlversion='3.4.4' {0} -u {1} -p {2} -e \"SOURCE '{3}/{4}_{5}_schema.cql'\"".format(self.host, user, password, self.snapshot_folder, self.keyspace, self.environment)
            # print(cmd_cql);
            os.system(cmd_cql);

        # list folder with snapshots
        folder_list = os.listdir(self.snapshot_folder)
        for item in folder_list:
            # determine if object is directory
            if os.path.isdir(os.path.join(self.snapshot_folder,item)):
                # get table name
                table_name = item.partition('-')[0]
                # consruction vars for copying to temporary folder
                snapshot_folder = self.snapshot_folder + '/' + item + '/snapshots/' + self.tag
                copy_folder = self.keyspace + '/' + table_name;
                try:
                    # remove foler if it existed
                    shutil.rmtree(copy_folder)
                except:
                    print("Not able to delete folder tree '% s'. Seems like folder is not exist" % copy_folder)
                # copy snapshot folder to temporary folder
                shutil.copytree(snapshot_folder, copy_folder);
                print('Copying folder ...')
                # Loading data from snapashot to tables
                if self.ssm_secret:
                    print('Getting secrets from SSM')
                    parameter = client_ssm.get_parameter(Name=self.secret_name, WithDecryption=True)
                    value_array = parameter['Parameter']['Value'].split('\n')
                    result_dict={}
                    for item in value_array:
                        result_dict[item.partition('=')[0]]=item.partition('=')[2]
                    user=result_dict['USER']
                    password=result_dict['PASSWORD']
                else:
                    user=self.user
                    password=self.password
                if self.ssl_connection:
                    if user:
                        cmd_cql = "sstableloader --nodes {0} {1} -u {2} -pw {3} -f {4} -ks {5} -ts {6} -p {7}".format(
                            self.host, copy_folder, user, password, self.cassandra_config_file, self.cassandra_keystore, self.cassandra_truststore, self.cassandra_port)
                    else:
                        cmd_cql = "sstableloader --nodes {0} {1} -f {2} -ks {3} -ts {4} -p {5}".format(
                            self.host, copy_folder, self.cassandra_config_file, self.cassandra_keystore, self.cassandra_truststore, self.cassandra_port)
                    os.system(cmd_cql)
                else:
                    if user:
                        cmd_cql = "sstableloader --nodes {0} {1} -u {2} -pw {3}".format(self.host, copy_folder, user, password)
                    else:
                        cmd_cql = "sstableloader --nodes {0} {1}".format(self.host, copy_folder)
                    os.system(cmd_cql)
                # clean system from temporary folder
                shutil.rmtree(self.keyspace)
        shutil.rmtree(self.snapshot_folder)