import boto3
def get_data(user,s3_id,s3_key):
    s3 = boto3.client(
        's3',aws_access_key_id=s3_id,aws_secret_access_key =s3_key
    )
    external_file_list = []
    internal_file_list = []
    output_json = {}
    res_list=[]
    bucket_name="datainsightsplatform"
    external_data_path = "Data_Market/" + user + "/DatasetSelection/"
    internal_data_path = "AI_ML/" + user + "/Dataset_selection/"
    for external_obj in s3.list_objects_v2(Bucket=bucket_name, Prefix=external_data_path)['Contents']:
        external_file_list.append(external_obj['Key'])
    for internal_obj in s3.list_objects_v2(Bucket=bucket_name, Prefix=internal_data_path)['Contents']:
        internal_file_list.append(internal_obj['Key'])
    output_json['Internal_datasource'] = internal_file_list
    output_json['External_datasource'] = external_file_list
    for i in output_json['Internal_datasource']:
        res_list.append(i)
    return res_list