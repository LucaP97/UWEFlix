import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/showings.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { getAllShowings } from "./services/ShowingService";
import { getAllFilms } from "./services/FilmService";

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
						src={require("./imgs/" + props.image)}
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

	useEffect(() => {
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
	}, []);

	function getShowingsForFilm(film, showings) {
		return showings.filter((s) => s.film == film.id);
	}

	return (
		<div className="container" style={{ marginTop: 20 }}>
			{console.log(showings)}
			<div className="row ">
				{films.map((film) => (
					<Showing
						key={film.title}
						title={film.title}
						age={film.age_rating}
						duration={film.duration}
						showings={getShowingsForFilm(film, showings)}
						image={film.image_uri}
						description={film.short_trailer_description}
					/>
				))}
			</div>
		</div>
	);
}

export default Showings;
