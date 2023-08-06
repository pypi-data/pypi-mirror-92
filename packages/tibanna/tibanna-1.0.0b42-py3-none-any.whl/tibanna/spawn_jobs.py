from tibanna.utils import create_jobid
from tibanna.ec2_utils import UnicornInput
from tibanna.core import API


def run_batch_workflows(input_json_list):
    for input_json in input_json_list:
        API().run_workflow(input_json)

