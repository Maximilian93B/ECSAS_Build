import Link from 'next/link';
import FileUpload from './components/FileUpload';


// Make a component and name it Home 
// This will be our main component
const Home = () => {
  // Every React component needs a return function 
  return (
    <div className="min-h-screen bg-white-100 flex flex-col items-center justify-center">
      {/*The Head is used for SEO*/}
      <main className='text-center'>
        <h1 className='text-4xl font-bold text-gray-900 mb-4'>
          Welcome to the Seabird Survery App
        </h1>
        <p className='text-lg text-gray-900 mb-6'> 
        Upload your survey data to visualize seabird sightings on a map.
        </p>    
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Upload Data
          </button>
         <FileUpload/>
         <div className="mt-10">
          <Link href="/AnalyticsPage" className="text-blue-500 hover:underline">
            View Seabird Data Here 
          </Link>
          </div>
      </main>
      </div>
  );
};

export default Home;

























