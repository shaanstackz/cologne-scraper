"use client";
import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchFragrance = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/search?q=${query}`);
      setResults(response.data.results);
    } catch (error) {
      console.error("Error fetching data", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-6">Cologne Price Finder</h1>
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Enter fragrance name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="p-2 rounded-md text-black"
        />
        <button
          onClick={searchFragrance}
          className="bg-blue-500 px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Search
        </button>
      </div>
      {loading && <p className="mt-4">Loading...</p>}
      <div className="mt-6 w-full max-w-lg">
        {results.length > 0 ? (
          results.map((item, index) => (
            <div key={index} className="bg-gray-800 p-4 rounded-md mb-2">
              <h2 className="text-lg font-semibold">{item.title}</h2>
              <p className="text-yellow-400 text-lg">{item.price}</p>
              <a
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:underline"
              >
                Buy Now
              </a>
            </div>
          ))
        ) : (
          <p className="text-gray-400">No results found.</p>
        )}
      </div>
    </div>
  );
}
