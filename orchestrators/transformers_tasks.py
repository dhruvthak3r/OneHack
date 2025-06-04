
from transformers.transform_devfolio import transform_devfolio
from transformers.transform_unstop import transform_unstop,get_metadata_list
from transformers.transform_devpost import transform_devpost
from transformers.transform_dorahack import transform_dorahack

from prefect import task


@task(log_prints=True, retries=3, retry_delay_seconds=5)
def orchestrate_transform_devfolio(filename):
    return transform_devfolio(filename)

@task(log_prints=True, retries=3, retry_delay_seconds=5)
def orchestrate_transform_unstop(filename):
    unstop_metadata_list = get_metadata_list(filename)

    return transform_unstop(unstop_metadata_list)

@task(log_prints=True, retries=3, retry_delay_seconds=5)
def orchestrate_transform_devpost(filename):
    return transform_devpost(filename)

@task(log_prints=True, retries=3, retry_delay_seconds=5)
def orchestrate_transform_dorahacks(filename):
    return transform_dorahack(filename)

