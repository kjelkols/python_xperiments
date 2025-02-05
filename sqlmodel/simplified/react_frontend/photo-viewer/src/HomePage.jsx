import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function HomePage() {
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
            <Link to={`/stack/${stack.id}`}>Stack {stack.id}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HomePage;
