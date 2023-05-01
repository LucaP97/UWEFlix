import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function NavBar() {
  const [showNav, setShowNav] = useState(false);

  function handleNavToggle() {
    setShowNav(!showNav);
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <button
          className="navbar-toggler"
          type="button"
          onClick={handleNavToggle}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <ul className={`navbar-nav ${showNav ? 'show' : ''}`}>
          <li className="nav-item">
            <a className="nav-link active" aria-current="page" href="/showings">
              Showings
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="/film_editing">
              Edit Films
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              Contact
            </a>
          </li>
          
        </ul>
        {/* Change login to logout if user is logged in */}
        <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link" href="/login" style={{fontWeight: 'bold'}}>Login</a>
            </li>
            <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link" href="/register" style={{fontWeight: 'bold'}}>Register</a>
            </li>
          </ul>
          </ul>
      </div>
    </nav>
  );
}

export default NavBar;
