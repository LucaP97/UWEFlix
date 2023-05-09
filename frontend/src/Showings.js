import React, { useState, useEffect } from "react";
import { json, useNavigate } from "react-router-dom";
import "./styles/showings.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { getAllShowings } from "./services/ShowingService";
import { getAllFilms } from "./services/FilmService";

import { useLocation } from "react-router-dom";

import { useSelector } from "react-redux";
import { data } from "jquery";

//TODO

//Need a calendar / filter at the top per day,
// showing for that day will be displayed with each time for that showing

//style showing times

function Showing(props) {


	const navigate = useNavigate();
	return (
		<div className={"col-md-4"}>
			<div className={"card showing-card "}>
				<div className={"card-header showing-card-header"}>
					<h4>{props.title.charAt(0).toUpperCase() + props.title.slice(1)}</h4>
				</div>
				<div className={"card-body"}>
					<h5 className={"card-title"}>
						{props.showings.map((showing) => (
							<span key={showing.showing_time} className="showing-time">
								{showing.showing_time.substring(0, 5)}
							</span>
						))}
					</h5>
					<p className={"card-text"}>Duration: {props.duration}m</p>
					<img
						className="image-showings"
						//src={require("./imgs/" + props.image)}
						src={props.image}
						alt="Fight club poster"
					/>
					<br />
					<button
						href=""
						className={"btn btn-primary"}
						onClick={() => {
							navigate("/showings/booking", {
								state: {
									showings: props.showings,
									image: props.image,
									title: props.title,
									duration: props.duration,
									age: props.age,
									description: props.description,
								},
							});
						}}
					>
						Buy Tickets
					</button>
				</div>
			</div>
		</div>
	);
}

function Showings() {
	const [films, setFilms] = useState([]);
	const [showings, setShowings] = useState([]);

	
	const location = useLocation();

	const userType = useSelector((state) => state.userType);
	useEffect(() => {

		const booking_id = new URLSearchParams(location.search).get('id');
		const showingID = new URLSearchParams(location.search).get('showing_id');
		const adultTickets = new URLSearchParams(location.search).get('adult_ticket');
		console.log(` 		TA:${adultTickets}`)
		const studentTickets = new URLSearchParams(location.search).get('student_ticket');
		console.log(` 		TA:${studentTickets}`)
		const childTickets = new URLSearchParams(location.search).get('child_ticket');
		console.log(` 		TA:${childTickets}`)

		const fetchFilms = async () => {
			const data = await getAllFilms();
			setFilms(data);
		};
		const fetchShowings = async () => {
			const data = await getAllShowings();
			setShowings(data);
		};
		fetchShowings();
		fetchFilms();


		if(booking_id !== null){
			let token;
			let headers;

			if(userType === "GUEST"){
				headers = {"Content-Type": "application/json"}
			}
			else{
				token = localStorage.getItem('access_token')
				headers = {
					'Content-Type': 'application/json',
					'Authorization': `JWT ${token}`
				}
			}

			
			if(parseInt(adultTickets) > 0){
				fetch(`http://127.0.0.1:8000/uweflix/booking/${booking_id}/items/`,{
					method: "POST",
					headers: headers,
					body: JSON.stringify(
						{
							"showing_id": showingID,
							"ticket_type": "A",
							"quantity": adultTickets
						}
					)
				})
				.then(response => response.json())
				.then(data => console.log(`		TA:${JSON.stringify(data)}`))
				.catch(error => console.error(error))
			}
			if(parseInt(studentTickets) > 0){
				fetch(`http://127.0.0.1:8000/uweflix/booking/${booking_id}/items/`,{
					method: "POST",
					headers: headers,
					body: JSON.stringify(
						{
							"showing_id": showingID,
							"ticket_type": "S",
							"quantity": studentTickets
						}
					)
				})
				.then(response => response.json())
				.then(data => console.log(`		TS:${JSON.stringify(data)}`))
				.catch(error => console.error(error))
			}
			if(parseInt(childTickets) > 0){
				fetch(`http://127.0.0.1:8000/uweflix/booking/${booking_id}/items/`,{
					method: "POST",
					headers: headers,
					body: JSON.stringify(
						{
							"showing_id": showingID,
							"ticket_type": "C",
							"quantity": childTickets
						}
					)
				})
				.then(response => response.json())
				.then(data => console.log(`		TC:${JSON.stringify(data)}`))
				.catch(error => console.error(error))
			}

			// fetch(`http://127.0.0.1:8000/uweflix/booking/${booking_id}/items/`,{
			// 		method: "POST",
			// 		headers: headers,
			// 		body: JSON.stringify(
			// 			{
			// 				"booking_id" : booking_id							
			// 			}
			// 		)
			// 	})

		}

	}, []);

	function getShowingsForFilm(film, showings) {
		return showings.filter((s) => s.film == film.id);
	}

	return (
		<div className="container" style={{ marginTop: 20 }}>
			<div className="row ">
				{films.map((film) => (
					<Showing
						key={film.title}
						title={film.title}
						age={film.age_rating}
						duration={film.duration}
						showings={getShowingsForFilm(film, showings)}
						image={film.images[0].image}
						description={film.short_trailer_description}
					/>
				))}
			</div>
		</div>
	);
}

export default Showings;
