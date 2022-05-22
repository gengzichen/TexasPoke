from collections import UserList
from datetime import datetime
from flask import jsonify, redirect, render_template, request
from app import app,db
from app import models

from app.api.Game import *
from app.api.Dealer import *
from app.api.Card import *
from app.api.Player import *
from app.api.RoyalCard import *

from app.forms import LoginForm


@app.route("/")
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

@app.route("/login",methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/login",methods=['POST'])
def login_to():
    # form= LoginForm()
    username=request.form['username']
    password=request.form['password']
    users=models.User.query.filter_by(username=username).all()
    for user in users:
        if user.check_password(password):
            if user.last_login_time != datetime.now().strftime("%x"):
                user.coin +=1000
                user.last_login_time = datetime.now().strftime("%x")
                db.session.commit()
            global player 
            player = user.user_info()
            return redirect('/game')
    
    return render_template('login.html',error="The username or password you enter is not corrent. Please enter again")

@app.route("/logout")
def logout():
    return redirect("/login")

@app.route("/register",methods=['POST'])
def register():
    username=request.form['username']
    password=request.form['password']

    users=models.User.query.all()
    for user in users:
        if username==user.username:
            return render_template('login.html',error="The username have been registered, Please use another one.")
    if len(password)<8:
        return render_template('login.html',error="The password you create is too short. Please create again.")

    user = models.User(username,password,1000,time=datetime.now().strftime("%x"))
    db.session.add(user)
    db.session.commit()

    return redirect("/login")

@app.route("/game")
def game():
    
    return render_template('game.html',coin=player[1])

@app.route("/help")
def help():
    return render_template('help.html')

@app.route("/level")
def level():
    users = models.User.query.order_by(models.User.coin.desc()).all()

    i=0
    user_info_list =[]
    for user in users:
        i += 1
        user_info=user.get_user_info()
        user_info['no'] = i
        if user_info['username']==player[0]:
            user_info['isplayer']=True
        else:
            user_info['isplayer']=False

        user_info_list.append(user_info)

    
    print(user_info_list)

    return render_template('level.html',users=user_info_list)


    
#Start Game
@app.route("/nexthand")
def play():
    
    gamer = UserAccount(player[0],player[1])
    print(gamer.name)
    Player = gamer.newPlayer()
    dealer = Dealer()
    global mygame
    mygame = Game(Player, dealer)

    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    player[1]=mygame.Player.coin

    game_info["pot"] = mygame.Pot

    # game_info["state"] = mygame.state

    player_card = [card.name for card in mygame.PlayerCard]
    game_info["player_first_card"] = player_card[0]
    game_info["player_second_card"] = player_card[1]
    game_info["player_bet"] = mygame.Player.bet

    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]
    game_info["dealer_bet"] = mygame.Dealer.bet

    game_info["all_action"] = mygame.action_list
    game_info["actions"] = mygame.actions

    game_info["message"] = mygame.Dealer.message

    print(game_info)
    return jsonify(game_info)

@app.route("/call")
def call():
    mygame.play("call",bet=0)

    game_info={}
    game_info["end"] = mygame.end
    game_info["player_coin"] = mygame.Player.coin
    player[1]=mygame.Player.coin

    user=models.User.query.filter_by(username=player[0]).first()
    user.coin=mygame.Player.coin
    db.session.commit()

    game_info["pot"] = mygame.Pot

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    player_card = [card.name for card in mygame.PlayerCard]
    game_info["player_first_card"] = player_card[0]
    game_info["player_second_card"] = player_card[1]

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet

    game_info["player_message"] = mygame.Player.message
    game_info["dealer_message"] = mygame.Dealer.message

    if(mygame.end==False):
        game_info["all_action"] = mygame.action_list
        game_info["actions"] = mygame.actions
        print(game_info)
        return jsonify(game_info)
    
    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]

    if mygame.result>=0:
        game_info["result"] = "You Win" + str(mygame.result)
    else:
        game_info["result"] = "You Lost" + str(abs(mygame.result))


    return jsonify(game_info)

@app.route("/minbet")
def minbet():
    mygame.play("minBet",0)
    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    player[1]=mygame.Player.coin
    game_info["pot"] = mygame.Pot

    user=models.User.query.filter_by(username=player[0]).first()
    user.coin=mygame.Player.coin
    db.session.commit()

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet
    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    game_info["all_action"] = mygame.action_list
    game_info["actions"] = mygame.actions

    game_info["player_message"] = mygame.Player.message
    game_info["dealer_message"] = mygame.Dealer.message

    if mygame.result>=0:
        game_info["result"] = "You Win " + str(mygame.result)
    else:
        game_info["result"] = "You Lost " + str(abs(mygame.result))

    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]

    print(game_info)

    return jsonify(game_info)

@app.route("/bet/",methods=['GET'])
def bet():
    betnumber=request.args.get('bet_number')

    mygame.play("bet",int(betnumber))
    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    player[1]=mygame.Player.coin
    game_info["pot"] = mygame.Pot

    user=models.User.query.filter_by(username=player[0]).first()
    user.coin=mygame.Player.coin
    db.session.commit()


    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet

    game_info["all_action"] = mygame.action_list
    game_info["actions"] = mygame.actions

    game_info["player_message"] = mygame.Player.message
    game_info["dealer_message"] = mygame.Dealer.message

    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]
    

    if mygame.result>=0:
        game_info["result"] = "You Win " + str(mygame.result)
    else:
        game_info["result"] = "You Lost " + str(abs(mygame.result))

    print(game_info)


    return jsonify(game_info)

@app.route("/check")
def check():
    mygame.play("check",bet=0)
    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    player[1]=mygame.Player.coin
    game_info["pot"] = mygame.Pot

    user=models.User.query.filter_by(username=player[0]).first()
    user.coin=mygame.Player.coin
    db.session.commit()

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet


    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    game_info["all_action"] = mygame.action_list
    game_info["actions"] = mygame.actions

    game_info["player_message"] = mygame.Player.message
    game_info["dealer_message"] = mygame.Dealer.message

    if mygame.result>=0:
        game_info["result"] = "You Win " + str(mygame.result)
    else:
        game_info["result"] = "You Lost " + str(abs(mygame.result))

    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]


    print(game_info)

    return jsonify(game_info)

@app.route("/allin")
def allin():
    mygame.play("allIn",0)
    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    player[1]=mygame.Player.coin
    game_info["pot"] = mygame.Pot

    user=models.User.query.filter_by(username=player[0]).first()
    user.coin=mygame.Player.coin
    db.session.commit()

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet

    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    game_info["player_message"] = mygame.Player.message
    game_info["dealer_message"] = mygame.Dealer.message

    if(mygame.end==False):
        game_info["all_action"] = mygame.action_list
        game_info["actions"] = mygame.actions
        print(game_info)
        return jsonify(game_info)

    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]

    if mygame.result>=0:
        game_info["result"] = "You Win " + str(mygame.result)
    else:
        game_info["result"] = "You Lost " + str(abs(mygame.result))

    return jsonify(game_info)



@app.route("/fold")
def fold():
    mygame.play("fold",0)
    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    player[1]=mygame.Player.coin
    game_info["pot"] = mygame.Pot

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet

    user=models.User.query.filter_by(username=player[0]).first()
    user.coin=mygame.Player.coin
    db.session.commit()

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]

    game_info["player_message"] = mygame.Player.message
    game_info["dealer_message"] = mygame.Dealer.message

    if mygame.result>=0:
        game_info["result"] = "You Win " + str(mygame.result)
    else:
        game_info["result"] = "You Lost " + str(abs(mygame.result))

    return jsonify(game_info)

