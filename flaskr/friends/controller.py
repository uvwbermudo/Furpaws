from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from . import friends
import wtforms_json
from flaskr import mysql
from flaskr.models import FriendRequests, Users, HasFriends
wtforms_json.init() 


@friends.route('/friends/<tag>', methods=['GET','POST'])
@login_required
def friends_page(tag):
    user = Users.query_get(tag=tag)
    all_friends = HasFriends.query_filter(account_tag=current_user.tag)
    friend_names = []
    for i in all_friends:
        friend_names.append(i.friend.first_name + ' ' + i.friend.last_name)
    return render_template('friends/friends.html/', tag=tag, all_friends=all_friends, friend_names=friend_names, user=user)

@friends.route('/friend-requests/<tag>', methods=['GET','POST'])
@login_required
def friend_requests(tag):
    requests = [FriendRequests.query_get(account_tag=tag)]
    request_details = FriendRequests.query_filter(account_tag=tag)
    user = Users.query_get(tag=tag)
    request_names = []
    for i in request_details:
        request_names.append(i.requester.first_name + ' ' + i.requester.last_name)
    return render_template('friends/friend-requests.html/', tag=tag, requests=requests, user=user, request_names=request_names)

@friends.route("/send-friend-request/<tag>/<current_user>", methods=['POST','DELETE'])
@login_required
def send_friend_request(tag, current_user):
    if request.method == 'POST':
        print(tag, current_user)
        new_friend_request = FriendRequests(account_tag=tag, sender_tag=current_user)
        new_friend_request.add()
        mysql.connection.commit()
        return render_template('friends/macros/send-friend-request.html', tag=tag, current_user=current_user)
    elif request.method == 'DELETE':
        friend_request = FriendRequests.query_get(sender_tag=current_user, account_tag=tag)
        FriendRequests.delete(friend_request.id)
        mysql.connection.commit()
        return render_template('friends/macros/cancel-friend-request.html',tag=tag, current_user=current_user)


        

@friends.route("/accept-friend-request/<id>", methods=['POST'])
@login_required
def accept_friend_request(id):
    if request.method == 'POST':
        friend_request = FriendRequests.query_get(id=id)
        FriendRequests.delete(friend_request.id)
        mysql.connection.commit()
        new_friend = HasFriends(account_tag=current_user.tag, friend_tag=friend_request.sender_tag)
        new_friend.add()
        new_friend = HasFriends(account_tag=friend_request.sender_tag, friend_tag=current_user.tag)
        new_friend.add()
        mysql.connection.commit()
        flash(f'Amazing! You are now friends with {friend_request.sender_tag}!', category='success')
    return redirect(url_for('friends.friend_requests', tag=current_user.tag))
    

@friends.route("/decline-friend-request/<id>", methods=['POST'])
@login_required
def decline_friend_request(id):
    if request.method == 'POST':
        friend_request = FriendRequests.query_get(id=id)
        FriendRequests.delete(friend_request.id)
        mysql.connection.commit()
        flash(f'Request declined successfully', category='success')
    return redirect(url_for('friends.friend_requests', tag=current_user.tag))
