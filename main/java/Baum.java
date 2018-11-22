import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

/**
 * Eine Klasse, die die einzelnen Bäume aus dem "Baumkataster" widerspiegelt
 * 
 * @author Jo
 *
 */

public class Baum {
	public double x;
	public double y;
	/**
	 * default: false = UMT-Koordinaten , true = UMT-Koordinaten zu GPS-Koordinaten
	 * umgewandelt
	 */
	public boolean latlong = false;
	public String neighborhood = "No MATCH"; //Stadtbezirk
	public String sublocality = "NO MATCH"; //Stadt
	public String formatted_address = "NO MATCH";

	public Baum(double x, double y) {
		super();
		this.x = x;
		this.y = y;
	}

	public Baum(double x, double y, boolean latlong) {
		this.x = x;
		this.y = y;
		this.latlong = latlong;
	}

	public Baum(double x, double y, boolean latlong, String neighborhood, String sublocality,
			String formatted_address) {
		super();
		this.x = x;
		this.y = y;
		this.latlong = latlong;
		this.neighborhood = neighborhood;
		this.sublocality = sublocality;
		this.formatted_address = formatted_address;
	}

	/**
	 * Gets Values of keys "neighborhood", "sublocality" and "formatted_address"
	 * from JSON-Response from GoogleGeocodingAPI and writes them to attributes
	 * 
	 * @param jsonLine JSON-Response
	 * @author Jo
	 */

	public void extractAttributesFromReponseJson(String jsonLine) {
		JsonObject response = new JsonParser().parse(jsonLine).getAsJsonObject();
		JsonArray results = response.getAsJsonArray("results");
		JsonObject firstResult = results.get(0).getAsJsonObject();

		// get neighborhood and sublocality
		JsonArray address_components = firstResult.getAsJsonArray("address_components");
		JsonObject neighborhood = address_components.get(2).getAsJsonObject();
		JsonObject sublocality = address_components.get(3).getAsJsonObject();
		this.neighborhood = neighborhood.get("long_name").getAsString();
		this.sublocality = sublocality.get("long_name").getAsString();

		// get formatted_address
		this.formatted_address = firstResult.get("formatted_address").getAsString();
	}

	@Override
	public String toString() {
		if (latlong) {
			return "Baum [x=" + x + ", y=" + y + ", neighborhood=" + neighborhood + ", sublocality=" + sublocality
					+ ", formatted_address=" + formatted_address + "]";
		}
		return String.format("(%.0f, %.0f)", x, y);
	}

}
