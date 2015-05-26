import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;


public class NumberEncoder {	
	
	private HashMap<Integer, char[]> mappings = new HashMap<>();
	private ArrayList<String> words = new ArrayList<>();
	
	NumberEncoder(String filePath){
		words = readWordsFromFile(filePath);
		addMappings();
	}
		
	private void addMappings(){
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
	
	private ArrayList<String> readWordsFromFile(String filePath){
		ArrayList<String> words = new ArrayList<String>();
		try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
			String line = br.readLine();
			while (line != null) {
				words.add(line);
				line = br.readLine();
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return words;
	}
	
	private ArrayList<Integer> numberToDigits(int number){
		ArrayList<Integer> digits = new ArrayList<>();
		
		while(number > 0){
			digits.add(number%10);
			number /= 10;
		}
		
		Collections.reverse(digits);
		return digits;
	}	
	
	private ArrayList<String> matchingStrings(ArrayList<String> matches, ArrayList<Integer> digits, int index){
		int digit = digits.get(0);
		for(String word : matches){
			if(index < word.length()){
				char character = word.charAt(index);
				boolean match = false;
				for(char c : mappings.get(digit)){
					if(character == c)
						match = true;
				}
				if(!match)
					matches.remove(word);
			}				
		}
		return matches;
	}	
	
	
	public String encode(int number){			
		return null;		
	}
	
	

	
			
	
	

	
	
		 

}


