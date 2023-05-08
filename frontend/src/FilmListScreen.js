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
	editFilm,
	deleteFilmShowings,
} from "./services/FilmService";

//icons
import { IonIcon } from "@ionic/react";
import {
	trashOutline,
	filmOutline,
	addOutline,
	pencilOutline,
} from "ionicons/icons";

function FilmRow(props) {
	const navigateEdit = useNavigate()
	return (
		<div className="row-container">
			<div class="image-container">
				<img className="image-film" src={props.image} alt="Fight club poster" />
			</div>
			<h3 className="film-title">
				{props.title.charAt(0).toUpperCase() + props.title.slice(1)}
			</h3>
			<div style={{ marginLeft: "auto" }}>
				<button
					onClick={() => {
						navigateEdit("/film_editing/edit_film", {
							state: props.film,
						})
					}}
					style={{marginRight: 10}}
				>
					<IonIcon icon={pencilOutline} size="large" color="black" />
				</button>
				<button
					onClick={() => {
						props.handler(props.film, props.id);
						const updatedFilms = props.prevfilms.filter(
							(film) => props.id !== film.id
						);
						props.updateFilms(updatedFilms);
					}}
				>
					<IonIcon icon={trashOutline} size="large" color="black" />
				</button>
			</div>
		</div>
	);
}

function FilmListScreen() {
	const [films, setFilms] = useState([]);
	const navigate = useNavigate();

	useEffect(() => {
		const fetchFilms = async () => {
			const data = await getAllFilms();
			setFilms(data);
		};

		fetchFilms();
	}, []);

	function getShowingsForFilm(film, showings) {
		return showings.filter((s) => s.film == film.id);
	}

	const handleDelete = async (film, film_id) => {
		//delete all associated showings first
		const showings = await getAllShowings();
		const filmShowings = getShowingsForFilm(film, showings);

		filmShowings.forEach((showing) => {
			deleteFilmShowings(showing.id);
		});
		//delete film

		const data = {
			title: film.title,
			age_rating: film.age_rating,
			duration: film.duration,
			short_trailer_description: film.short_trailer_description,
			is_active: false,
		};
		console.log(data);
		const response = await editFilm(data, film_id);
		console.log(response);
	};

	const updateFilms = (fs) => {
		setFilms(fs);
	};

	return (
		<div className={"list"} style={{ justifyContent: "flex-start" }}>
			<div className="top-row">
				<button
					href=""
					className={"btn btn-primary"}
					onClick={() => {
						navigate("/add_film");
					}}
				>
					Add New Film <IonIcon icon={addOutline} size="small" color="white" />
					<IonIcon icon={filmOutline} size="small" color="white" />
				</button>
			</div>
			<div className="list">
				{films.map((film) => (
					<FilmRow
						key={film.id}
						id={film.id}
						film={film}
						title={film.title}
						age={film.age_rating}
						duration={film.duration}
						image={film.images[0].image}
						description={film.short_trailer_description}
						handler={handleDelete}
						updateFilms={updateFilms}
						prevfilms={films}
					/>
				))}
			</div>
		</div>
	);
}

export default FilmListScreen;
