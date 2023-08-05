#-*-coding:utf-8 -*-
from os.path import expanduser
from gadgethiServerUtils.file_basics import *
from gadgethiServerUtils.exceptions import *
from gadgethiServerUtils.db_operations import *

from DodayUtils._dwrappers import *
import DodayUtils

import os
import boto3
from importlib import import_module

class DodayUtilManager:
	"""
	This is the main class for doday
	utility manager. 
	"""
	def __init__(self, db=False, desc="Doday Util Main", 
		yaml_exccondition=None, configs={}, config_path="", 
		init_modules='*', table_list=[]):

		self.doday_config = load_config(config_path)
		self.credentials_config = load_config(expanduser("~") + "/.dutils/credentials.yaml")

		init_log(self.doday_config["log_file_path"])

		self.desc = desc

		yaml_config = {}
		yaml_config.update(configs)
		yaml_config.update(self.doday_config)
		yaml_config.update(self.credentials_config)

		if yaml_exccondition:
			# Initialization if yaml exccondition is defined
			self.fetch_yamls(yaml_config, yaml_exccondition)

		# Initialize doday configuration
		initialize_doday_configs(yaml_config)

		if init_modules == '*': 
			# Initialize all util classes
			my_location = os.path.dirname(__file__)
			module_list = [file[:-3]
						   for file in os.listdir(my_location)
						   if os.path.splitext(file)[1] == '.py'
						   and file != '__init__.py' and file[0] != "_"
						   and file != 'DodayUtilManager.py']
		else:
			module_list = init_modules.copy()

		for mod in module_list:
			setattr(self, mod, getattr(DodayUtils, mod)(**yaml_config))

		if db:
			# db operations init
			generate_db_header(table_list)
			init_db_location(self.doday_config)

			# db_operation, connect to correct database specified
			connect_to_database()

		logging.info("*** DoDay Util Initialized ***")

	# Fetch yaml function
	# -----------------------
	def fetch_yamls(self, yaml_config, exceptcond=lambda :False):
		"""
		This is the helper function to fetch yamls from s3
		"""
		ACCESS_ID = yaml_config["aws_access_key_id"] 
		SECRET_KEY = yaml_config["aws_secret_access_key"] 
		
		# bucket and document location info
		bucket_name = yaml_config["yaml_s3_bucket"]
		s3_folder_header = yaml_config["yaml_s3_folder"] #"doday_yamls/"
		local_folder_header = yaml_config["yaml_local_folder"] #"sample_menu/"

		# database ini
		database_ini_path = yaml_config["s3_database_ini_path"] #"database_ini/database.ini"
		database_ini_local_path = yaml_config["local_database_ini_path"] #"util/database.ini"

		s3 = boto3.client('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)
		objects = s3.list_objects(Bucket=bucket_name, Prefix=s3_folder_header)["Contents"]
		print("Pulling Yamls....")
		for obj in objects:
			obj_name = obj["Key"].replace(s3_folder_header, "")
			if exceptcond(obj_name=obj_name):
				continue
			print(obj_name)
			s3.download_file(bucket_name, s3_folder_header+obj_name, local_folder_header+obj_name)

		# Also fetch database ini here -> no need to put the path to config here -> database ini should also be in util/
		s3.download_file(bucket_name, database_ini_path, database_ini_local_path)

