import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token"); 
     
      if (!token) {
        setError("User not logged in");
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/users/user", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`, 
          },
        });

        if (response.ok) {
          const data = await response.json();
          setEmail(data.email);
        } else {
          setError("Failed to fetch user details");
        }
      } catch (error) {
        setError("Error fetching user");
        console.error("Error:", error);
      }
    };

    fetchUser();
  }, []);

  return (
    <div className="p-6 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      {email ? (
        <p className="text-lg">Welcome, {email}!</p>
      ) : (
        <p className="text-red-500">{error}</p>
      )}
    </div>
  );
};

export default Dashboard;
