"use client";
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone'


// Feed props to FileUpload that allow us to pass loacations and success messages to our function
// This will allow the function to accept the Lat + Long from our Data file 
// We will set a onSuccess message when the function executes with no errors 


const FileUpload = () => {
  // Set the state to handle messages and erorrs   
  
  
  
  
  
// Callback function to handle the file being dropped 
// Create a new formData() --> Object to hold our file data 
// APPEND !!! each file to the FormData 
  const onDrop = useCallback((acceptedFiles: File[]) => {
    //This will be a logic for our file upload
    console.log(acceptedFiles)
    }, []);

    
    /**
     * Make a POST request to our python backend using AXIOS 
     * Following the route/then.response/catch format 
     */





    const{ getRootProps, getInputProps } = useDropzone({onDrop})

    return (
        <div {...getRootProps()} className="border-2 border-dashed border-gray-500 p-5 text-center mt-8">
          <input {...getInputProps()} />
          <p>Drag & drop some files here, or click the button below to browse through your file explorer</p>
        </div>
      );
    };

export default FileUpload;



   