from crypt import methods
from flask import jsonify, redirect, render_template, request
from app import app,db
from app import models

from app.api.Game import *
from app.api.Dealer import *
from app.api.Card import *
from app.api.Player import *
from app.api.RoyalCard import *

from app.forms import LoginForm

player = ["mycc",100]

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
            global player 
            player = user.user_info()
            return redirect('/game')
    
    return render_template('login.html',error="The username or password you enter is not corrent. Please enter again")

@app.route("/register",methods=['POST'])
def register():
    username=request.form['username']
    password=request.form['password']

    users=models.User.query.all()
    for user in users:
        if username==user.username:
            return render_template('login.html',error="The username have been registered, Please use another one.")
    
    user=models.User(username,password,1000)
    db.session.add(user)
    db.session.commit()

    return redirect("/login")

@app.route("/game")
def game():
    return render_template('game.html',coin=player[1])

@app.route("/level")
def level():
    users = models.User.query.order_by(models.User.coin.desc()).all()

    level={}
    level["first_place"]=users[0].username
    level["first_place_c"]=users[0].coin
    level["second_place"]=users[1].username
    level["second_place_c"]=users[1].coin
    level["third_place"]=users[2].username
    level["third_place_c"]=users[2].coin

    three_top_name=[users[0].username,users[1].username,users[2].username]
    # if player.username in three_top_name:
    #     level["congrations"]="congrations"

    return render_template('level.html',level=level)



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
    game_info["pot"] = mygame.Pot

    game_info["state"] = mygame.state

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


    public_card = [card.name for card in mygame.PublicCard]
    print(public_card)
    # game_info["public"] = 

    print(game_info)
    return jsonify(game_info)

@app.route("/call")
def call():
    mygame.play("call",bet=0)

    game_info={}
    game_info["end"] = mygame.end
    game_info["player_coin"] = mygame.Player.coin
    game_info["pot"] = mygame.Pot

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    player_card = [card.name for card in mygame.PlayerCard]
    game_info["player_first_card"] = player_card[0]
    game_info["player_second_card"] = player_card[1]

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet

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

    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet
    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    game_info["all_action"] = mygame.action_list
    game_info["actions"] = mygame.actions

    if mygame.result>=0:
        game_info["result"] = "You Win " + str(mygame.result)
    else:
        game_info["result"] = "You Lost " + str(abs(mygame.result))

    print(game_info)

    return jsonify(game_info)

@app.route("/bet/",methods=['GET'])
def bet():
    betnumber=request.args.get('bet_number')

    mygame.play("bet",int(betnumber))
    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    game_info["player_bet"] = mygame.Player.bet

    game_info["all_action"] = mygame.action_list
    game_info["actions"] = mygame.actions
    

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
    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    game_info["all_action"] = mygame.action_list
    game_info["actions"] = mygame.actions
    print(game_info)

    return jsonify(game_info)

@app.route("/allin")
def allin():
    mygame.play("allIn",0)
    game_info={}
    game_info["player_coin"] = mygame.Player.coin
    game_info["player_bet"] = mygame.Player.bet
    game_info["dealer_bet"] = mygame.Dealer.bet

    game_info["end"] = mygame.end

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

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

    public_card = [card.name for card in mygame.PublicCard]
    game_info["public_card"] = public_card

    dealer_card = [card.name for card in mygame.DealerCard]
    game_info["dealer_first_card"] = dealer_card[0]
    game_info["dealer_second_card"] = dealer_card[1]

    if mygame.result>=0:
        game_info["result"] = "You Win " + str(mygame.result)
    else:
        game_info["result"] = "You Lost " + str(abs(mygame.result))

    return jsonify(game_info)










