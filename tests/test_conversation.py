# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import datetime
import os

from mock import patch, call, Mock

from connect.models import Conversation, ConversationMessage, User, Fulfillment
from .common import Response, load_str

conversation_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'conversation.json'))

add_message_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'add_message_response.json'))


def test_conversation_attributes():
    # type: () -> None
    conversation = Conversation.deserialize(conversation_contents)
    assert isinstance(conversation, Conversation)
    assert conversation.id == 'CO-750-033-356'
    assert conversation.instance_id == 'LST-038-662-242'
    assert conversation.created == datetime.datetime(2018, 12, 18, 12, 49, 34)
    assert conversation.topic == 'Topic'
    assert isinstance(conversation.messages, list)
    assert len(conversation.messages) == 1

    message = conversation.messages[0]
    assert isinstance(message, ConversationMessage)
    assert message.id == 'ME-506-258-087'
    assert message.conversation == conversation.id
    assert message.created == datetime.datetime(2018, 12, 18, 13, 3, 30)
    assert isinstance(message.creator, User)
    assert message.creator.id == 'UR-922-977-649'
    assert message.creator.name == 'Some User'
    assert message.text == 'Hi, check out'

    assert isinstance(conversation.creator, User)
    assert conversation.creator.id == 'UR-922-977-649'
    assert conversation.creator.name == 'Some User'


@patch('requests.post')
def test_add_message(post_mock):
    # type: (Mock) -> None
    post_mock.return_value = Response(True, add_message_response, 200)

    text = 'Hi, please see my listing request'

    conversation = Conversation.deserialize(conversation_contents)
    message = conversation.add_message(text)

    post_mock.assert_called_with(
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        json={'text': text},
        timeout=300,
        url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356/messages')

    assert isinstance(message, ConversationMessage)
    assert message.id == 'ME-000-000-000'
    assert message.conversation == 'CO-000-000-000'
    assert message.created == datetime.datetime(2018, 12, 18, 13, 3, 30)
    assert isinstance(message.creator, User)
    assert message.creator.id == 'UR-000-000-000'
    assert message.creator.name == 'Some User'
    assert message.text == text


@patch('requests.get')
def test_get_conversation_ok(get_mock):
    # type: (Mock) -> None
    get_mock.side_effect = [
        Response(True, '[' + conversation_contents + ']', 200),
        Response(True, conversation_contents, 200)
    ]

    request = Fulfillment(id='PR-0000-0000-0000')
    conversation = request.get_conversation()

    assert get_mock.call_count == 2
    get_mock.assert_has_calls([
        call(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': request.id},
            timeout=300,
            url='http://localhost:8080/api/public/v1/conversations'),
        call(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url='http://localhost:8080/api/public/v1/conversations/' + conversation.id)
    ])

    assert isinstance(conversation, Conversation)


@patch('requests.get')
def test_get_conversation_empty(get_mock):
    # type: (Mock) -> None
    get_mock.return_value = Response(True, '[]', 200)

    request = Fulfillment(id='PR-0000-0000-0000')
    conversation = request.get_conversation()

    assert get_mock.call_count == 1
    get_mock.assert_has_calls([
        call(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': request.id},
            timeout=300,
            url='http://localhost:8080/api/public/v1/conversations')
    ])

    assert conversation is None


@patch('requests.get')
def test_get_conversation_bad_deserialize(get_mock):
    # type: (Mock) -> None
    get_mock.side_effect = [
        Response(True, '[' + conversation_contents + ']', 200),
        Response(True, '', 200)
    ]

    request = Fulfillment(id='PR-0000-0000-0000')
    conversation = request.get_conversation()

    assert get_mock.call_count == 2
    get_mock.assert_has_calls([
        call(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'instance_id': request.id},
            timeout=300,
            url='http://localhost:8080/api/public/v1/conversations'),
        call(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url='http://localhost:8080/api/public/v1/conversations/CO-750-033-356')
    ])

    assert conversation is None
