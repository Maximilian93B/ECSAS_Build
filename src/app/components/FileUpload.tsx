"use client";
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone'

// create a function that accepts a file
// need to use OnDrop (built into React)
// We need a DropZone to accept props
// Then return it in a div and call it in our parent

const FileUpload = () => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
    //This will be a logic for our file upload
    console.log(acceptedFiles)
    }, []);

    const{ getRootProps, getInputProps } = useDropzone({onDrop})

    return (
        <div {...getRootProps()} className="border-2 border-dashed border-gray-500 p-5 text-center mt-8">
          <input {...getInputProps()} />
          <p>Drag & drop some files here, or click the button below to browse through your file explorer</p>
        </div>
      );
    };

export default FileUpload;



   