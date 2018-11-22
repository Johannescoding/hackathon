import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

/**
 * A class to make a Reverse-Geocoding-GET-request to the GoogleGeocodeAPI
 * 
 * @author Jo
 *
 */

public class GoogleApi {

	private static final String API_CODE = "";
	private static final String URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng=";

	public String getJSONByGoogle(double lat, double len) throws Exception {

		URL url = new URL(URL + lat + "," + len + "&key=" + API_CODE);

		// Open the Connection
		HttpURLConnection con = (HttpURLConnection) url.openConnection();

		int responseCode = con.getResponseCode();
		if (responseCode == 200) {
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer response = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}
			in.close();

			return response.toString();
		}
		return null;
	}

}
