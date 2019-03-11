import React, { Component, Fragment } from 'react';
import Square from './Square';
import './Square.css';
import { Images } from './img/Images'
import axios from "axios";

class Board extends Component {
    constructor(props) {
        super(props);

        this.state = {
            rows: props.rows,
            columns: props.columns,
            created: false,
            guiString: null,
            guiBoard: null
        }
    }

    componentDidMount() {
        // If the game is being continued and game has been started on it, then update board. If not, initialize empty GUI board
        if (this.props.loaded_from_server && this.props.game_guiString != "") {
            console.log("In here?")
            this.updateBoard(this.props.game_guiString)

        } else {
            let board = [] // create array of elements to create a grid
            for (let i = 0; i < this.state.rows; i++) {
                let boardRow = []
                for (let j = 0; j < this.state.columns; j++) {
                    boardRow.push(<Square row={i} column={j} type={"E"} key={`(${i}, ${j})`} getSquare={this.props.getSquare} updateBoard={this.updateBoard} />)
                }
                board.push(<div className="row" key={i}>{boardRow}</div>);
            }
            this.setState({ guiBoard: board });
        }
       
    }

    // updating the board according to the guiString passed in
    updateBoard = (guiString, answer) => {
        if (guiString.length > 1) {
            let board = [] // create array of elements to create a grid
            let guiArray = guiString.split(" ");
            var k = 0; // increment one dimensional guiArray

            for (let i = 0; i < this.state.rows; i++) {
                let boardRow = []
                for (let j = 0; j < this.state.columns; j++) {
                    boardRow.push(<Square row={i} column={j} type={guiArray[k]} key={`(${i}, ${j})`} getSquare={this.props.getSquare} updateBoard={this.updateBoard}/>)
                    k++;
                }
                
                board.push(<div className="row" key={i}>{boardRow}</div>);
                this.setState({ guiString: guiString, guiBoard: board })
            }
        } else {
           
        }
    }

    render() {
        return(
            <Fragment>
                {this.state.guiBoard && (this.state.guiBoard)}
            </Fragment>         
        )
    }
}

export default Board;