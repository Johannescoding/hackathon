import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CSV_Reader {
	private String line = "";
	private String csvSplitBy = ";";
	private int anzahlGelesene = 0;
	private int anzahlGeschriebene = 0;
	private int anzahlKaputte = 0;

	public int getAnzahlKaputte() {
		return anzahlKaputte;
	}

	public void setAnzahlKaputte(int anzahlKaputte) {
		this.anzahlKaputte = anzahlKaputte;
	}

	public int getAnzahlGeschriebene() {
		return anzahlGeschriebene;
	}

	public void setAnzahlGeschriebene(int anzahlGeschriebene) {
		this.anzahlGeschriebene = anzahlGeschriebene;
	}

	public int getAnzahlGelesene() {
		return anzahlGelesene;
	}

	public void setAnzahlGelesene(int anzahlGelesene) {
		this.anzahlGelesene = anzahlGelesene;
	}

	/**
	 * A function to read the tree csv file to a list of trees
	 * 
	 * @param csvFile File Location
	 * @return a List of all (usable) trees with their coordinates
	 * @throws IndexOutOfBoundsException
	 */
	public List<Baum> readCSVtoList(String csvFile) throws IndexOutOfBoundsException {

		List<Baum> baeume = new ArrayList<Baum>();
		BufferedReader br = null;
		try {
			br = new BufferedReader(new FileReader(csvFile));

			while ((line = br.readLine()) != null) {

				// use semicolon as separator
				String[] csvBaumFile = line.split(csvSplitBy);

				// skip first line and useless lines
				try {
					if (anzahlGelesene == 0 || csvBaumFile[4].equals("") || csvBaumFile[5].equals("")
							|| csvBaumFile[4].equals("0") || csvBaumFile[5].equals("0")) {
						anzahlGelesene++;
						continue;
					}
					// get x- and y-coordinates
					Baum currentBaum = new Baum(Double.parseDouble(csvBaumFile[4]), Double.parseDouble(csvBaumFile[5]));
					baeume.add(currentBaum);
				} catch (IndexOutOfBoundsException e) {
					anzahlGelesene++;
					anzahlKaputte++;
				}

				anzahlGelesene++;
				anzahlGeschriebene++;
			}

		} catch (IOException e) {
			System.out.println(anzahlGelesene);
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return baeume;
	}
}
