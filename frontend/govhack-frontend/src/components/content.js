import {Card} from '@material-ui/core';
import {makeStyles} from '@material-ui/core/styles';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import {CardElement} from './card';
import React, {Component} from 'react';

export class Content extends Component {
    render() {
        return (
            <div style={{background: '#658dc6', display:"flex",
                justifyContent:"center",
                width:"80vw",
                overflowY: "scroll",
                flexWrap:"wrap",}}>
                {this.props.clientData.map((v, i) =>  {
                    return (<CardElement key={i} cardInfo={v}/>);
                })
                }
            </div>
        )
    }
}
