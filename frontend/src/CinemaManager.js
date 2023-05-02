import Button from 'react-bootstrap/Button';

function CinemaManager(){
    return(
        <div className={"col-md-4"}>
                <>
                    <div>
                        Hello 
                    </div>
                </>
                <ul>
                    <Button variant="outline-primary" href="/film_editing">Add/Delete Films</Button>
                    <Button variant="outline-primary" href="/add_showing">Create Showing</Button>
                </ul>


        </div>

        

    )
}
export default CinemaManager;
