import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function StacksPage() {
  const [stacks, setStacks] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/stacks")  // Call FastAPI
      .then((response) => response.json())
      .then((data) => setStacks(data))
      .catch((error) => console.error("Error fetching stacks:", error));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Stacks</h1>
      <div className="grid grid-cols-3 gap-4">
        {stacks.map((stack) => (
          <Link key={stack.id} to={`/stack/${stack.id}`} className="block border p-2 rounded shadow hover:shadow-lg">
            {stack.first_image ? (
              <img src={`${stack.first_image}`} alt="Stack" className="w-full h-32 object-cover rounded" />
            ) : (
              <div className="w-full h-32 flex items-center justify-center bg-gray-200 rounded">No Image</div>
            )}
            <p className="text-center mt-2">Stack #{stack.id}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default StacksPage;
