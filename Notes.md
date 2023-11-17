# Notes
_just for storing thoughts while I work on the CW_

- Requires 3.10 or higher due to | symbol in type hinting
- Requires copy library for deep copying (not sure if python default or not)
- check whether input coordinates start at 0, whether they are inputted on one line etc, or if free to interpret
- Should there be an entry point for AI game loop?

## Requirements
- Flask


### Flask 

This part is the variables required to render the placement.html file
```
@app.route('/placement', methods=['GET','POST'])
def index():

    if request.method =='POST':
        data = request.data
        json_data = request.get_json()
        print("JSON Data:", json_data)
        return json_data

  

    return render_template('placement.html',board_size =5, ships= {'Ship1':5,'Ship2':4,'Ship3':3,'Ship4':2})


```
board size doesnt work properly?
Issue with rendering different board sizes in gameplay.html too fixed it tho :)

This part is the variables required to render the gameplay.html file
```
 return render_template('gameplay.html',player_board = board)
```


This part handles when a player attacks
```
@app.route('/attack')
def attacked():
    x= request.args.get('x')
    y = request.args.get('y')
    print('attacked',x,y)
    return {'hit':True,'AI_Turn':(0,0)}
```

## Next Code TODO
- Add an HTML intro screen (difficulty / board size options, stormy?)
- Multiplayer

##  When done with code
1. Test
2. Pylint 
3. Document
4. README file 
5. Sort out licensing


## difficulties
:param difficulty: What algorithm to choose a point: 0 is pure random, 1 is random but wont choose same twice
       2 is medium_ai guessing with random blind guesses, 3 is medium_ai with intelligent blind guesses, 4 is intelligent_ai