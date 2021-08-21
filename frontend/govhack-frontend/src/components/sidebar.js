import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import { Divider } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';

export class SideBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pType: '',
            youtubeInterests: props.youtubeInterests,
            selectedYoutubeInterests: [],
        };
        this.handlePTypeInputChange = this.handlePTypeInputChange.bind(this);
    }

    handlePTypeInputChange(event) {
        this.setState({ pType: event.target.value });
    }

    render() {
        return (
            <div style={{
                width: "20vw",
                display: "flex",
            }}>

                <form style={{ display: 'flex', flexDirection: 'column', margin: '15px 32px', width: '100%', overflowY:"scroll" }}>
                    <TextField
                        id="p-type"
                        label="Personality type"
                        fullWidth
                        value={this.state.pType}
                        margin="normal"
                        style={{ marginTop: '5px' }}
                        onChange={this.handlePTypeInputChange}

                    />
                    <Button variant="contained" color="primary"
                            style={{ marginTop: '10px' }}

                            onClick={() => this.props.onSubmitPersonalityType(this.state.pType)}
                    >
                        Submit
                    </Button>
                    <Typography color="textSecondary" >

                    <p>__________________________</p>
                    </Typography>
                    <p><b>YouTube Interests</b></p>

                    {this.props.youtubeInterests.map((v, i) => {
                        return (
                            <div key={i} style={{textAlign: "left"}}>
                            <Checkbox onClick={() => this.props.checkboxClicked(v)}/> {v}
                            </div>
                        )
                    })}
                </form>


            </div>
        )
    }
}
