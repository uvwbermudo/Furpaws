from flaskr import get_error_items, get_form_fields, mysql, socketio
from flaskr.models import Users, Conversations, HasConversations, Messages
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, session
from flask_login import current_user, login_required
from . import msgs
import wtforms_json
import json
wtforms_json.init()
import datetime
from flask_socketio import send, join_room, emit, leave_room, disconnect

rooms = {}

@msgs.route('/messages', methods=['GET'])
@login_required
def message_home():
    return render_template('messages/messages_home.html')


@msgs.route('/messages/start-conversation', methods=['POST'])
@login_required
def start_convo():
    cursor = mysql.connection.cursor()
    today = datetime.datetime.now()
    recipient = request.form['recipient']
    other_user = Users.query_get(tag=recipient)
    partner_name = f"{other_user.first_name} {other_user.last_name}"
    main_name = f"{current_user.first_name} {current_user.last_name}"
    if not other_user:
        flash('Recipient does not exist', category='error')
        return redirect('/messages')
    members = [recipient, current_user.tag]
    members.sort()
    member1 = Users.query_get(members[0])
    member2 = Users.query_get(members[1])
    has_active = HasConversations.get_active(main_tag=current_user.tag, partner_tag=other_user.tag)
    if has_active:
        flash(f'You have an ongoing conversation with {other_user.tag}', category='error')
        return redirect('/messages')


    new_convo = Conversations(member1=member1.tag, member2=member2.tag)
    last_id=new_convo.add()
    has_convo1 = HasConversations(main_tag=current_user.tag, partner_tag=recipient, conversation_id=last_id, last_updated=today, partner_name=partner_name).add()
    has_convo1 = HasConversations(main_tag=recipient, partner_tag=current_user.tag, conversation_id=last_id, last_updated=today, partner_name=main_name).add()
    message = request.form['message']
    new_message = Messages(message_content=message, conversation_id=last_id, sender=current_user.tag, date_sent=today)
    new_message.add()
    mysql.connection.commit()
    return redirect('/messages')

@msgs.route('/messages/get-conversations/<tag>', methods=['GET'])
@login_required
def get_convos(tag):
    if request.args:
        filter = request.args['searchbar']
        if not filter:
            convos = HasConversations.query_filter(main_tag=tag)
        else:
            convos = HasConversations.query_filter(partner=filter)
    else:
        convos = HasConversations.query_filter(main_tag=tag)
    return render_template('/messages/macros/conv_list.html', convos=convos)


@msgs.route('/messages/delete-convo', methods=['POST'])
@login_required
def delete_convo():
    today = datetime.datetime.now()
    has_id = request.form['has_id']
    convo_id = request.form['convo_id']
    message = f"{current_user.tag} has deleted the conversation on their end. They can no longer receive your messages from here. if you would like to message them. Start a new conversation with them. Deleting this conversation deletes all the messages in here forever."
    new_message = Messages(message_content=message, conversation_id=convo_id, sender=current_user.tag, date_sent=today)
    remaining = HasConversations.query_filter(convo_id=convo_id)
    print(remaining)
    HasConversations.deactivate(id=has_id)
    HasConversations.delete(id=has_id)
    new_message.add()
    mysql.connection.commit()
    if len(remaining) == 1:
        Conversations.delete(convo_id)
    mysql.connection.commit()
    return redirect('/messages')


@msgs.route('/messages/get-chat-box/<has_id>/<convo_id>', methods=['GET'])
@login_required
def get_chat_box(has_id,convo_id):
    convo = Conversations.query_get(convo_id)
    has_convo = HasConversations.query_get(id=has_id)
    HasConversations.bump_open(convo_id=convo_id, main_tag=current_user.tag)
    mysql.connection.commit()
    other_user = has_convo.partner_details
    return render_template('messages/chat_box.html', other_user=other_user, convo_id=convo_id, convo=convo, has_id=has_id)


@msgs.route('/messages/search-recipients/<filter>', methods=['GET'])
@login_required
def search_recipient(filter):
    user = Users.query_get(filter)
    if user:
        return Response(status=200)
    return Response(status=408)

@socketio.on('message')
def handle_message(data):
    print(session)
    data = json.loads(data)
    message = data['content']
    room = data['room']
    sender = data['sender'] 
    today = datetime.datetime.now()
    new_message = Messages(message_content=message, conversation_id=room, sender=sender, date_sent=today)
    new_message.add()
    HasConversations.bump(convo_id=room, partner_tag=sender)
    mysql.connection.commit()
    if message == 'User Connected':
        return
    emit('message', {'sender':sender, 'content':message}, to=room)

@socketio.on('join room')
def handle_join_room(data):
    room = data['room']
    # Check if the user is already in a room
    # Join the new room
    join_room(room)
    # Store the current conversation in the session
    session['current_room'] = room


@socketio.on('leave room')
def handle_leave_conversation(data):
    # Leave the current room
    print(session)
    room = data['room']
    print('LEAVING ROOM', room)
    leave_room(room)
    session.pop('current_room')
    # Remove current conversation from the session