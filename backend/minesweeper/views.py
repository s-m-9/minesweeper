# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BoardSerializer
from django.http import HttpResponse, HttpRequest
from .models import Board
from game import board
import json

# Create your views here.

gameBoard = board.Board(9, 9, 10)
gameOver = False

class BoardView(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    # all boards
    queryset = Board.objects.all()
    

    # gameBoard = board.Board(9, 9, 10)
    global gameBoard
    gameBoard.createBoard()
    # if request.method == 'POST':

# create a new game
def createGame(request):
    global gameBoard
    if request.method == 'POST':
        # gets request and turns it into json to get it's values
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        rows = body['rows']
        columns = body['columns']
        num_of_bombs = body['num_of_bombs']
        
        gameBoard = board.Board(int(rows), int(columns), int(num_of_bombs))
        gameBoard.createBoard()
        
        return HttpResponse("game reset")

# for returning players, populate GUI board on front end
def populateBoard(request):
    global gameBoard
    if request.method == 'POST':
        # gets request and turns it into json to get it's values
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        state = body['game_state']
        guiString = body['game_guiString']

        # populate the board with the guistring and its state
        boardString = gameBoard.populateBoard(state, guiString)

        return HttpResponse(boardString)

# where the game is run
def play(request):
    global gameBoard
    if request.method == 'POST':
        answer = None
        
        # gets request and turns it into json to get it's values
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        row = body['row']
        column = body['column']
        
        answer = gameBoard.click(row, column)
        winCondition = json.loads(answer)["answer"]

        # if the game is over, the player can't put anymore squares
        if winCondition == "YOU WIN!" or winCondition == "BOMB! YOU LOSE!":
            gameBoard.lockGame()

        return HttpResponse(answer)

def reset(request):
    global gameBoard
    gameBoard.unlockGame()
    return HttpResponse("game reset")

