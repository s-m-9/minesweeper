import React, { Component } from 'react';
import { Images } from './img/Images'
import './Square.css'
import axios from "axios";
class Square extends Component {
    constructor(props) {
        super(props);

        this.state = {
            row: props.row,
            column: props.column,
            type: props.type,
            img_src: Images.squares.unturned_square,
        }
    }

    componentDidMount() {
        if (this.state.type == "H") { // Its been hit
            this.setState({ img_src: Images.squares.empty_hit_square})
        } else if (this.state.type.substring(0, 1) == "[") { // contains number
            if (this.state.type.charAt(1) == "1") {
                this.setState({ img_src: Images.squares.hit_square_1 })
            } else if (this.state.type.charAt(1) == "2") {
                this.setState({ img_src: Images.squares.hit_square_2 })
            } else if (this.state.type.charAt(1) == "3") {
                this.setState({ img_src: Images.squares.hit_square_3 })
            } else {
                this.setState({ img_src: Images.squares.hit_square_4 })
            }
        } else {
            this.setState({ img_src: Images.squares.unturned_square})
        }
    }

    componentWillReceiveProps(newProps) {
        // Update the square's hit status using incoming properties
        if (newProps.type == "H") { // its been hit
            this.setState({ type: newProps.type, img_src: Images.squares.empty_hit_square })
        } else if (newProps.type.substring(0, 1) == "[") { // contains number
            if (newProps.type.charAt(1) == "1") {
                this.setState({ type: newProps.type, img_src: Images.squares.hit_square_1 })
            } else if (newProps.type.charAt(1) == "2") {
                this.setState({ type: newProps.type, img_src: Images.squares.hit_square_2 })
            } else if (newProps.type.charAt(1) == "3") {
                this.setState({ type: newProps.type, img_src: Images.squares.hit_square_3 })
            } else {
                this.setState({ type: newProps.type, img_src: Images.squares.hit_square_4 })
            }
            
        } else {
            this.setState({ type: newProps.type, img_src: Images.squares.unturned_square })
        }
        
    }

    click = (ev) => {
        var guiString = null
        
        // sending the coordinates to server in order to see and update status of board. 
        // Resonse has the updated GUI as a String and status of square
        var row_col = JSON.stringify({
            row: this.state.row,
            column: this.state.column
        })
        axios.post(`/game/play/`, row_col,
            {
                headers: {
                    'Content-type': 'application/json',
                }
            })
            .then(response => {
                var answer = response.data.answer
                guiString = response.data.guiString
                
                if (answer == "BOMB! YOU LOSE!") {
                    this.setState({ img_src: Images.squares.bomb_square })
                    // sent up to Game to update the game's entry on server. Used if you want to play later.
                    this.props.getSquare({ row: this.state.row, column: this.state.column }, guiString, answer) 
                } else if (answer == "EmptySpot") {
                    this.props.updateBoard(response.data.guiString, response.data.answer)
                    this.props.getSquare({ row: this.state.row, column: this.state.column }, guiString, answer)
                } else if (answer == "GAME OVER!") {
                    // Do nothing
                } else {
                    if (answer == "1") {
                        this.setState({ img_src: Images.squares.hit_square_1 })
                    } else if (answer == "2") {
                        this.setState({ img_src: Images.squares.hit_square_2 })
                    } else if (answer == "3") {
                        this.setState({ img_src: Images.squares.hit_square_3 })
                    } else {
                        this.setState({ img_src: Images.squares.hit_square_4 })
                    }
                    this.props.getSquare({ row: this.state.row, column: this.state.column }, guiString, answer)
                }
            })
            .catch(err => console.log(err))
    }

    render() {
        return (
            <div className="column">
                <img src={this.state.img_src} onClick={this.click} className="square" alt="Square" />
            </div>
            
        )
    }
}

export default Square;