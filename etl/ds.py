from .logs import die, info
import requests
import json as js
import osm2geojson as o2g
import geojson as geojs


def get_data(overpass_url: str, query: str, obj_name: str, country: str):
    """
    This function sends the query for the OSM Overpass API in string format and gives back a JSON response object
    Args:
        query(str): Query in string format of Overpass query language
        url(str): Url in string format from config file
        obj_name(str): Takes the name of the object for error message
        country (str): Takes the name of the country for error message
    Returns: 
        A response data object in json format containing OSM data
    """
    # Perform a maximum of ten trials to download the data
    download_attempt = 1

    while download_attempt <= 10:
        try: 
            response = requests.get(overpass_url, params={'data': query})
            data = response.json()
        except:
            info(f"EXTRACTION: FAILED DOWNLOAD IN ATTEMPT {download_attempt} FOR {obj_name} IN {country} ")
            download_attempt += 1
        else:
            if data["elements"] == []:
                info(f"EXTRACTION: DOWNLOADED DATA FOR {obj_name} IN {country} WAS EMPTY IN DOWNLOAD ATTEMPT {download_attempt}")
                download_attempt += 1
            else: break
    else: 
        die(f"STOPPED DOWNLOAD AFTER ATTEMPT: {download_attempt-1}")

    return data


def create_fname(fname: str, directory: str):
    """
    This function creates filenames

    Args:
        fname (str): name of file
        directory (str): The directory which will be set before the filename
    
    Return:
        str: Complete filename with directory path
    """
    fname = f"{directory}/{fname}" #'data/original/rail'
    return fname


def save_as_json_geojson(overpass_json, filename: str):
    """This function saves the overpass query results in folder original in json format in a json file and geojson file
    Arg:
        overpass_json = Json format of the Overpass result
        filename: str = Filename for the saving the files
    Return:
        data\original\filename.json
        data\original\filename.geojson
    """
    # Save as normal json file
    with open(f"{filename}.json", mode="w") as file1:
        geojs.dump(overpass_json, file1)
    # Save as geojson file
    overpass_geojson = o2g.json2geojson(overpass_json) ## convert to a geojson
    with open(f"{filename}.geojson",mode="w") as file2:
        geojs.dump(overpass_geojson,file2)