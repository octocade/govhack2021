import React, { Component } from 'react';

export class AppBar extends Component {

    render() {
        return (
            <div style={{ zIndex: 10000, width: "100vw", backgroundColor: "#fff", height: "10vh", display: "flex", boxShadow: '0 3px 6px rgba(0,0,0,0.16)' }}>
                <div style={{ fontFamily: "'Noto Sans JP'", alignText: 'center', flex: 5, margin: 'auto', fontSize: '38px', color: '#555'}}>
                    D I S C O V E R I E
                </div>
            </div>
        )
    }
}