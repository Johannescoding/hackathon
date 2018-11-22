import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import gov.nasa.worldwind.avlist.AVKey;
import gov.nasa.worldwind.geom.LatLon;
import gov.nasa.worldwind.geom.coords.UTMCoord;

public class main {

	public static String csvFile = "C:\\Users\\Jo\\Documents\\baum.csv";

	public static void main(String[] args) {

//		JsonReader jsonreader;
//		try {
//			jsonreader = new JsonReader(new FileReader("C:\\Users\\Jo\\Documents\\Dokumente\\beispiel.json"));
//			JsonElement file1 = new JsonParser().parse(jsonreader);
//			String file = file1.toString();
//			Baum baum = new Baum(10,10, true);
//			baum.extractAttributesFromReponseJson(file);
//			System.out.println(baum.toString());
//		} catch (FileNotFoundException e) {
//			e.printStackTrace();
//		}

		CSV_Reader csvReader = new CSV_Reader();
		List<Baum> baeume = csvReader.readCSVtoList(csvFile);
		System.out.println(
				"Gelesen:" + csvReader.getAnzahlGelesene() + ", Geschrieben: " + csvReader.getAnzahlGeschriebene());
		System.out.println("Kaputte:" + csvReader.getAnzahlKaputte());
		System.out.println(baeume);

		List<Baum> baeumeLatLong = createLatLongList(baeume);
		System.out.println(baeumeLatLong);

		List<Baum> fertigeBaumListe = anfrageUeberListe(baeumeLatLong);
		System.out.println(fertigeBaumListe);
	}

	/**
	 * @deprecated first trial to parse GoogleGeocodeAPI response
	 */

	private static String getFieldValue(String response, String field) {
		if (response == null || field == null) {
			return null;
		}
		if (field != "formatted_address") {
			System.out.println(field);
			int hinten = response.indexOf(field);
			String first = response.substring(0, hinten);
			System.out.println(first);
			String parameter = "long_name";
			int vorne = first.lastIndexOf(parameter) + parameter.length() + 5;
			String second = first.substring(vorne, hinten);
			System.out.println(second);
			String third = second.substring(0, second.indexOf('\"'));
			return field + ":" + third;
		} else {
			int vorne = response.indexOf(field);
			String first = response.substring(vorne);
			System.out.println(first);
			String second = first.substring(0, first.indexOf(','));
			System.out.println(second);
			String third = second.replaceFirst("\\s", "");
			third = third.replaceFirst("\\s", "");
			System.out.println(third);
			String fourth = third.replaceAll("\"", "");
			return fourth;
		}
	}

	/**
	 * Funktion, um Stadtbezirk zu jedem Baum in einer Liste zu finden und dann eine
	 * Liste über alle geänderten Bäume ausgeben
	 * 
	 * @param bauemeLatLong tree list ready for GoogleGeocodeAPI reverse geocoding
	 *                      request (with GPS-coordinates)
	 * @return tree list with latlong coordinates and attributes "neighborhood",
	 *         "sublocality" and "formatted_address"
	 * @author Jo
	 */

	private static List<Baum> anfrageUeberListe(List<Baum> bauemeLatLong) {
		Iterator<Baum> it = bauemeLatLong.iterator();
		List<Baum> output = new ArrayList<Baum>();
		String response = null;
		GoogleApi google = new GoogleApi();

		while (it.hasNext()) {
			Baum currentBaum = it.next();
			try {
				response = google.getJSONByGoogle(currentBaum.x, currentBaum.y);
			} catch (Exception e) {
				e.printStackTrace();
			}
			currentBaum.extractAttributesFromReponseJson(response);
			output.add(currentBaum);
		}
		return output;
	}

	/**
	 * Function to change the coordinate system of all trees in a list from utm to
	 * latlong
	 * 
	 * @param baeume List of trees that has been read from csv file
	 * @return new List of trees with GPS-coordinates
	 * @author Jo
	 */

	private static List<Baum> createLatLongList(List<Baum> baeume) {
		Iterator<Baum> it = baeume.iterator();
		List<Baum> output = new ArrayList<Baum>();
		while (it.hasNext()) {
			Baum currentBaum = it.next();
			LatLon coord = UTMCoord.locationFromUTMCoord(32, AVKey.NORTH, currentBaum.x, currentBaum.y, null);
			output.add(new Baum(coord.getLatitude().getDegrees(), coord.getLongitude().getDegrees(), true));
		}

		return output;
	}

}
