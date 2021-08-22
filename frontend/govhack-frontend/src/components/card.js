import {Card} from '@material-ui/core';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import React, {Component} from 'react';
import youtube from './youtube.svg';
import personality from './personaility.svg';

const JEDI_URL = "https://www.nationalskillscommission.gov.au/our-work/australian-skills-classification#occupations~"
export class CardElement extends Component {

    renderIco() {
        const s = this.props.cardInfo.source.split(' ');
        if ((s.length > 0) && (s[0] === "Youtube:")) {
            return (
                <Typography color="textPrimary" variant="body2" component="p" style={{textAlign: "left", overflowY: "scroll", display: "flex", justifyContent: "left"}}>
                    <img src={youtube} style={{width: "24px", height: "24px"}} alt="logo"/>   {this.props.cardInfo.source.slice(9)}
                </Typography>
            )
        } else {
            // This is from personality type.
            return (
                <Typography color="textPrimary" variant="body2" component="p" style={{textAlign: "left", overflowY: "scroll", display: "flex", justifyContent: "left"}}>
                    <img src={personality} style={{width: "24px", height: "24px"}} alt="logo"/>   {this.props.cardInfo.source.slice(this.props.cardInfo.source.length - 4)}
                </Typography>
            )
        }
    }

    render() {
        return (
                <Card style={{ flex: 1, minWidth: '200px', position: 'relative', margin: '8px', zDepth: 1, background: "white"}}
                >
                    <CardContent>
                        <Typography color="textPrimary" gutterBottom>
                           {this.props.cardInfo.name}
                        </Typography>
                        <Typography color="textSecondary" variant="body2" component="p" style={{textAlign: "left", overflowY: "scroll"}}>
                            {this.props.cardInfo.desc}
                            <br/><br/>
                            Job vacancies in VIC: {this.props.cardInfo.vac}
                        </Typography>
                        <br/>
                        {this.renderIco()}

                    </CardContent>
                    <CardActions>
                        <a href={JEDI_URL + this.props.cardInfo.code} style={{textDecoration: "none"}}>
                            <Button size="small">Checkout profile</Button>
                        </a>
                    </CardActions>
                </Card>
        )
    }
}
