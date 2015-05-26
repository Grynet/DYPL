import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class NumberEncoder {
	
	HashMap<Integer, char[]> mappings;
	
	NumberEncoder(){
		defineMappings();
	}
	
	
	private void defineMappings(){
		mappings = new HashMap<>();
		mappings.put(0, new char[]{'e'});
		mappings.put(1, new char[]{'j','n','q'});
		mappings.put(2, new char[]{'r','w','x'});
		mappings.put(3, new char[]{'d','s','y'});
		mappings.put(4, new char[]{'f','t'});
		mappings.put(5, new char[]{'a','m'});
		mappings.put(6, new char[]{'c','i','v'});
		mappings.put(7, new char[]{'b','k','u'});
		mappings.put(8, new char[]{'l','o','p'});
		mappings.put(9, new char[]{'g','h','z'});
	}

	public String[] readFile(String filePath, int numWords) {

		String[] results = new String[numWords];
		//Skapa en counter som räknar alla rader, istället för numWords? På så sätt slippa beroendet av att veta hur många rader det är i filen.
		try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
			String line = br.readLine();
			int index = 0;

			while (line != null && index < results.length) {
				results[index++] = line;
				line = br.readLine();
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return results;
	}
	
	
	public int[] encode(String number){
		int[]numberArray = new int[number.length()];
		int counter = 0;
		for(char digit : number.toCharArray()) {
		    Integer.parseInt(digit+"");
			numberArray[counter] = Integer.parseInt(digit+"");
			counter++;
		}
		return numberArray;
	}
	
	

	public static void main(String[] args) {
		NumberEncoder encoder = new NumberEncoder();
		String filePath = "dict.txt";
		int numWords = 676;
		String[] results = encoder.readFile(filePath, numWords);
		encoder.encode("12345");
		
		 

	}

}
