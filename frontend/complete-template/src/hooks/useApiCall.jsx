import { useEffect, useState } from "react";

function useApiCall(apiUrl) {
    const [data, setData] = useState(null);
    const [loadingData, setLoading] = useState(true);
  
    useEffect(() => {
      async function fetchData() {
        try {
          const response = await fetch(apiUrl);
          const jsonData = await response.json();
          setData(jsonData);
          setLoading(false);
        } catch (error) {
          console.error('Error fetching data:', error);
          setLoading(false);
        }
      }
  
      fetchData();
    }, [apiUrl]);
  
    return { data, loadingData };
  }
  
  export default useApiCall;