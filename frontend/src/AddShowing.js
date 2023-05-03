import React, { useState, useEffect } from 'react';
import { Form, Button } from "react-bootstrap";
import { getAllFilms } from "./services/FilmService";
import { event } from 'jquery';

// NEED TO INSTALL DATE PICKER: npm install react-datetime-picker
// NEED TO INSTALL TIME PICKER: npm install react-time-picker

import DatePicker from 'react-date-picker'
import 'react-date-picker/dist/DatePicker.css';
import 'react-calendar/dist/Calendar.css';

import TimePicker from 'react-time-picker'
import 'react-time-picker/dist/TimePicker.css';
import 'react-clock/dist/Clock.css';




// ONLY CINEMA MANAGER HAS AUTHORITY TO POST NEW SHOWINGS


function AddShowing(){
    const [screenList, setScreenList] = useState([]);
    const [screen, setScreen] = useState(null);

    const [filmsList, setFilmsList] = useState([]);
    const [film, setFilm] = useState(null);

    const [date, setDate] = useState(new Date());
    const [timeValue,setTimeValue] = useState(null);

    const [tickeksSold, setTickeksSold] = useState(0);

    const [priceList, setPriceList] = useState([]);
    const [price, setPrice] = useState(null);

    //ar DateTimeField = require('react-bootstrap-datetimepicker');

    useEffect(() => {
        const fetchScreens = async () => {
            const response = await fetch("http://127.0.0.1:8000/uweflix/screens/");
            const data = await response.json();
            //console.log(data);
            setScreenList(data);
		};
        const fetchFilms = async () => {
			const data = await getAllFilms();
			setFilmsList(data);
		};
        const fetchPrices = async () => {
            const response = await fetch("http://127.0.0.1:8000/uweflix/prices/");
            const data = await response.json();
            //console.log(data);
            setPriceList(data);
		};

        fetchScreens();
        fetchFilms();
        fetchPrices();
        
    }, []);

    //console.log(`T: ${JSON.stringify(screenList[0].screen_name)}`);

    const handleNumberOfSoldTickets = (event) => {
        const newValue = parseInt(event.target.value);
        setTickeksSold(isNaN(newValue) ? 0 : newValue);
    };

    const handleSubmit = (e) =>{
        e.preventDefault();

        const token = localStorage.getItem('access_token')
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${token}`
        }

        fetch("http://127.0.0.1:8000/uweflix/showings/", {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                screen: screen,
                film: film,
                showing_date: date,
                showing_time: timeValue,
                price: price
            })

        })
        .then(response => response.json())
        .then(data => {
            // console.log(`T: ${JSON.stringify(data)}`);
        })
        ;
    

    }

    return(
        <div className={"col-md-4"}>
            <h2 style={{ marginTop: 10 }}>Add a new Showing</h2>
            <Form onSubmit={handleSubmit}>
                {/* select screen */}
                <Form.Group controlId="screens" style={{ marginBottom: 10}}>
                    <Form.Label>Screen</Form.Label>
                    <Form.Select
                        value={screen?.id}
                        onChange={(event) => setScreen(event.target.value)}
                    >
                        <option value="">--Select a screen--</option>
                        {screenList.map(screen => (
                            <option key={screen.id} value={screen.id}>{screen.screen_name}</option>
                        ))}
					</Form.Select>
                </Form.Group>
                {/* select film */}
                <Form.Group controlId="films" style={{ marginBottom: 10}}>
                    <Form.Label>Film</Form.Label>
                    <Form.Select
                        value={film?.id}
                        onChange={(event) => setScreen(event.target.value)}
                    >
                        <option value="">--Select a film--</option>
                        {filmsList.map(film => (
                            <option key={film.id} value={film.id}>{film.title}</option>
                        ))}
					</Form.Select>
                </Form.Group>                
                {/* select date */}
                <Form.Group>
                    <Form.Label>Date</Form.Label>
                    <div>
                        <DatePicker onChange={setDate} value={date} />
                    </div>
                </Form.Group>
                {/* select time */}
                <Form.Group>
                    <Form.Label>Time</Form.Label>
                    <div>
                        <TimePicker onChange={setTimeValue} value={timeValue} />
                    </div>
                </Form.Group>
                {/* set ticket sold */}
                <Form.Group>
                    <Form.Label>Tickets Sold</Form.Label>
                    <Form.Control 
                        type="number"
                        value={tickeksSold} 
                        onChange={handleNumberOfSoldTickets} />
                </Form.Group>
                {/* set price */}
                <Form.Group>
                    <Form.Label>Price Selection</Form.Label>
                    <Form.Select
                        value={price?.id}
                        onChange={(event) => setPrice(event.target.value)}
                    >
                        <option value="">--Select price config--</option>
                        {priceList.map(price => (
                            <option value={price.id}>{price.id}</option>
                        ))}
					</Form.Select>
                </Form.Group>

                <Button variant="primary" type="submit" style={{ marginTop: 20 }}>
					Add Showing
				</Button>
            </Form>
        </div>
    )
}
export default AddShowing;