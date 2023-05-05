import React, { useState, useEffect } from "react";
import "./styles/screens.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { getAllScreens, addScreen } from "./services/ScreenService";
import { Form, Button } from "react-bootstrap";

import jwtDecode from 'jwt-decode'

//icons
import { IonIcon } from "@ionic/react";
import {} from "ionicons/icons";

function ScreenListScreen() {
	const [screens, setScreens] = useState([]);
	const [newScreen, setNewScreen] = useState();
	const [newCapcity, setNewCapacity] = useState();

	useEffect(() => {
		const fetchScreens = async () => {
			const data = await getAllScreens();
			setScreens(data);
		};

		fetchScreens();
	}, []);

	const handleSubmit = async (event) => {
        event.preventDefault();

        const data = await addScreen({
            screen_name: newScreen,
            capacity: newCapcity
        })

        //update screen list
        setScreens(prev => [...prev, data])

    };

    // const access_token = localStorage.getItem('access_token')
    // const decodedToken = jwtDecode(access_token)
    // console.log(decodedToken)
    

	return (
		<div className={"list"} style={{ justifyContent: "flex-start" }}>
            <div>
				<Form onSubmit={handleSubmit} className="form">
					<div className="top-row">
						<Form.Group controlId="formName" >
							<Form.Control
								type="number"
								placeholder="Enter screen name"
								value={newScreen}
								onChange={(event) => setNewScreen(event.target.value)}
							/>
						</Form.Group>
                        <img
							className="image-seat"
                            style={{ marginRight: 30, paddingTop: 8, marginLeft:8}}
							src={require("./imgs/cinema.png")}
							alt="Fight club poster"
						/>
                        
						<Form.Group controlId="formPassword" style={{  }}>
							<Form.Control
								type="number"
								placeholder="Enter capcity"
								value={newCapcity}
								onChange={(event) => setNewCapacity(event.target.value)}
							/>
                            
						</Form.Group>
                        <img
							className="image-seat"
                            style={{paddingTop: 8}}
							src={require("./imgs/seat.png")}
							alt="Fight club poster"
						/>
					</div>
					<Button variant="primary" type="submit" style={{ height: '5vh' }}>
						Add Screen
					</Button>
				</Form>
			</div>
            <hr/>
			<div className="list">
				{screens.map((screen) => (
					<div className="row-container">
						<h3 className="film-title">Screen {screen.screen_name}</h3>
						<div style={{ marginLeft: "auto" }}>
							<h4>{screen.capacity}</h4>
						</div>
						<img
							className="image-seat"
							src={require("./imgs/seat.png")}
							alt="Fight club poster"
						/>
					</div>
				))}
			</div>
		</div>
	);
}

export default ScreenListScreen;
