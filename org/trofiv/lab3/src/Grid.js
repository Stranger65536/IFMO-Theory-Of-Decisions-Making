import React, {Component} from "react";
import _ from "underscore";
import Checkbox from 'material-ui/Checkbox';

export default class Grid extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            size: props.size
        }
    }

    drawGrid = (size) => {
        const elements = [];
        _.each(_.range(size), function (row) {
            _.each(_.range(size), function (column) {
                elements.push(
                    <div className="cell"
                         key={row + '.' + column}><Checkbox/></div>);
            });
            elements.push(<br key={row}/>);
        });
        return elements;
    };

    gridSize = (size) => {
        return 36 * size;
    };

    componentWillReceiveProps(props) {
        this.setState({
            ...this.state,
            size: props.size
        });
    }

    render() {
        const size = this.gridSize(this.state.size);
        return (
            <div className="grid"
                 style={{width: size, height: size}}>
                {this.drawGrid(this.state.size)}
            </div>
        )
    }
}