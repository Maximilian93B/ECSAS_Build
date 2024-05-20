'use client';

import React, { useEffect  } from "react";
import '@arcgis/core/assets/esri/themes/light/main.css';
import MapView from '@arcgis/core/views/MapView';
import Map from '@arcgis/core/Map';
import Basemap from '@arcgis/core/Basemap';
import WebTileLayer from '@arcgis/core/layers/WebTileLayer';


const AnalyticsPage = () => {
    useEffect(() => {
        const initializeMap = async () => {
            // Create a new WebTileLayer for the ocean basemap
            const oceanBaseLayer = new WebTileLayer ({
                urlTemplate: "https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{level}/{row}/{col}"
            });

            // Create a new basemap using WebTileLauer
            const oceanBasemap = new Basemap({
                baseLayers: [oceanBaseLayer]
            });

            const map = new Map({
                basemap: oceanBasemap
            }); 

            // Create a new MapView and set its container, map , and other properties
            const view = new MapView({
                container: "viewDiv",
                map: map, 
                center: [-100.33, 25.69], // Long , lat 
                zoom: 3 
            });
        };

        initializeMap();
    }, []);

    return (    
        <div>
            <main className="min-h-screen flex flex-col items-center justify-center">
                <h1 className="text-4xl font-bold mb-4">Seabird Analytics Survey Map</h1>
                <div id="viewDiv" className="w-full h-full" style={{ height: '80vh', width: '80vw' }}></div>
            </main>
        </div>
    );

};

export default AnalyticsPage; 