"use client";
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

// Define the types for the props
interface FileUploadProps {
  setLocations: (locations: any[]) => void;
  onUploadSuccess: () => void;
}

// Define the types for the response data
interface GeoJSONFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: number[];
  };
  properties: {
    [key: string]: any;
  };
}

interface UploadResponse {
  message: string;
  geojson: {
    type: string;
    features: GeoJSONFeature[];
  };
}

// FileUpload component
const FileUpload: React.FC<FileUploadProps> = ({ setLocations, onUploadSuccess }) => {
  // Set the state to handle messages and errors
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');

    // Callback function to handle the file being dropped
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const formData = new FormData();
    acceptedFiles.forEach((file) => {
      formData.append('file', file);
    });
  
      try {
        // Make a POST request to our Python backend using AXIOS
        const response = await axios.post<UploadResponse>('http://127.0.0.1:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
  
      setMessage(response.data.message);
      setError('');
      setLocations(response.data.geojson.features); // Extract locations from the GeoJSON data
      onUploadSuccess(); // Call the callback function after successful upload
      } catch (err) {
        console.error('There was an error uploading the file!', err);
        if (axios.isAxiosError(err)) {
          if (err.response && err.response.data && err.response.data.error) {
            setError(`Error: ${err.response.data.error}`);
          } else {
            setError('There was an error uploading the file.');
          }
        } else {
          setError('An unknown error occurred.');
        }
        setMessage('');
      }
  }, [setLocations, onUploadSuccess]);
  
    const { getRootProps, getInputProps } = useDropzone({ onDrop });

    return (
      <div className="container mx-auto p-4">
        <div {...getRootProps()} className="border-2 border-dashed border-gray-500 p-5 text-center mt-8">
          <input {...getInputProps()} />
          <p>Drag & drop some files here, or click to select files</p>
        </div>
        {error && <p className="text-red-500">{error}</p>}
        {message && <p className="text-green-500">{message}</p>}
      </div>
    );
  };

export default FileUpload;
