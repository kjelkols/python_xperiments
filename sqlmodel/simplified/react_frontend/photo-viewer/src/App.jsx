/*
import { useEffect, useState } from "react";

function App() {
  const [stacks, setStacks] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/stacks")
      .then((res) => res.json())
      .then((data) => setStacks(data));
  }, []);

  return (
    <div>
      <h1>Stacks</h1>
      <ul>
        {stacks.map((stack) => (
          <li key={stack.id}>
            Stack {stack.id} - {stack.imagefiles.length} images
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
*/

/*
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import HomePage from "./HomePage";
import StackPage from "./StackPage";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Home</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/stack/:id" element={<StackPage />} />
      </Routes>
    </Router>
  );
}

export default App;

*/

import { Routes, Route, Link } from "react-router-dom";
import HomePage from "./HomePage";
import StackPage from "./StackPage";
import StacksPage from "./StacksPage";

function App() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link><br />
        <Link to="/stacks">Stacks</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/stack/:id" element={<StackPage />} />
        <Route path="/stacks" element={<StacksPage />} />
      </Routes>
    </div>
  );
}

export default App;
