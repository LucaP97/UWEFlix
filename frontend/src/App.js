import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Showings from './Showings'
import Booking from './Booking'
import RegisterUser from './RegisterUser';
import LoginUser from './LoginUser';
import NavBar from './Components/NavBar';

function App() {
  return (
    <Router>
      <html>
      <head>
        <meta charSet="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <meta httpEquiv="X-UA-Compatible" content="ie=edge"/>
        <title>Cinema Showings</title>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
          integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
          crossOrigin="anonymous"
        />
    </head>

      <body>
        <NavBar />
        
          <Routes>
          <Route path="/"/>
            <Route path="/register" element={<RegisterUser />}/>
            <Route path="/login" element={<LoginUser />}/>
            <Route path="/showings" element={<Showings />}/>
            <Route path="/showings/booking" element={<Booking />}/>
          </Routes>
          
        
        
      </body>
      </html>
    </Router>
  );
}

export default App;
