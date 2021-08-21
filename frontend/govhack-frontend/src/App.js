import logo from './logo.svg';
import './App.css';
import {GoogleLogin} from 'react-google-login';
import React, {Component} from 'react';
import {AppBar} from './components/appbar';
import {SideBar} from './components/sidebar'
import {Content} from './components/content';
import axios from 'axios';

class App extends Component {
    youtubeInterestSelectStatus = {}

    constructor(props) {
        super(props);
        this.state = {
            hasLoggedIn: false,
            allYoutubeInterests: [],
            cardData: [],
        }
        this.getYoutubeInterests();
        this.onYoutubeCheckboxClick = this.onYoutubeCheckboxClick.bind(this);

    }

    getYoutubeInterests() {
        axios.get('http://localhost:5000/get_youtube_interests?with_all_jobs=true').then(response => {
            console.log(response.data);
            const justInterests = [];

            for (const interestJobMapping of response.data["youtube_interests_with_jobs"]) {
                if (interestJobMapping["similar_jobs"].length === 0) {
                    continue
                }

                const ensure_relevant_j = []
                for (const j of interestJobMapping["similar_jobs"]) {
                    if (j["source"] === "Youtube: " + interestJobMapping["interest"]) {
                        ensure_relevant_j.push(j)
                    }
                }
                if (ensure_relevant_j.length === 0) {
                    continue
                }

                justInterests.push(interestJobMapping["interest"])

                this.youtubeInterestSelectStatus[interestJobMapping["interest"]] = {
                    "selected": false,
                    "cards": ensure_relevant_j
                };
            }
            this.setState({allYoutubeInterests: justInterests})

            console.log(this.youtubeInterestSelectStatus);
        });

    }

    handleLogIn() {
        console.log('handle log in')
        this.setState({hasLoggedIn: true})
    }

    onYoutubeCheckboxClick(interestToggled) {
        // console.log(interestToggled);
        // Do the toggle.
        this.youtubeInterestSelectStatus[interestToggled]["selected"] = !this.youtubeInterestSelectStatus[interestToggled]["selected"];
        if (this.youtubeInterestSelectStatus[interestToggled]["selected"]) {
            this.setState({cardData: [...this.state.cardData, ...this.youtubeInterestSelectStatus[interestToggled]["cards"]]})
        } else {
            const remainingData = this.state.cardData;
            const result = remainingData.filter((d) => {
                // Remove this.
                return d["source"] != "Youtube: " + interestToggled;
            })
            console.log(result);

            this.setState(
                {cardData: result}
            )
        }
    }

    onSubmitPersonalityType(ptype) {
        console.log('on submit ptype: ' + ptype);
        if (ptype === '') { // Risky should guard against bad input but im too tired.
            return;
        }
        // Remove personality types form the screen.
        const cards = this.state.cardData;
        const result = cards.filter(
            (c) => c.source.slice(0, 6) !== "Person"
        )
        this.setState({cardData: result});

        axios.get('  http://localhost:5000/personality_mappings?ptype=' + ptype).then(response => {
            console.log(response.data);
            const pJobs = []
            for (const entry of response.data["personality_mappings"]) {
                // console.log(entry["career"]);
                if (entry["similar_jobs"][0]) {
                    pJobs.push(entry["similar_jobs"][0]);
                }

            }
            console.log(pJobs);
            this.setState({cardData: [...this.state.cardData, ...pJobs]});
        });
    }

    render() {
        console.log('state has logged in? ' + this.state.hasLoggedIn)
        // const displayHome = this.state.hasLoggedIn ? "none": "block"
        // const displayHomeInverted = this.state.hasLoggedIn ? "block": "none"

        const displayHome = "none"
        const displayHomeInverted = "block"

        return (
            <div>
                <div className="App" style={{display: displayHome}}>
                    <header className="App-header">
                        <img src={logo} className="App-logo" alt="logo"/>
                        <p>
                            Log in with your Google account and <b>Uncover</b> possibilities.
                        </p>
                        <GoogleLogin
                            clientId="542193569156-48pri3fbbj966c1tg6sa1u814u542lpv.apps.googleusercontent.com"
                            buttonText="Login"
                            onSuccess={() => this.handleLogIn()}
                            onFailure={() => this.handleLogIn()}
                            cookiePolicy={'single_host_origin'}
                        />
                    </header>
                </div>
                <div className="App" style={{display: displayHomeInverted}}>
                    <AppBar></AppBar>
                    <div style={{display: 'flex', height: '90vh', margin: 'auto', zIndex: -5}}>

                        <Content clientData={this.state.cardData}></Content>
                        <SideBar
                            youtubeInterests={this.state.allYoutubeInterests}
                            checkboxClicked={(v) => this.onYoutubeCheckboxClick(v)}
                            onSubmitPersonalityType={(p) => this.onSubmitPersonalityType(p)}
                        >
                        </SideBar>
                    </div>

                </div>
            </div>
        );
    }
}

export default App;
