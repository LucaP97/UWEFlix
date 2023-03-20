import React, {useState, useEffect} from 'react'
import "./styles/showings.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import { getAllShowings } from './services/ShowingService';
import { getAllFilms } from './services/FilmService';

//TODO

//Need a calendar / filter at the top per day, 
// showing for that day will be displayed with each time for that showing

//style showing times


function Showing(props) {
  return (
    <div className={"col-md-6"}>
        <div className={"card showing-card "}>
          <div className={"card-header showing-card-header"}>
            <h4>{props.title.charAt(0).toUpperCase() + props.title.slice(1)}</h4>
          </div>
          <div className={"card-body"}>
            <h5 className={"card-title"}>{props.showings.map(showing => (
              showing.showing_time.slice(-11).substring(0,5) + showing.showing_time.slice(-3)
            ))}</h5>
            <p className={"card-text"}>Duration: {props.duration}m</p>
            <img src={require("./imgs/" + props.image)} alt="Fight club poster" />
            <br/>
            <a href="#" className={"btn btn-primary"}>Buy Tickets</a>
          </div>
        </div>
      </div>
  )
}

function Showings() {
  const [films, setFilms] = useState([])
  const [showings, setShowings] = useState([])

  useEffect( () => {
    const fetchFilms = async () => {
      const data = await getAllFilms()
      setFilms(data);
    }
    const fetchShowings = async () => {
      const data = await getAllShowings()
      setShowings(data);
    }
    fetchShowings();
    fetchFilms();
  }, [])

  function getShowingsForFilm(film, showings) {
    return showings.filter((s) => s.film == film.id)
  }

  return (

    <div className="container" style={{marginTop: 20}}>
      {console.log(films)}
      <div className="row">
      {films.map(film => (
          <Showing title={film.title} age={film.age_rating} duration={film.duration} showings={getShowingsForFilm(film, showings)} image={film.image_uri}/>
        ))}  
    </div>
  </div>
  )
}

export default Showings