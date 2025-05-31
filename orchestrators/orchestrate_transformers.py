from utils import read_json_file

from transformers.transform_devfolio import transform_devfolio
from transformers.transform_unstop import transform_unstop,get_metadata_list
from transformers.transform_devpost import transform_devpost
from transformers.transform_dorahack import transform_dorahack

from prefect import flow,task

@flow
def transform_hackathon_data(devfolio_data,unstop_data,devpost_data,dorahacks_data):

    """
    Flow to Transform the data extracted for respective platforms.
    """

    orchestrate_transform_devfolio(devfolio_data)

    orchestrate_transform_unstop(unstop_data)

    orchestrate_transform_devpost(devpost_data)

    orchestrate_transform_dorahacks(dorahacks_data)



@task
def orchestrate_transform_devfolio(data):
    transform_devfolio(data)

@task
def orchestrate_transform_unstop(data):
    unstop_metadata_list = get_metadata_list(data)

    transform_unstop(unstop_metadata_list)

@task
def orchestrate_transform_devpost(data):
    transform_devpost(data)

@task
def orchestrate_transform_dorahacks(data):
    transform_dorahack(data)



if __name__ == '__main__':

    devfolio_data = read_json_file('devfolio_hackathons.json')
    unstop_data = read_json_file('unstop_hackathons.json')
    devpost_data = read_json_file('devpost_hackathons.json')
    dorahacks_data = read_json_file('dorahacks_hackathons.json')

    transform_hackathon_data(devfolio_data,unstop_data,devpost_data,dorahacks_data)
