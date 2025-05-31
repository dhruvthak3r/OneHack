
from transformers.transform_devfolio import transform_devfolio
from transformers.transform_unstop import transform_unstop,get_metadata_list
from transformers.transform_devpost import transform_devpost
from transformers.transform_dorahack import transform_dorahack

from prefect import task


@task
def orchestrate_transform_devfolio(data):
    return transform_devfolio(data)

@task
def orchestrate_transform_unstop(data):
    unstop_metadata_list = get_metadata_list(data)

    return transform_unstop(unstop_metadata_list)

@task
def orchestrate_transform_devpost(data):
    return transform_devpost(data)

@task
def orchestrate_transform_dorahacks(data):
    return transform_dorahack(data)

