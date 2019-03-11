import React, { Component, Fragment } from 'react';
import './App.css';
import Board from './Board';
import axios from "axios";

class Game extends Component {

    constructor(props) {
        super(props)
        this.state = {
            boardData: null,
            lastPositionRow: null,
            lastPositionCol: null,
            created: false,
            game_state: "_-",
            game_guiString: "",
            id: this.props.match.params.id,
            game_exists: true,
            loaded_from_server: false,
            game_answer: null
        }
    }

    componentDidMount() {
        if (this.state.id == null ) { // New Game Condition
            // create board entry on server, currently hardcoded
            var id = Math.random().toString(36).substring(7);
            var board = JSON.stringify({
                game_columns: 9,
                game_code: id.toString(),
                game_num_of_bombs: 10,
                game_rows: 9,
                game_state: "_-"
            });

            // sending board to server
            axios.post("http://localhost:8000/game/minesweeper/", board, {
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                this.setState({ boardData: response.data, id: response.data.id})
                this.getBoard();
                console.log(response.data)
            })
            .catch(err => console.error(err));

            this.setState({created: true})
            
        } else { // If ther is an id present in link
            // unlock game so player can click again
            axios.get(`/game/reset`)
            .then(response => {
                //  populate the board with moves
                return axios.get(`/game/minesweeper/${this.state.id}`)
            })
            .then(response => {
                this.setState({ 
                    boardData: response.data, 
                    game_state: response.data.game_state, 
                    game_guiString: response.data.game_guiString, 
                    loaded_from_server: true}) 
                return axios.post(`/game/populate/`, {
                    game_state: response.data.game_state,
                    game_guiString : response.data.game_guiString
                });
            })
            .then(response => {
                // console.log(response)
            })
            .catch(err => {
                // No board matching id was found on the server
                this.setState({game_exists: false}) 
                console.log(err)
            });

        }
    }

    getBoard = () => {
        // returns the game board
        axios.get(`/game/minesweeper/${this.state.id}`)
            .then(response => this.setState({ id: response.data.id }))
            .catch(err => console.log(err));
    }

    // getting the the last clicked square's coordinates and message sent in response
    getSquare = (pos, guiString, answer) => {

        // sending the state of the board and snapshot of GUI to server
        this.setState({ lastPositionRow: pos.row, lastPositionCol: pos.column, game_answer: answer })
        var data = JSON.stringify({
            game_state: this.state.game_state + `${pos.row},${pos.column}-`,
            game_guiString: guiString
        });

        axios.put(`/game/minesweeper/${this.state.id}/`, data, {
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            this.setState({ lastPositionRow: pos.row, lastPositionCol: pos.column, game_state: response.data.game_state })
        })
        .catch(err => console.log(err));
    }

    // creating a new game
    reset = (ev) => {
        
        var data = JSON.stringify({
            rows: 9,
            columns: 9,
            num_of_bombs: 10
        });

        return axios.post(`/game/create/`, data) 
                .then(response => {
                    // sending back to the root link and refreshing the page to get a new board
                    this.props.history.push('/');
                    window.location.reload()
                    
                })
                .catch (err => {
                    console.log(err)
                });
        
    }

    // Displays Win or Lose message below gameboard if player wins or loses
    getStatusText = () => {
        var answer = this.state.game_answer
        if (answer == "BOMB! YOU LOSE!" || answer == "YOU WIN!")
            return answer
    }

    render() {
        // console.log(this.state.boardData)
        const { game_exists } = this.state;
        return (
            <Fragment>
                {
                    game_exists ?
                        (this.state.boardData && (
                            
                            <div>
                                <h1>MINESWEEPER</h1>
                                <h3>Game Saved at http://localhost:3000/{this.state.id}</h3>
                                <Board rows={this.state.boardData.game_rows} columns={this.state.boardData.game_columns} getSquare={this.getSquare} game_guiString={this.state.game_guiString} loaded_from_server={this.state.loaded_from_server} />
                                <h2>{this.getStatusText()}</h2>
                                <input type="button" value="New Game" onClick={this.reset} />
                            </div>
                            
                        ))
                    :   (
                            <div className="App">
                                <h1>Game Does Not Exist</h1>
                            </div>
                        )
                }
            </Fragment>
        );
    }
}

export default Game;