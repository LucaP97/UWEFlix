//List all films
//add expansion dropdown for more details
//add Add film button at the top of the page
//add Bin button on each film row entry to delete

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/filmslist.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { getAllShowings } from "./services/ShowingService";
import {
	getAllFilms,
	deleteFilm,
	deleteFilmShowings,
} from "./services/FilmService";

//icons
import { IonIcon } from "@ionic/react";
import { trashOutline } from "ionicons/icons";

function FilmRow(props) {
	function getShowingsForFilm(film, showings) {
		return showings.filter((s) => s.film == film.id);
	}

	const handleDelete = async () => {
		//delete all associated showings first
		const showings = await getAllShowings();
		const filmShowings = getShowingsForFilm(props.film, showings);

		filmShowings.forEach((showing) => {
			deleteFilmShowings(showing.id);
		});
		//delete film
		deleteFilm(props.id);
	};

	return (
		<div className="row-container">
			<div class="image-container">
				<img
					className="image-film"
					src={require("./imgs/" + props.image)}
					alt="Fight club poster"
				/>
			</div>
			<h3 className="film-title">
				{props.title.charAt(0).toUpperCase() + props.title.slice(1)}
			</h3>
			<div style={{ marginLeft: "auto" }}>
				<button onClick={handleDelete}>
					<IonIcon icon={trashOutline} size="large" color="black" />
				</button>
			</div>
		</div>
	);
}

function FilmListScreen() {
	const [films, setFilms] = useState([]);

	useEffect(() => {
		const fetchFilms = async () => {
			const data = await getAllFilms();
			setFilms(data);
		};

		fetchFilms();
	}, []);

	return (
		<div style={{ height: "100vh" }}>
			<div>{/* add button link to add new film */}</div>
			<div className="list">
				{films.map((film) => (
					<FilmRow
						key={film.id}
						id={film.id}
						film={film}
						title={film.title}
						age={film.age_rating}
						duration={film.duration}
						image={film.image_uri}
						description={film.short_trailer_description}
					/>
				))}
			</div>
		</div>
	);
}

export default FilmListScreen;
