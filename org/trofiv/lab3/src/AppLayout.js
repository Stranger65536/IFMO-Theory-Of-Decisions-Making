import React, {Component} from "react";
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import {emcMuiTheme} from "./Common";
import Grid from "./Grid";
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';

export default class AppLayout extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            size: this.getSize(),
        }
    }

    getSize = () => {
        const hash = window.location.hash;
        if (hash.startsWith("#") && hash.length > 1) {
            return Number(hash.substr(1));
        }
    };

    updateSize = (e, index, value) => {
        window.location.hash = '#' + value;
        this.setState({...this.state, size: value});
    };

    render() {
        return (
            <div style={{width: "100%", height: "100%"}}>
                <MuiThemeProvider muiTheme={emcMuiTheme}>
                    <div>
                        <AppBar title="Lab03"
                                className="bar"
                                iconElementRight={
                                    <SelectField
                                        floatingLabelText="Board size"
                                        value={this.state.size}
                                        onChange={this.updateSize}>
                                        <MenuItem value={2}
                                                  primaryText="2x2"/>
                                        <MenuItem value={3}
                                                  primaryText="3x3"/>
                                        <MenuItem value={4}
                                                  primaryText="4x4"/>
                                        <MenuItem value={5}
                                                  primaryText="5x5"/>
                                    </SelectField>}/>
                        <Grid size={this.state.size}/>
                    </div>
                </MuiThemeProvider>
            </div>
        )
    }
}