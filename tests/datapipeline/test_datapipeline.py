"""Verify AWS Data Pipeline Creation."""
from unittest import mock
import pytest

import copy
import awscli.customizations.datapipeline.translator
from foremast.datapipeline.datapipeline import AWSDataPipeline

GOOD_DEF = 	{
        "objects": [],
        "parameters": [],
        "values": {}
        }

BAD_DEF = 	{
        "no_object": [],
        "parameters": [],
        "values": {}
        }

TEST_PROPERTIES = {
    'test_env': {
        'datapipeline': {
            'name': 'Test Pipeline',
            'description': "this is a test",
            'json_definition': GOOD_DEF
        }
    }
}

@mock.patch('foremast.datapipeline.datapipeline.boto3.Session.client')
@mock.patch('foremast.datapipeline.datapipeline.get_details')
@mock.patch('foremast.datapipeline.datapipeline.get_properties')
def test_create_datapipeline(mock_get_properties, mock_get_details, mock_boto3):
    """Check data pipeline creation"""
    generated = {"project": "test"}
    properties = copy.deepcopy(TEST_PROPERTIES)
    mock_get_details.return_value.data = generated
    mock_get_properties.return_value = properties
    mock_boto3.return_value.create_pipeline.return_value = { 'pipelineId': '1234'}

    dp = AWSDataPipeline(app='test_app', env='test_env', region='us-east-1', prop_path='other')
    dp.create_datapipeline()
    assert dp.pipeline_id == '1234'

@mock.patch('foremast.datapipeline.datapipeline.boto3.Session.client')
@mock.patch('foremast.datapipeline.datapipeline.get_details')
@mock.patch('foremast.datapipeline.datapipeline.get_properties')
def test_good_set_pipeline_definition(mock_get_properties, mock_get_details, mock_boto3):
    """Tests that good pipeline definition is set correctly"""
    generated = {"project": "test"}
    properties = copy.deepcopy(TEST_PROPERTIES)
    mock_get_details.return_value.data = generated
    mock_get_properties.return_value = properties

    good_dp = AWSDataPipeline(app='test_app', env='test_env', region='us-east-1', prop_path='other')
    good_dp.pipeline_id='1'
    result = good_dp.set_pipeline_definition()
    assert result == None


@mock.patch('foremast.datapipeline.datapipeline.boto3.Session.client')
@mock.patch('foremast.datapipeline.datapipeline.get_details')
@mock.patch('foremast.datapipeline.datapipeline.get_properties')
def test_bad_set_pipeline_definition(mock_get_properties, mock_get_details, mock_boto3):
    """Tests that bad pipeline definition is caught"""
    generated = {"project": "test"}
    properties = copy.deepcopy(TEST_PROPERTIES)
    properties['test_env']['datapipeline']['json_definition'] = BAD_DEF
    mock_get_details.return_value.data = generated
    mock_get_properties.return_value = properties

    bad_dp = AWSDataPipeline(app='test_app', env='test_env', region='us-east-1', prop_path='other')
    bad_dp.pipeline_id='1'
    with pytest.raises(awscli.customizations.datapipeline.translator.PipelineDefinitionError):
        bad_dp.set_pipeline_definition()

@mock.patch('foremast.datapipeline.datapipeline.boto3.Session.client')
@mock.patch('foremast.datapipeline.datapipeline.get_details')
@mock.patch('foremast.datapipeline.datapipeline.get_properties')
def test_get_pipeline_id(mock_get_properties, mock_get_details, mock_boto3):
    """Tests getting the pipeline ID from boto3"""
    test_pipelines = [{'pipelineIdList': [
        {
            "name": "Test Pipeline",
            "id": "1234"
        },
        {
            "name": "Other",
            "id": "5678"
        }
        ],
        "hasMoreResults": False 
        }]
    generated = {"project": "test"}
    properties = copy.deepcopy(TEST_PROPERTIES)
    mock_get_details.return_value.data = generated
    mock_get_properties.return_value = properties
    mock_boto3.return_value.get_paginator.return_value.paginate.return_value = test_pipelines

    dp = AWSDataPipeline(app='test_app', env='test_env', region='us-east-1', prop_path='other')
    dp.get_pipeline_id()
    assert dp.pipeline_id == '1234'
