import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function StackPage() {
  const { id } = useParams();  // Get the stack ID from the URL
  const [stack, setStack] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/stack/${id}`)
      .then((res) => res.json())
      .then((data) => setStack(data));
  }, [id]);

  if (!stack) return <p>Loading...</p>;

  return (
    <div>
      <h1>Stack {stack.id}</h1>
      <ul>
        {stack.imagefiles.map((img) => (
          <li key={img.id}>{img.id} {img.path_str}</li>
        ))}
      </ul>
    </div>
  );
}

export default StackPage;
